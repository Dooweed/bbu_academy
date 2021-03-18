import traceback
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import urlencode

from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponseForbidden, QueryDict, HttpResponseServerError
from django.template.loader import render_to_string

from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from premailer import transform

from bbu_academy.settings import EMAIL_HOST_USER, STAFF_MAILS
from courses.models import Course
from payme_billing.forms import ButtonBasePaymentInitialisationForm, QrBasePaymentInitialisationForm
from payme_billing.vars.settings import URL
from trainings.models import Training
from .models import Student, IndividualPayer, PurchaseRecord
from .forms import IndividualPayerForm, StudentForm, SelfPaymentForm, ConfirmationForm, EntityPayerForm, PaymentForm

from django.utils.translation import gettext as _

SUBMIT = "submit"
EDIT = "edit"
DELETE = "delete"


# Utility functions
def get_students_list(record):
    students_list = []

    for student in record.students.all():
        student_form = StudentForm(instance=student, initial={"id": student.id})
        student_form.study_document_link = student.study_document_link
        student_form.student_passport_link = student.passport_link
        students_list.append(student_form)

    return students_list
def get_record(request):
    if "record_id" in request.session:  # Use created record if it exists
        record = PurchaseRecord.objects.get_or_create(id=request.session["record_id"])[0]
    else:
        record = PurchaseRecord.objects.create()
        request.session["record_id"] = record.id
        request.session.modified = True
    return record


def offer_agreement_view(request):
    if request.method == "POST":
        record = get_record(request)
        record.offer_agreement = True
        record.save()
        return redirect("purchase:individual-form")
    else:
        return render(request, "purchase/offer-agreement.html")


def individual_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("purchase:offer-agreement")

    if request.method == "POST":  # Post method
        self_payment_form = SelfPaymentForm(request.POST)
        self_payment = self_payment_form.is_valid() and self_payment_form.cleaned_data.get("self_payment")

        student_post = {}
        student_files = {}
        if self_payment:
            for key in request.POST.keys():
                student_post[key.replace("individual_payer_", "student_")] = request.POST[key]
            for key in request.FILES.keys():
                student_files[key.replace("individual_payer_", "student_")] = deepcopy(request.FILES[key]) if key.startswith("individual_payer_") else request.FILES[key]

        individual_payer_form = IndividualPayerForm(request.POST, request.FILES)
        student_form = StudentForm(QueryDict(urlencode(student_post)), student_files) if self_payment else StudentForm(request.POST, request.FILES)

        if individual_payer_form.is_valid():  # Save individual_payer_form if it is correct
            payer: IndividualPayer = individual_payer_form.save(commit=False)
            if record.get_individual_payer_or_none():  # Use existing ID if possible
                payer.id = record.get_individual_payer_or_none().id
            payer.record = record
            payer.save()
            payer.save_passport(individual_payer_form.cleaned_data.get("individual_payer_passport"))

            if record.get_entity_payer_or_none():  # Delete ENTITY PAYER if exists
                record.get_entity_payer_or_none().delete()

        if student_form.is_valid():  # Save student_form if it is correct
            student: Student = student_form.save(commit=False)
            if record.students.exists():  # Use existing ID if possible
                student.id = record.students.order_by("-id").first().id
            student.record = record
            student.save()
            student.save_passport(student_form.cleaned_data.get("student_passport"))
            student.save_study_document(student_form.cleaned_data.get("study_document"))

            if record.students.count() > 1:  # Delete all other students if exists
                record.students.exclude(id=student.id).delete()

        # Redirect to the next step if everything is correct
        if record.individual_form_is_ready():
            return redirect("purchase:confirmation-form")

    else:  # GET method
        student_form = StudentForm(instance=record.students.order_by("-id").first())
        individual_payer_form = IndividualPayerForm(instance=record.get_individual_payer_or_none())
        self_payment_form = SelfPaymentForm()

    payer_correct = bool(record.get_individual_payer_or_none())
    student_correct = record.students.exists()

    context = {
        "student_fields": student_form.get_student_fields(),
        "payer_fields": individual_payer_form.visible_fields(),
        "free_fields": student_form.get_rest_fields(),
        "self_payment": self_payment_form,
        "payer_correct": payer_correct,
        "student_correct": student_correct,
    }

    return render(request, "purchase/individual-form.html", context)


