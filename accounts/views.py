from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def administrador_view(request):
    return render(request, "accounts/admin_dash.html")  

@login_required
def redirecionar_apos_login(request):
    if request.user.is_superuser:
        return redirect('admin_dash')
    return redirect('perfil')



