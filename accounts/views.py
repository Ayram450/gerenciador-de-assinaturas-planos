from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from django.utils import timezone
from subscriptions.models import Subscription
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.views.generic.detail import DetailView


User = get_user_model()


@staff_member_required
def administrador_view(request):
    hoje = timezone.now().date()
    data_limite = hoje + timedelta(days=5)

    # Métricas globais
    total_usuarios = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_assinaturas = Subscription.objects.filter(
        status__in=["pendente", "atrasado"]
    ).count()
    total_valor_mensal = (
        Subscription.objects.aggregate(total=Sum("valorMens"))["total"] or 0
    )
    proximos_vencimentos = Subscription.objects.filter(
        data_venc__range=(hoje, data_limite)
    ).count()
    pagamentos_atrasados = Subscription.objects.filter(status="atrasado").count()

    receita_total_mes = (
        Subscription.objects.filter(
            status="pago", data_venc__month=hoje.month, data_venc__year=hoje.year
        ).aggregate(total=Sum("valorMens"))["total"]
        or 0
    )

    # Lista de usuários com contagem de assinaturas
    usuarios_info = (
        User.objects
        .filter(is_staff=False, is_superuser=False)
        .exclude(id__isnull=True)
        .annotate(qtd_assinaturas=Count("subscription"))
        .values("id", "username", "email", "date_joined", "qtd_assinaturas")
    )

    return render(
        request,
        "accounts/admin_dash.html",
        {
            "total_usuarios": total_usuarios,
            "total_assinaturas": total_assinaturas,
            "total_valor_mensal": total_valor_mensal,
            "proximos_vencimentos": proximos_vencimentos,
            "pagamentos_atrasados": pagamentos_atrasados,
            "receita_total_mes": receita_total_mes,
            "usuarios_info": usuarios_info,  # <== novo contexto
        },
    )

@login_required
def redirecionar_apos_login(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect("admin_dash")
    else:
        return redirect("perfil")

@method_decorator(staff_member_required, name='dispatch')
class ExcluirUsuarioView(View):
    def post(self, request, user_id):
        usuario = get_object_or_404(User, id=user_id)

        # Protege contra exclusão de admin
        if usuario.is_staff or usuario.is_superuser:
            return redirect("admin_dash")  

        usuario.delete()
        return redirect("admin_dash")
    
@method_decorator(staff_member_required, name='dispatch')
class DadosUsuarioView(DetailView):
    model = User
    template_name = "accounts/dados_usuario.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.get_object()
        context["assinaturas"] = Subscription.objects.filter(user=usuario)
        return context

