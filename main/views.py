import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


def show_main(request):
    return render(request, "index.html", {
        "last_login": request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan"),
    })


def show_project(request):
    title_query = request.GET.get("title", "").strip()
    context = {
        "title_query": title_query,
        "is_editor": is_editor(request.user),
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")
    return render(request, "projects_form.html", {"form": form})


@login_required(login_url="/login/")
def edit_project(request, project_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_project")
    return render(request, "projects_form.html", {"form": form, "is_edit": True, "project": project})


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    data = []
    for project in projects:
        starred_users = list(project.starred_by.all())
        data.append({
            "pk": str(project.pk),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "repository_url": project.repository_url,
                "project_image_url": project.project_image_url,
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and any(user.pk == request.user.pk for user in starred_users),
                "starred_by_names": ", ".join(user.username for user in starred_users),
            },
        })
    return JsonResponse(data, safe=False)


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse({"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."}, status=403)
    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse({"message": "Proyek berhasil ditambahkan.", "pk": str(project.pk)}, status=201)
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Proyek berhasil dihapus!")
    return redirect("main:show_project")


def show_experience(request):
    return render(request, "experience.html", {
        "experiences": Experience.objects.order_by("-started_at"),
        "is_editor": is_editor(request.user),
    })


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil ditambahkan!")
        return redirect("main:show_experience")
    return render(request, "experience_form.html", {"form": form, "is_edit": False})


@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")
    return render(request, "experience_form.html", {"form": form, "is_edit": True})


@require_POST
@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    return render(request, "register.html", {"name": "Muhammad Adib Islami", "form": form})


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        redirect_to = request.POST.get("next") or request.GET.get("next", "")
        if not url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}):
            redirect_to = "main:show_main"
        response = redirect(redirect_to)
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response
    return render(request, "login.html", {"name": "Muhammad Adib Islami", "form": form})


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


@login_required(login_url="/login/")
@require_POST
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return redirect("main:show_project")
