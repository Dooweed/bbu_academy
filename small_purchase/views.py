from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from premailer import transform

from bbu_academy.settings import EMAIL_PAYMENT_NOTIFICATION_USER, STAFF_MAILS, BASE_DIR
from payme_billing.forms import ButtonBasePaymentInitialisationForm
from payme_billing.utils import get_payment_link
from payme_billing.vars.settings import URL
from purchase.utils import get_atb_members_list, build_invoice, delete_session_purchase_record
from services.models import Service
from small_purchase.forms import IndividualPayerForm, EntityPayerForm, ConfirmationForm, PaymentForm
from small_purchase.models import SmallPurchaseRecord, IndividualPayer, EntityPayer


PASSPORT_EMAIL_FILE_NAME = 'passport'
PASSPORT = _('Паспорт')
INVOICE = _("Счёт")


def placeholder(request):
    return HttpResponse("It's a placeholder, dude")


def get_record(request):
    if "record_id" in request.session:  # Use created record if it exists
        record = SmallPurchaseRecord.objects.get_or_create(id=request.session["record_id"])[0]
    else:
        record = SmallPurchaseRecord.objects.create()
        request.session["record_id"] = record.id
        request.session.modified = True
    return record


def offer_agreement_view(request):
    if request.method == "POST":
        record = get_record(request)
        if record.finished:
            return redirect("small_purchase:finished")
        record.offer_agreement = True
        record.save()
        return redirect("small_purchase:individual-form")
    else:
        return render(request, "small_purchase/offer-agreement.html")


def individual_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("small_purchase:offer-agreement")
    elif record.finished:
        return redirect("small_purchase:finished")

    if request.method == "POST":  # Post method
        form = IndividualPayerForm(request.POST, files=request.FILES)

        if form.is_valid():  # Save form if it is correct
            instance: IndividualPayer = form.save(commit=False)
            if record.get_individual_payer_or_none():  # Use existing ID if possible
                instance.id = record.get_individual_payer_or_none().id
            instance.record = record
            instance.save()
            instance.save_passport(form.cleaned_data.get("passport"))

            if record.get_entity_payer_or_none():  # Delete bounded ENTITY PAYER if exists
                record.get_entity_payer_or_none().delete()

            # Redirect to the next step if everything is correct
            return redirect("small_purchase:confirmation-form")

    else:  # GET method
        form = IndividualPayerForm(instance=record.get_individual_payer_or_none())

    context = {
        "form": form,
    }

    return render(request, "small_purchase/individual-form.html", context)


def entity_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("small_purchase:offer-agreement")
    elif record.finished:
        return redirect("small_purchase:finished")

    if request.method == "POST":  # Post method
        form = EntityPayerForm(request.POST)

        if form.is_valid():  # Save form if it is correct
            instance: EntityPayer = form.save(commit=False)
            if record.get_entity_payer_or_none():  # Use existing ID if possible
                instance.id = record.get_entity_payer_or_none().id
            instance.record = record
            instance.save()

            if record.get_individual_payer_or_none():  # Delete bounded INDIVIDUAL PAYER if exists
                record.get_individual_payer_or_none().delete()

            # Redirect to the next step if everything is correct
            return redirect("small_purchase:confirmation-form")

    else:  # GET method
        form = EntityPayerForm(instance=record.get_entity_payer_or_none())

    context = {
        "form": form,
    }

    return render(request, "small_purchase/entity-form.html", context)


def confirmation_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("small_purchase:offer-agreement")
    elif not record.is_ready():  # Redirect to form if it is not valid
        return redirect("small_purchase:entity-form") if record.get_entity_payer_or_none() else redirect("small_purchase:individual-form")
    elif record.finished:
        return redirect("small_purchase:finished")

    if request.method == "POST":
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            record.amount = form.cleaned_data.get('amount')
            record.service = form.cleaned_data.get('service')

            if record.get_entity_payer_or_none():
                member_list = get_atb_members_list()
                record.special_price = record.payer.inn in member_list
                # Fill payment type if payer is entity (entity has only ONE option of payment)
                record.payment_type = "bank"
            record.price = record.service.special_price if record.special_price else record.service.price
            record.overall_price = record.amount * record.price
            record.save()

            return redirect("small_purchase:payment-form")
    else:
        if request.session.get('product_class') == 'Service':
            record.service = Service.objects.get(id=request.session.get('product_id'))
            record.save()
        record.amount = 1
        form = ConfirmationForm(instance=record)

    context = {
        "form": form,
        "is_entity": bool(record.get_entity_payer_or_none()),
    }

    return render(request, "small_purchase/confirmation-form.html", context)


