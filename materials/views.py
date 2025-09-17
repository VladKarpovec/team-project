from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Material
from .forms import MaterialForm


def material_list(request):
    materials = Material.objects.order_by('-created_at')
    return render(request, 'materials/material_list.html', {'materials': materials})


@login_required
def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'materials/material_detail.html', {'material': material})


@staff_member_required
def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('materials:material_list')
    else:
        form = MaterialForm()
    return render(request, 'materials/material_form.html', {'form': form})


@staff_member_required
def material_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('materials:material_detail', pk=pk)
    else:
        form = MaterialForm(instance=material)
    return render(request, 'materials/material_form.html', {'form': form})


@staff_member_required
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('materials:material_list')
    return render(request, 'materials/material_confirm_delete.html', {'material': material})
