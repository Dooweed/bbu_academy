from django.contrib import admin

# from .forms import ProductForm
from .models import *

# Register your models here.

class StudentInline(admin.StackedInline):
    model = Student
    extra = 0
    can_delete = False

    class Media:
        css = {'all': ('css/no-add_another-button.css',)}

class IndividualPayerInline(admin.StackedInline):
    model = IndividualPayer
    extra = 0
    can_delete = False

    class Media:
        css = {'all': ('css/no-add_another-button.css',)}

class EntityPayerInline(admin.StackedInline):
    model = EntityPayer
    extra = 0
    can_delete = False

    class Media:
        css = {'all': ('css/no-add_another-button.css',)}


@admin.register(PurchaseRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_filter = ("is_paid", "finished", "study_type", "overall_price", "payment_type", "date_started", "date_finished")
    list_display = ("payer_name", "payer_type", "student_name", "overall_price", "payment_type", "study_type", "date_started", "finished")

    # "id", "finished", "study_type", "payment_type", "get_price", "overall_price", "date_started", "date_finished"
    fields = ("id", "offer_agreement", "is_paid", "finished", "study_type", "special_price", "payment_type", "get_price", "overall_price", "date_started", "date_finished")
    readonly_fields = ("id", "get_price", "date_started", "date_finished", "overall_price")
    inlines = (StudentInline, IndividualPayerInline, EntityPayerInline)

    save_on_top = True

    # form = ProductForm

    def get_inlines(self, request, obj):
        if obj.payer:
            return StudentInline, eval(f"{type(obj.payer).__name__}Inline")
        else:
            return StudentInline,

    def has_add_permission(self, request):
        return False

@admin.register(AtbMembers)
class AtbMembersAdmin(admin.ModelAdmin):
    list_display = ("__str__", "was_used")
