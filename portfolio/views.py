from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

def project_list(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(owner=request.user)
    else:
        projects = Project.objects.none()  # або показати всі, якщо це публічна галерея

    return render(request, "portfolio/project_list.html", {
        "projects": projects
    })


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("portfolio:project_list")
    return render(request, "portfolio/project_form.html", {"form": form})

@login_required
def project_update(request, pk):
    project = Project.objects.get(pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("portfolio:project_list")
    return render(request, "portfolio/project_form.html", {"form": form})

@login_required
def project_delete(request, pk):
    project = Project.objects.get(pk=pk, owner=request.user)
    if request.method == "POST":
        project.delete()
        return redirect("portfolio:project_list")
    return render(request, "portfolio/project_confirm_delete.html", {"project": project})