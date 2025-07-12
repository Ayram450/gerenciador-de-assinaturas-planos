from django.shortcuts import render, get_object_or_404
from subscriptions.notifications.email_gmail import send_gmail
from django.template.loader import render_to_string
from .models import Subscription, RelatorioMensal, AssinaturaRelatorio
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Sum, Min, Max
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class SubscriptionListView(ListView):
    model = Subscription
    template_name = "subscriptions/subscription_list.html"

    def get_queryset(self):
        # Exclui assinaturas que já foram pagas
        return Subscription.objects.filter(user=self.request.user).exclude(
            status="pago"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subscriptions = self.get_queryset()
        context["total_subscriptions"] = subscriptions.count()
        context["total_valor_mensal"] = (
            subscriptions.aggregate(total=Sum("valorMens"))["total"] or 0
        )

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
            subscription = Subscription.objects.get(
                id=subscription_id, user=request.user
            )
            subscription.nomeAssi = nome
            subscription.empresa = empresa
            subscription.valorMens = valor
            subscription.categoria = categoria
            subscription.metPagar = metPagar
            subscription.data_venc = data_venc
            subscription.save()
        else:
            # Criação
            nova = Subscription.objects.create(
                user=request.user,
                nomeAssi=nome,
                empresa=empresa,
                valorMens=valor,
                categoria=categoria,
                metPagar=metPagar,
                data_venc=data_venc,
            )

            #  Envia o e-mail informando que o lembrete será enviado
            html_body = render_to_string(
                "subscriptions/email_body.html",
                {
                    "username": request.user.username,
                    "nome": nome,
                    "empresa": empresa,
                    "valor": valor,
                    "categoria": categoria,
                    "metPagar": metPagar,
                    "data_venc": data_venc,
                },
            )

            send_gmail(
                to_email=request.user.email,
                subject="Assinatura Criada com Sucesso",
                message_text="Sua assinatura foi criada com sucesso.",  # Texto simples de fallback
                html_content=html_body,
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

    def get_queryset(self):
        # Garante que só veja/edite suas próprias assinaturas
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionDeleteView(DeleteView):
    model = Subscription
    success_url = reverse_lazy("assinaturas")

    def get_queryset(self):
        # Garante que só exclua suas próprias assinaturas
        return Subscription.objects.filter(user=self.request.user)


def pagamentos_view(request):
    q = request.GET.get("q")  # texto de busca
    status = request.GET.get("status")  # filtro por status

    # Busca todas as assinaturas
    subscriptions = Subscription.objects.filter(user=request.user)

    # Atualiza o status atrasado automaticamente
    for sub in subscriptions:
        if sub.status == "pendente" and sub.data_venc < timezone.now().date():
            sub.status = "atrasado"
            sub.save()

    # Aplica filtros de texto
    if q:
        subscriptions = subscriptions.filter(
            Q(nomeAssi__icontains=q) | Q(empresa__icontains=q)
        )

    # Filtro por status (se fornecido)
    if status == "pending":
        subscriptions = subscriptions.filter(status="pendente")
    elif status == "completed":
        subscriptions = subscriptions.filter(status="pago")
    elif status == "failed":
        subscriptions = subscriptions.filter(status="atrasado")

    # Estatísticas (independentes dos filtros aplicados)
    all_subs = Subscription.objects.filter(user=request.user)
    pagos = all_subs.filter(status="pago").count()
    pendentes = all_subs.filter(status="pendente").count()
    atrasados = all_subs.filter(status="atrasado").count()

    hoje = timezone.now().date()
    total_pago_mes = (
        all_subs.filter(
            status="pago",
            data_pagamento__year=hoje.year,
            data_pagamento__month=hoje.month,
        ).aggregate(total=Sum("valorMens"))["total"]
        or 0
    )

    return render(
        request,
        "subscriptions/pagamentos.html",
        {
            "subscription_list": subscriptions,
            "pagos": pagos,
            "pendentes": pendentes,
            "atrasados": atrasados,
            "total_pago_mes": total_pago_mes,
        },
    )


class SubscriptionCompleteView(View):
    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk, user=request.user)

        if subscription.status in ["pendente", "atrasado"]:
            subscription.status = "pago"
            if not subscription.data_pagamento:
                subscription.data_pagamento = timezone.now().date()
            subscription.save()

            # Define a nova data de vencimento (mês seguinte)
            nova_data = subscription.data_venc + relativedelta(months=1)

            # Verifica se já existe uma assinatura futura com essa data
            existe_futura = Subscription.objects.filter(
                nomeAssi=subscription.nomeAssi,
                empresa=subscription.empresa,
                data_venc=nova_data,
            ).exists()

            # Só cria se ainda não existir
            if not existe_futura:
                Subscription.objects.create(
                    user=request.user,
                    nomeAssi=subscription.nomeAssi,
                    empresa=subscription.empresa,
                    valorMens=subscription.valorMens,
                    data_venc=nova_data,
                    categoria=subscription.categoria,
                    metPagar=subscription.metPagar,
                    status="pendente",
                )

        return redirect("pagamentos")


@login_required
def lembretes(request):
    hoje = timezone.now().date()
    user = request.user

    # Filtra apenas assinaturas ativas (pendentes ou atrasadas)
    assinaturas_ativas = Subscription.objects.filter(
        user=user, status__in=["pendente", "atrasado"]
    )

    # Adiciona dinamicamente o campo "dias_restantes" a cada assinatura
    for sub in assinaturas_ativas:
        sub.dias_restantes = (sub.data_venc - hoje).days

    # 1. Lembretes Ativos
    total_ativos = assinaturas_ativas.count()

    # 2. Vencimento Atrasado: data mais antiga com status atrasado
    vencimento_atrasado = (
        assinaturas_ativas.filter(status="atrasado").order_by("data_venc").first()
    )
    data_atrasada = vencimento_atrasado.data_venc if vencimento_atrasado else None

    # 3. Vencimento Próximo: data mais próxima com status pendente
    vencimento_proximo = (
        assinaturas_ativas.filter(status="pendente", data_venc__gte=hoje)
        .order_by("data_venc")
        .first()
    )
    data_proxima = vencimento_proximo.data_venc if vencimento_proximo else None

    # 4. Total a Pagar: valor da assinatura mais próxima com status pendente
    valor_a_pagar = vencimento_proximo.valorMens if vencimento_proximo else 0

    return render(
        request,
        "subscriptions/lembretes.html",
        {
            "total_ativos": total_ativos,
            "data_atrasada": data_atrasada,
            "data_proxima": data_proxima,
            "valor_a_pagar": valor_a_pagar,
            "subscription_list": assinaturas_ativas,  # Adiciona a lista para exibir no HTML
        },
    )


def relatorios(request):
    return render(
        request,
        "subscriptions/relatorios.html",
    )


@login_required
def perfil(request):
    user = request.user
    perfil, _ = Profile.objects.get_or_create(user=user)

    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ["telefone", "data_nascimento"]
            widgets = {
                "telefone": forms.TextInput(
                    attrs={
                        "class": "w-full px-3 py-2 border border-gray-300 rounded-md"
                    }
                ),
                "data_nascimento": forms.DateInput(
                    attrs={
                        "type": "date",
                        "class": "w-full px-3 py-2 border border-gray-300 rounded-md",
                    },
                    format="%Y-%m-%d",
                ),
            }

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = ProfileForm(instance=perfil)

    return render(request, "subscriptions/perfil.html", {"user": user, "form": form})


def gerar_relatorio_do_mes(mes, ano, request):
    assinaturas = Subscription.objects.filter(
        data_venc__month=mes, data_venc__year=ano, user=request.user
    )

    total_assinaturas = assinaturas.count()
    total_valor = assinaturas.aggregate(total=Sum("valorMens"))["total"] or 0

    pagas = assinaturas.filter(status="pago")
    pendentes = assinaturas.filter(status="pendente")
    atrasadas = assinaturas.filter(status="atrasado")

    relatorio, created = RelatorioMensal.objects.update_or_create(
        mes=mes,
        ano=ano,
        defaults={
            "total_assinaturas": total_assinaturas,
            "total_valor_mensal": total_valor,
            "assinaturas_pagas": pagas.count(),
            "valor_pagas": pagas.aggregate(total=Sum("valorMens"))["total"] or 0,
            "assinaturas_pendentes": pendentes.count(),
            "valor_pendentes": pendentes.aggregate(total=Sum("valorMens"))["total"]
            or 0,
            "assinaturas_atrasadas": atrasadas.count(),
            "valor_atrasadas": atrasadas.aggregate(total=Sum("valorMens"))["total"]
            or 0,
            "proximos_vencimentos": Subscription.objects.filter(
                data_venc__gt=timezone.now().date()
            ).count(),
        },
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
            valorMens=sub.valorMens,
        )

    return relatorio