def entity_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("purchase:offer-agreement")

    student_missing = False
    payer_missing = False

    if request.method == "POST":
        if record.entity_form_is_ready():
            return redirect("purchase:confirmation-form")
        else:
            student_missing = not record.students.exists()
            payer_missing = not bool(record.get_entity_payer_or_none())

    context = {"SUBMIT": SUBMIT, "student_missing": student_missing, "payer_missing": payer_missing}
    return render(request, "purchase/entity-form.html", context)


def entity_form_load_data(request):
    record = get_record(request)

    if request.is_ajax():
        payer = record.get_entity_payer_or_none()

        student_form_context = {"student_form": StudentForm(), "editing": False}
        students_list_context = {"EDIT": EDIT, "DELETE": DELETE, "students_list": get_students_list(record)}
        payer_form_context = {"payer_form": EntityPayerForm(instance=payer), "payer_is_valid": bool(payer)}

        data = {"payer_form": render_to_string("purchase/chunks/entity-payer-form.html", payer_form_context, request=request),
                "student_form": render_to_string("purchase/chunks/student-form.html", student_form_context, request=request),
                "students_list": render_to_string("purchase/chunks/student-display.html", students_list_context, request=request)}

        return JsonResponse(data=data)


def ajax_student(request, action: str):
    try:
        if request.is_ajax():
            record = get_record(request)

            if action == SUBMIT:
                student_form = StudentForm(request.POST, request.FILES)
                if student_form.is_valid():
                    student = student_form.save(commit=False)
                    if student_form.id_is_valid():  # Edit existing student
                        id = student_form.cleaned_data.get("id")
                        if record.students.filter(id=id).exists():
                            student.id = id
                        else:
                            return HttpResponseForbidden()
                    student.record = record
                    student.save()
                    student.save_passport(student_form.cleaned_data.get("student_passport"))
                    student.save_study_document(student_form.cleaned_data.get("study_document"))

                    student_form = StudentForm()
            elif action == EDIT:
                student_form = StudentForm(request.GET)
                if student_form.id_is_valid():
                    id = student_form.cleaned_data.get("id")

                    if record.students.filter(id=id).exists():
                        student_form = StudentForm(instance=Student.objects.get(id=id), initial={"id": id})
                    else:  # Raise an error if the user is not owner of requested student object
                        return HttpResponseForbidden()
                else:
                    raise Http404()
            elif action == DELETE:
                student_form = StudentForm(request.GET)
                if student_form.id_is_valid():
                    id = student_form.cleaned_data.get("id")

                    if record.students.filter(id=id).exists():
                        student_form = None
                        record.students.get(id=id).delete()
                    else:  # Raise an error if the user is not owner of requested student object
                        return HttpResponseForbidden()
                else:
                    raise Http404()
            else:
                raise Http404()

            students_list = get_students_list(record)

            student_form_context = {"student_form": student_form, "editing": action == EDIT}
            students_list_context = {"EDIT": EDIT, "DELETE": DELETE, "students_list": students_list}

            data = {
                "student_form": render_to_string("purchase/chunks/student-form.html", student_form_context, request=request) if student_form else None,
                "students_list": render_to_string("purchase/chunks/student-display.html", students_list_context, request=request),
            }

            return JsonResponse(data=data)
        else:
            raise Http404()
    except:
        traceback.print_exc()
        raise


def ajax_payer(request, action: str):
    if request.is_ajax():
        record = get_record(request)

        if action == SUBMIT:
            payer_form = EntityPayerForm(request.POST)
            payer_is_valid = payer_form.is_valid()
            if payer_is_valid:
                payer = payer_form.save(commit=False)
                if record.get_entity_payer_or_none():
                    payer.id = record.get_entity_payer_or_none().id
                payer.record = record
                payer.save()

                if record.get_individual_payer_or_none():  # Delete INDIVIDUAL PAYER if exists
                    record.get_individual_payer_or_none().delete_temp_files()
                    record.get_individual_payer_or_none().delete()
        else:
            raise Http404()

        payer_form_context = {"payer_form": payer_form, "payer_is_valid": payer_is_valid}

        data = {
            "payer_form": render_to_string("purchase/chunks/entity-payer-form.html", payer_form_context, request=request),
        }

        return JsonResponse(data=data)
    else:
        raise Http404()