def payment_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("small_purchase:offer-agreement")
    elif not record.is_ready():  # Redirect to form if it is not valid
        return redirect("small_purchase:entity-form") if record.get_entity_payer_or_none() else redirect("small_purchase:individual-form")
    elif not record.is_confirmed():
        return redirect("small_purchase:confirmation-form")
    elif record.finished:
        return redirect("small_purchase:finished")

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():  # Finish purchase
            payment_type = form.cleaned_data.get("payment_type")

            record.payment_type = payment_type
            record.date_finished = timezone.now()
            record.save()

            # Send mail with full information to workers and payer
            if payment_type == "payme":
                payment_link = get_payment_link(record.id, record.get_9_digit_phone(), record.get_amount() * 100, request.LANGUAGE_CODE,
                                                request.build_absolute_uri(reverse("small_purchase:finished")))
            else:
                payment_link = None
            build_invoice(record, request, True)
            html_context = {"payer": record.payer, "mail": True, "payment_link": payment_link}
            plain_context = {"payer": record.payer, "mail": True}
            html_content = render_to_string("small_purchase/mail/html_mail.html", html_context, request=request)
            text_content = strip_tags(render_to_string("small_purchase/mail/text_mail.html", plain_context))
            mail = EmailMultiAlternatives(subject="Новая покупка", body=text_content, from_email=EMAIL_PAYMENT_NOTIFICATION_USER, to=STAFF_MAILS + [record.payer.email])
            with open(BASE_DIR / "static" / "css" / "mail.css", 'r') as css:
                css = css.read().replace('\n', '')
                mail.attach_alternative(transform(html_content, css_text=css), 'text/html')  # Attach html version

            # Attach files
            mail.attach(INVOICE + record.invoice_path.suffix, record.invoice_path.read_bytes())
            if record.get_individual_payer_or_none() is not None:  # Only individuals submit their passport
                mail.attach(PASSPORT_EMAIL_FILE_NAME + record.payer.passport_path.suffix, record.payer.passport_path.read_bytes())

            result = mail.send()

            request.session["allow_media"] = record.id
            delete_session_purchase_record(request)
            if not record.finished:
                record.finish()

            if result:
                if payment_type == "payme":
                    return redirect("small_purchase:payme-payment")
                else:
                    return redirect("small_purchase:finished")
            else:
                return HttpResponseServerError(_("Что-то пошло не так при оформлении заказа. Разработчик был уведомлён об ошибке. Приносим свои извинения"))

    form = PaymentForm(instance=record)

    context = {
        "record": record,
        "form": form,
    }

    return render(request, "small_purchase/payment-form.html", context)


def payme_payment_view(request):
    record_id = request.session.get("allow_media")
    if record_id and SmallPurchaseRecord.objects.filter(id=request.session["allow_media"]).exists():
        record = SmallPurchaseRecord.objects.get(id=request.session["allow_media"])
    else:  # Redirect to index if session has no record
        return redirect("index")

    if record.is_paid:
        return redirect("small_purchase:finished")
    elif not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("small_purchase:offer-agreement")
    elif not record.is_ready():  # Redirect to form if it is not valid
        return redirect("small_purchase:entity-form") if record.get_entity_payer_or_none() else redirect("small_purchase:individual-form")
    elif not record.is_confirmed():
        return redirect("small_purchase:confirmation-form")

    payment_link = get_payment_link(f'S{record.id}', record.get_9_digit_phone(), record.get_amount() * 100, request.LANGUAGE_CODE,
                                    request.build_absolute_uri(reverse("small_purchase:finished")))

    button_form = ButtonBasePaymentInitialisationForm(f'S{record.id}', record.get_9_digit_phone(), record.get_amount() * 100,
                                                      request.LANGUAGE_CODE, request.build_absolute_uri(reverse("small_purchase:finished")), style="white", width=300)

    context = {
        "button_form": button_form,
        "url": URL,
        "payment_link": payment_link,
    }

    return render(request, "purchase/payme.html", context)


def payment_finished_view(request):
    record_id = request.session.get("allow_media")
    if record_id:
        record = SmallPurchaseRecord.objects.get(id=request.session["allow_media"])
    else:  # Redirect to index if session has no record
        return redirect("index")

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("small_purchase:offer-agreement")
    elif not record.is_ready():  # Redirect to form if it is not valid
        return redirect("small_purchase:entity-form") if record.get_entity_payer_or_none() else redirect("small_purchase:individual-form")
    elif not record.is_confirmed():
        return redirect("small_purchase:confirmation-form")

    context = {
        "payme_completed": record.payment_type == "payme" and record.is_paid,
        "invoice_link": request.build_absolute_uri(record.invoice_link()),
    }

    return render(request, "small_purchase/finished.html", context)
