from django.contrib import admin
from django.urls import path
from django.urls import include

from subscriptions.views import  (SubscriptionListView, SubscriptionCreateView,
SubscriptionUpdateView, SubscriptionDeleteView,
SubscriptionCompleteView,
)
from subscriptions.views import lembretes
from subscriptions.views import relatorios
from subscriptions.views import pagamentos_view
from subscriptions.views import perfil
from base.views import homepage
from base.views import recursos
from base.views import sobre
from accounts.views import redirecionar_apos_login, administrador_view





urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("assinaturas/", SubscriptionListView.as_view(), name="assinaturas"),
    path("assinaturas/cr", SubscriptionCreateView.as_view(), name='criar_assinatura'),
    path("assinaturas/ed<int:pk>/", SubscriptionUpdateView.as_view(), name="editar_assinatura"),
    path("assinaturas/ex<int:pk>/", SubscriptionDeleteView.as_view(), name="excluir_assinatura"),
    path("complete/<int:pk>", SubscriptionCompleteView.as_view(), name="subscription_complete"),
    path("lembretes/", lembretes, name="lembretes"),
    path("relatorios/", relatorios, name="relatorios"),
    path("pagamentos/", pagamentos_view, name="pagamentos"),
    path("", homepage, name="homepage"),
    path("recursos/", recursos, name="recursos"),
    path("sobre/", sobre, name="sobre"),
    path("perfil/", perfil, name="perfil"),
    path('admin-dashboard/', administrador_view, name='admin_dash'),
    path('redirecionar/', redirecionar_apos_login, name='redirecionar_apos_login'),
  
    
    
]
