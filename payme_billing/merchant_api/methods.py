from django.utils import timezone

from payme_billing.models import PaymeTransaction

from payme_billing.merchant_api.classes import Error, Correct, PaymeCheckFailedException
from payme_billing.merchant_api.checks import check_amount, check_account, check_transaction_id, check_time, check_time_diapason, check_reason
from payme_billing.vars.settings import MODEL
from payme_billing.vars.static import *


def perform(name, params):
    return eval(f"_{name}(params)")


def _CheckPerformTransaction(params):
    # Check that all required params are present and correct
    try:
        amount = check_amount(params)
        purchase_id, phone = check_account(params)
    except PaymeCheckFailedException as e:
        return e.error()

    # Check that purchase exist
    purchase = MODEL.objects.filter(id=purchase_id, payment_type="payme")
    if not purchase.exists():
        return Error(RECEIPT_NOT_FOUND_ERROR)
    else:
        purchase = purchase.get()

    # Check that purchase is not available for new transaction (already tied to another transaction)
    if purchase.state == 0:  # Go ahead, purchase is available
        pass
    elif purchase.state == 4:
        return Error(RECEIPT_PAID_ERROR)
    elif purchase.state == 50:
        return Error(RECEIPT_CANCELLED_ERROR)
    else:
        return Error(RECEIPT_BUSY_ERROR)

    # Check that phone is correct
    if phone != purchase.get_9_digit_phone():
        return Error(PHONE_ERROR)

    # Check that amount is correct
    if purchase.overall_price * 100 != amount:
        return Error(AMOUNT_ERROR)

    # All checks are passed, returning positive response
    response = {
        "allow": True
    }
    return Correct(response)


def _CreateTransaction(params):
    # Check that all required params are present and correct
    try:
        transaction_id = check_transaction_id(params)
        amount = check_amount(params)
        purchase_id, phone = check_account(params)
        time = check_time(params)
    except PaymeCheckFailedException as e:
        return e.error()

    # Retrieve transaction object
    transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id)

    # If transaction already exist
    if transaction.exists():
        transaction = transaction.get()

        if transaction.state != 1:  # Transaction is not in ready state
            return Error(CANNOT_PERFORM_ERROR)
        elif transaction.is_timed_out():  # Transaction is timed out
            transaction.state = -1
            transaction.denial_reason = 4
            transaction.save()
            return Error(CANNOT_PERFORM_ERROR)
        else:  # Transaction is READY to be performed
            transaction.state = 1
            transaction.save()
    # If transaction does not exist yet
    else:
        # Check that operation can be performed
        result = _CheckPerformTransaction(params)
        if result.is_error():
            return result
        else:
            transaction = PaymeTransaction.objects.create(transaction_id=transaction_id, record_id=purchase_id, amount=amount, phone=phone, state=1, payme_creation_time=time)
            if MODEL.objects.filter(id=purchase_id).update(state=1) != 1:
                return Error(RECEIPT_NOT_FOUND_ERROR)

    # All checks are passed, returning positive response
    response = {
        "create_time": transaction.get_creation_time(),
        "transaction": transaction.transaction_id,
        "state": transaction.state,
    }
    return Correct(response)


def _PerformTransaction(params):
    # Check that all required params are present and correct
    try:
        transaction_id = check_transaction_id(params)
    except PaymeCheckFailedException as e:
        return e.error()

    # Retrieve transaction object
    transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id)

    # If transaction exist
    if transaction.exists():
        transaction = transaction.get()

        # Transaction is in pending state
        if transaction.state == 1:
            # Transaction is timed out
            if transaction.is_timed_out():
                transaction.state = -1
                transaction.denial_reason = 4
                transaction.save()
                return Error(CANNOT_PERFORM_ERROR)
            # Transaction is NOT timed out
            else:
                # Return error if model object was not found
                purchase = MODEL.objects.filter(id=transaction.record_id, payment_type="payme")
                if purchase.get().is_paid:
                    return Error(RECEIPT_PAID_ERROR)
                if purchase.update(is_paid=True, state=4) != 1:
                    return Error(RECEIPT_NOT_FOUND_ERROR)
                transaction.perform_time = timezone.now()
                transaction.state = 2
                transaction.save()
        # Transaction is already completed
        elif transaction.state == 2:
            pass
        # Transaction is NOT performed and NOT ready to be performed
        else:
            return Error(CANNOT_PERFORM_ERROR)
    # If transaction does not exist
    else:
        return Error(TRANSACTION_NOT_FOUND_ERROR)

    # All checks are passed, returning positive response
    response = {
        "state": transaction.state,
        "perform_time": transaction.get_perform_time(),
        "transaction": transaction.transaction_id,
    }

    return Correct(response)


def _CancelTransaction(params):
    try:
        transaction_id = check_transaction_id(params)
        reason = check_reason(params)
    except PaymeCheckFailedException as e:
        return e.error()

    # Retrieve transaction object
    transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id)

    # If transaction exist
    if transaction.exists():
        transaction = transaction.get()

        # Transaction is in pending state
        if transaction.state == 1:
            transaction.state = -1
            transaction.denial_reason = reason
            transaction.cancel_time = timezone.now()
            transaction.save()
        # Transaction is already completed
        elif transaction.state == 2:
            return Error(CANNOT_CANCEL_ERROR)

    # If transaction does not exist
    else:
        return Error(TRANSACTION_NOT_FOUND_ERROR)

    # All checks are passed, returning positive response
    response = {
        "cancel_time": transaction.get_cancel_time(),
        "state": transaction.state,
        "transaction": transaction.transaction_id
    }

    return Correct(response)


def _CheckTransaction(params):
    # Check that all required params are present and correct
    try:
        transaction_id = check_transaction_id(params)
    except PaymeCheckFailedException as e:
        return e.error()

    # Retrieve transaction object
    transaction = PaymeTransaction.objects.filter(transaction_id=transaction_id)

    # If transaction exist
    if transaction.exists():
        transaction = transaction.get()
    # If transaction does not exist
    else:
        return Error(TRANSACTION_NOT_FOUND_ERROR)

    # All checks are passed, returning positive response
    response = {
        "create_time": transaction.get_creation_time(),
        "perform_time": transaction.get_perform_time(),
        "cancel_time": transaction.get_cancel_time(),
        "transaction": transaction.transaction_id,
        "state": transaction.state,
        "reason": transaction.denial_reason
    }

    return Correct(response)


def _GetStatement(params):
    time_from, time_to = check_time_diapason(params)

    transactions = PaymeTransaction.objects.filter(payme_creation_time__gte=time_from, payme_creation_time__lte=time_to)

    response = []
    for transaction in transactions:
        purchase = MODEL.objects.get(id=transaction.record_id)
        response.append({
            "id": transaction.transaction_id,
            "time": transaction.get_payme_creation_time(),
            "amount": purchase.get_amount(),
            "account": {
                "purchase_id": purchase.id,
                "phone": purchase.get_9_digit_phone(),
            },
            "create_time": transaction.get_creation_time(),
            "perform_time": transaction.get_perform_time(),
            "cancel_time": transaction.get_cancel_time(),
            "transaction": transaction.transaction_id,
            "state": transaction.state,
            "reason": transaction.denial_reason,
        })

    return response
