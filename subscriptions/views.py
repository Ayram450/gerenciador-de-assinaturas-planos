from django.shortcuts import render, get_object_or_404
from .models import Subscription, RelatorioMensal, AssinaturaRelatorio
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from dateutil.relativedelta import relativedelta



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
        subscription_id = request.POST.get("id")
        nome = request.POST.get("nomeAssi")
        empresa = request.POST.get("empresa")
        valor = request.POST.get("valorMens")
        categoria = request.POST.get("categoria")
        metPagar = request.POST.get("metPagar")
        data_venc = request.POST.get("data_venc")

        if subscription_id:
            # Edição
            subscription = Subscription.objects.get(id=subscription_id)
            subscription.nomeAssi = nome
            subscription.empresa = empresa
            subscription.valorMens = valor
            subscription.categoria = categoria
            subscription.metPagar = metPagar
            subscription.data_venc = data_venc
            subscription.save()
        else:
            # Criação
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
    
class SubscriptionDeleteView(DeleteView):
    model = Subscription
    success_url = reverse_lazy("assinaturas")
    
    
def pagamentos_view(request):
    q = request.GET.get("q")  # texto de busca
    status = request.GET.get("status")  # filtro por status (se você tiver)

    subscriptions = Subscription.objects.all()
    
    for sub in subscriptions:
        sub.verificar_status()

    # Filtro por nome do plano ou empresa
    if q:
        subscriptions = subscriptions.filter(
            Q(nomeAssi__icontains=q) | Q(empresa__icontains=q)
        )

    # Exemplo: filtro por status, se o modelo tiver esse campo
    if status == "pending":
        subscriptions = subscriptions.filter(status="pendente")
    elif status == "completed":
        subscriptions = subscriptions.filter(status="pago")
    elif status == "failed":
        subscriptions = subscriptions.filter(status="atrasado")

    return render(request, "subscriptions/pagamentos.html", {
        "subscription_list": subscriptions
    })
 
# def concluir_pagamento(request, pk):
#     subscription = get_object_or_404(Subscription, pk=pk)

#     if subscription.status == 'pendente' or subscription.status == 'atrasado':
#         # Atualiza status
#         subscription.status = 'pago'
#         subscription.save()

#         # Gera nova mensalidade para o próximo mês
#         nova_data = subscription.data_venc + timedelta(days=30)
#         Subscription.objects.create(
#             nomeAssi=subscription.nomeAssi,
#             empresa=subscription.empresa,
#             valorMens=subscription.valorMens,
#             data_venc=nova_data,
#             categoria=subscription.categoria,
#             metPagar=subscription.metPagar,
#             status='pendente'
#         )

#     return redirect('pagamentos')
    
class SubscriptionCompleteView(View): 
    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)

        if subscription.status in ['pendente', 'atrasado']:
            subscription.status = 'pago'
            subscription.save()

            # Define a nova data de vencimento (mês seguinte)
            nova_data = subscription.data_venc + relativedelta(months=1)

            # Verifica se já existe uma assinatura futura com essa data
            existe_futura = Subscription.objects.filter(
                nomeAssi=subscription.nomeAssi,
                empresa=subscription.empresa,
                data_venc=nova_data
            ).exists()

            # Só cria se ainda não existir
            if not existe_futura:
                Subscription.objects.create(
                    nomeAssi=subscription.nomeAssi,
                    empresa=subscription.empresa,
                    valorMens=subscription.valorMens,
                    data_venc=nova_data,
                    categoria=subscription.categoria,
                    metPagar=subscription.metPagar,
                    status='pendente'
                )

        return redirect('pagamentos')
        

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


 # def pagamentos(request):
#    return render(
 #       request,
  #      "subscriptions/pagamentos.html",
   # )


@login_required
def perfil(request):
    return render(
        request,
        "subscriptions/perfil.html",
    )

def gerar_relatorio_do_mes(mes, ano):
    assinaturas = Subscription.objects.filter(data_venc__month=mes, data_venc__year=ano)

    total_assinaturas = assinaturas.count()
    total_valor = assinaturas.aggregate(total=Sum('valorMens'))['total'] or 0

    pagas = assinaturas.filter(status='pago')
    pendentes = assinaturas.filter(status='pendente')
    atrasadas = assinaturas.filter(status='atrasado')

    relatorio, created = RelatorioMensal.objects.update_or_create(
        mes=mes,
        ano=ano,
        defaults={
            'total_assinaturas': total_assinaturas,
            'total_valor_mensal': total_valor,
            'assinaturas_pagas': pagas.count(),
            'valor_pagas': pagas.aggregate(total=Sum('valorMens'))['total'] or 0,
            'assinaturas_pendentes': pendentes.count(),
            'valor_pendentes': pendentes.aggregate(total=Sum('valorMens'))['total'] or 0,
            'assinaturas_atrasadas': atrasadas.count(),
            'valor_atrasadas': atrasadas.aggregate(total=Sum('valorMens'))['total'] or 0,
            'proximos_vencimentos': Subscription.objects.filter(data_venc__gt=timezone.now().date()).count()
        }
    )

    # Limpa registros anteriores se relatório foi recriado
    if not created:
        relatorio.assinaturas.all().delete()

    # Cópia das assinaturas no momento do relatório
    for sub in assinaturas:
        AssinaturaRelatorio.objects.create(
            relatorio=relatorio,
            nomeAssi=sub.nomeAssi,
            empresa=sub.empresa,
            data_venc=sub.data_venc,
            status=sub.status,
            categoria=sub.categoria,
            metPagar=sub.metPagar,
            valorMens=sub.valorMens
        )

    return relatorio

