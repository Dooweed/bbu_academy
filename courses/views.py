from django.shortcuts import render, get_object_or_404

# Create your views here.
from courses.models import Course
from settings.models import Page


def courses_list_view(request):
    page = get_object_or_404(Page, name="courses:courses")
    courses = Course.objects.filter(active=True)[:10]

    context = {
        "courses": courses,
        "page": page
    }
    return render(request, 'courses/courses.html', context)

def course_view(request, course_url):
    page = get_object_or_404(Page, name="courses:course")
    course = get_object_or_404(Course, url=course_url, active=True)

    context = {
        "course": course,
        "page": page
    }
    return render(request, 'courses/course.html', context)
