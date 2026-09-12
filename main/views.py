from django.shortcuts import render
from main.models import Experience

def show_main(request):
    context = {
        "name": "Nama Lengkap Anda",           # Ganti dengan nama Anda
        "npm": "NPM_Anda",                     # Ganti dengan NPM Anda
        "study_program": "S1 Ilmu Komputer",   # Program Studi
        "bio": (
            "Mahasiswa Fakultas Ilmu Komputer Universitas Indonesia "
            "yang tertarik pada software engineering dan pemrograman berbasis platform."
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Nama Lengkap Anda",           # Sesuaikan nama
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)