def confirmation_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("purchase:offer-agreement")
    elif not record.is_ready():  # Redirect to form if it is not valid
        return redirect("purchase:entity-form") if record.get_entity_payer_or_none() else redirect("purchase:individual-form")

    if request.method == "POST":
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            product = Course.objects.get(id=form.cleaned_data.get("p_id")) if form.cleaned_data.get("is_course") else Training.objects.get(id=form.cleaned_data.get("p_id"))
            record.product = product
            record.special_price = form.cleaned_data.get("special_price")
            record.price = product.special_price if record.special_price else product.price
            record.overall_price = record.students.count() * record.price
            record.study_type = form.cleaned_data.get("study_type")
            if record.get_entity_payer_or_none():  # Fill payment type if payer is entity (entity has only ONE option of payment)
                record.payment_type = "bank"
            record.save()

            return redirect("purchase:payment-form")
    else:
        product_class = request.session.get('product_class')
        product_id = request.session.get('product_id')
        initial = {}
        if product_class and product_id:
            initial["product"] = f"{product_class.lower()}-{product_id}"
        if record.study_type:
            initial["study_type"] = record.study_type

        form = ConfirmationForm(initial=initial)

    context = {
        "form": form,
    }

    return render(request, "purchase/confirmation-form.html", context)


def payment_form_view(request):
    record = get_record(request)

    if not record.offer_agreement:  # Redirect to offer-agreement if user haven't agreed
        return redirect("purchase:offer-agreement")
    elif not record.is_ready():  # Redirect to form if it is not valid
        return redirect("purchase:entity-form") if record.get_entity_payer_or_none() else redirect("purchase:individual-form")
    elif not record.is_confirmed():
        return redirect("purchase:confirmation-form")

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():  # Finish purchase
            record.payment_type = form.cleaned_data.get("payment_type")
            record.save()

            # Send mail with full information to workers and payer
            html_content = render_to_string("purchase/mail/html_mail.html", {"payer": record.payer, "students_list": get_students_list(record), "mail": True}, request=request)
            text_content = strip_tags(render_to_string("purchase/mail/text_mail.html", {"payer": record.payer, "students_list": record.students.all(), "mail": True}))
            mail = EmailMultiAlternatives(subject="Новая покупка", body=text_content, from_email=EMAIL_HOST_USER, to=STAFF_MAILS + [record.payer.email()])
            mail.attach_alternative(transform(html_content, base_url=f"{request.scheme}://{request.get_host()}"), 'text/html')  # Attach html version

            # Attach files
            for student in record.students.all():
                archive_name = str(student.folder_path / f"{student.name}.zip")
                with ZipFile(archive_name, "w") as archive:
                    archive.write(student.passport_path)
                    archive.write(student.study_document_path)
                with open(archive_name, "rb") as archive:
                    mail.attach(archive_name, archive.read())
                Path(archive_name).unlink()

            if record.get_individual_payer_or_none() is not None:
                mail.attach(record.payer.passport_path.name, record.payer.passport_path.read_bytes())

            result = mail.send()

            if result:
                # record.delete_temp_files()
                return redirect("purchase:payme-payment")
            else:
                return HttpResponseServerError(_("Что-то пошло не так при оформлении заказа. Разработчик был уведомлён об ошибке. Приносим свои извинения"))

    form = PaymentForm(instance=record)

    context = {
        "record": record,
        "form": form,
    }

    return render(request, "purchase/payment-form.html", context)

def payme_payment_view(request):
    record = get_record(request)

    button_form = ButtonBasePaymentInitialisationForm(record.id, record.get_9_digit_phone(), record.get_amount() * 100, request.LANGUAGE_CODE, style="white")
    qr_form = QrBasePaymentInitialisationForm(record.id, record.get_9_digit_phone(), record.get_amount() * 100, request.LANGUAGE_CODE)

    context = {
        "button_form": button_form,
        "qr_form": qr_form,
        "url": URL,
    }

    return render(request, "purchase/payme.html", context)
