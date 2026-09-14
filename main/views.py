from django.shortcuts import render
from main.models import Experience, Project


def show_main(request):
    context = {
        "name": "Muhammad Adib Islami",
        "npm": "2506657030",
        "class_name": "PBP C",
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Muhammad Adib Islami",
        "experiences": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_project(request):
    context = {
        "name": "Muhammad Adib Islami",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)