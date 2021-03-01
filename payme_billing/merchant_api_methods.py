from django.utils import timezone

from payme_billing.models import PaymeTransaction

from .utils import Error, Correct
from .vars import MODEL


def perform(name, params):
    return eval(f"_{name}(params)")


def _CheckPerformTransaction(params):
    # Check that all required params are present and correct
    amount = params.get("amount")
    account = params.get("account")
    if not amount or not isinstance(amount, int) or not account or not isinstance(account, dict):
        return Error(-32600)
    # Check that Account object has all necessary for operation fields
    purchase_id = account.get("purchase_id")
    phone = account.get("phone")
    if not purchase_id or not isinstance(purchase_id, int) or not phone:
        return Error(-32600)

    # Check that purchase exist
    purchase = MODEL.objects.filter(id=purchase_id, is_paid=False, payment_type="payme")
    if not purchase.exists():
        return Error(-31050)

    # Check that phone is correct
    if purchase.phone != phone:
        return Error(-31051)

    # Check that amount is correct
    if purchase.overall_price * 100 != amount:
        return Error(-31001)

    # All checks are passed, returning positive response
    response = {
        "allow": True
    }
    return Correct(response)


def _CreateTransaction(params):
    # Check that all required params are present and correct
    id = params.get("id")
    amount = params.get("amount")
    account = params.get("account")
    if not id or not amount or not isinstance(amount, int) or not account or not isinstance(account, dict):
        return Error(-32600)
    # Check that Account object has all necessary for operation fields
    purchase_id = account.get("purchase_id")
    phone = account.get("phone")
    if not purchase_id or not isinstance(purchase_id, int) or not phone:
        return Error(-32600)

    # Retrieve transaction object
    transaction = PaymeTransaction.objects.filter(transaction_id=id)

    # If transaction already exist
    if transaction.exists():
        transaction = transaction.get()

        if transaction.state != 1:  # Transaction is not in ready state
            return Error(-31008)
        elif transaction.is_timed_out():  # Transaction is timed out
            transaction.state = -1
            transaction.denial_reason = 4
            transaction.save()
            return Error(-31008)
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
            transaction = PaymeTransaction.objects.create(transaction_id=id, record_id=purchase_id, amount=amount, phone=phone, state=1)

    # All checks are passed, returning positive response
    response = {
        "create_time": transaction.creation_time * 1000,
        "transaction": transaction.transaction_id,
        "state": transaction.state,
    }
    return Correct(response)


def _PerformTransaction(params):
    # Check that all required params are present and correct
    id = params.get("id")
    if not id:
        return Error(-32600)

    # Retrieve transaction object
    transaction = PaymeTransaction.objects.filter(transaction_id=id)

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
                return Error(-31008)
            # Transaction is NOT timed out
            else:
                # Return error if model object was not found
                if MODEL.objects.filter(id=transaction.record_id, is_paid=False, payment_type="payme").update(is_paid=True) != 1:
                    return Error(-31050)
                transaction.perform_time = timezone.now()
                transaction.save()
        # Transaction is already completed
        elif transaction.state == 2:
            pass
        # Transaction is NOT performed and NOT ready to be performed
        else:
            return Error(-31008)
    # If transaction does not exist
    else:
        return Error(-31003)

    # All checks are passed, returning positive response
    response = {
        "state": transaction.state,
        "perform_time": transaction.perform_time,
        "transaction": transaction.transaction_id,
    }

    return Correct(response)


def _CancelTransaction(params):
    return


def _CheckTransaction(params):
    return


def _GetStatement(params):
    return
