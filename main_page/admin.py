from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import MainSlider, SecondarySlider, SingleBlock, StaticBlock, Review
from .forms import MainSliderForm, SecondarySliderForm, SingleBlockForm, StaticBlockForm, ReviewForm


@admin.register(MainSlider)
class MainSliderAdmin(admin.ModelAdmin):
    list_display = ("name", "get_title", "reference", "button")
    autocomplete_fields = ("news_reference", "training_reference", "course_reference")
    form = MainSliderForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            "js/admin/hide_foreign_key_fields.js",
        )


@admin.register(SecondarySlider)
class SecondarySliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("get_title", "reference")
    autocomplete_fields = ("news_reference", "training_reference", "course_reference")
    form = SecondarySliderForm

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            "js/admin/hide_foreign_key_fields.js",
        )

@admin.register(SingleBlock)
class SingleBlockAdmin(admin.ModelAdmin):
    list_display = ("get_title", "reference")
    autocomplete_fields = ("news_reference", "training_reference", "course_reference")
    form = SingleBlockForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            "js/admin/hide_foreign_key_fields.js",
        )


@admin.register(StaticBlock)
class StaticBlockAdmin(admin.ModelAdmin):
    list_display = ("get_title", "reference")
    autocomplete_fields = ("news_reference", "training_reference", "course_reference")
    form = StaticBlockForm

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            "js/admin/hide_foreign_key_fields.js",
        )

@admin.register(Review)
class ReviewAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "status", "active", "rating", "language", "has_image", "sorting")
    list_editable = ("active", )

    form = ReviewForm

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            "js/admin/hide_foreign_key_fields.js",
        )
