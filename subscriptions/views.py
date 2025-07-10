from django.shortcuts import render, get_object_or_404
from .models import Subscription, RelatorioMensal
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect



class SubscriptionListView(ListView):
    model = Subscription
    template_name = "subscriptions/subscription_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        subscriptions = self.get_queryset()
        context["total_subscriptions"] = subscriptions.count()
        context["total_valor_mensal"] = subscriptions.aggregate(total=Sum("valorMens"))["total"] or 0
        
        hoje = datetime.today().date()
        data_limite = hoje + timedelta(days=5)
        context["proximos_vencimentos"] = subscriptions.filter(
            data_venc__range=(hoje, data_limite)
        ).count()

        return context
    
    def post(self, request, *args, **kwargs):
        nome = request.POST.get("nomeAssi")
        empresa = request.POST.get("empresa")
        valor = request.POST.get("valorMens")
        categoria = request.POST.get("categoria")
        metPagar = request.POST.get("metPagar")
        data_venc = request.POST.get("data_venc")

        Subscription.objects.create(
            nomeAssi=nome,
            empresa=empresa,
            valorMens=valor,
            categoria=categoria,
            metPagar=metPagar,
            data_venc=data_venc
        )

        return redirect("assinaturas")

class SubscriptionCreateView(CreateView):
    model = Subscription
    fields = ["nomeAssi", "empresa", "data_venc", "categoria", "metPagar", "valorMens"]
    success_url = reverse_lazy("assinaturas")
    
class SubscriptionUpdateView(UpdateView):
    model = Subscription
    fields = ["nomeAssi", "empresa", "data_venc", "categoria", "metPagar", "valorMens"]
    success_url = reverse_lazy("assinaturas")
    
    

def lembretes(request):
    return render(
        request,
        "subscriptions/lembretes.html",
    )

def relatorios(request):
    return render(
        request,
        "subscriptions/relatorios.html",
    )


def pagamentos(request):
    return render(
        request,
        "subscriptions/pagamentos.html",
    )


@login_required
def perfil(request):
    return render(
        request,
        "subscriptions/perfil.html",
    )



