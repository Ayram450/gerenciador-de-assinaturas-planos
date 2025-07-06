from django.shortcuts import render
from .models import Subscription
from django.contrib.auth.decorators import login_required





def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, "subscriptions/subscription_list.html", {"subscriptions": subscriptions})

def lembretes(request):
    return render(request, "subscriptions/lembretes.html", )

def relatorios(request):
    return render(request, "subscriptions/relatorios.html", )

def pagamentos(request):
    return render(request, "subscriptions/pagamentos.html", )

@login_required
def perfil(request):
    return render(request, "subscriptions/perfil.html", )


