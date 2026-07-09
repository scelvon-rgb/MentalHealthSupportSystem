from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Resource
from .forms import ResourceForm


@login_required
def resource_list(request):

    search = request.GET.get("search")

    resources = Resource.objects.all().order_by("-created_at")

    if search:
        resources = resources.filter(
            title__icontains=search
        )

    role = request.user.userprofile.role.role_name

    is_admin = role in ["Admin", "Administrator"]

    return render(
        request,
        "resources/resource_list.html",
        {
            "resources": resources,
            "is_admin": is_admin,
            "search": search,
        }
    )


@login_required
def resource_detail(request, resource_id):

    resource = get_object_or_404(
        Resource,
        id=resource_id
    )

    role = request.user.userprofile.role.role_name

    is_admin = role in ["Admin", "Administrator"]

    return render(
        request,
        "resources/resource_detail.html",
        {
            "resource": resource,
            "is_admin": is_admin,
        }
    )


@login_required
def add_resource(request):

    role = request.user.userprofile.role.role_name

    if role not in ["Admin", "Administrator"]:
        return redirect("dashboard")

    if request.method == "POST":

        form = ResourceForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("resource_list")

    else:

        form = ResourceForm()

    return render(
        request,
        "resources/add_resource.html",
        {
            "form": form
        }
    )


@login_required
def edit_resource(request, resource_id):

    role = request.user.userprofile.role.role_name

    if role not in ["Admin", "Administrator"]:
        return redirect("dashboard")

    resource = get_object_or_404(
        Resource,
        id=resource_id
    )

    if request.method == "POST":

        form = ResourceForm(
            request.POST,
            request.FILES,
            instance=resource
        )

        if form.is_valid():

            form.save()

            return redirect(
                "resource_detail",
                resource_id=resource.id
            )

    else:

        form = ResourceForm(
            instance=resource
        )

    return render(
        request,
        "resources/edit_resource.html",
        {
            "form": form,
            "resource": resource
        }
    )


@login_required
def delete_resource(request, resource_id):

    role = request.user.userprofile.role.role_name

    if role not in ["Admin", "Administrator"]:
        return redirect("dashboard")

    resource = get_object_or_404(
        Resource,
        id=resource_id
    )

    resource.delete()

    return redirect("resource_list")