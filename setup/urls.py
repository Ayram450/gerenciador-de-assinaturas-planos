from django.contrib import admin
from django.urls import path
from django.urls import include

from subscriptions.views import subscription_list
from subscriptions.views import lembretes
from subscriptions.views import relatorios
from subscriptions.views import pagamentos
from subscriptions.views import perfil
from base.views import homepage
from base.views import recursos
from base.views import sobre




urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("assinaturas/", subscription_list, name="assinaturas"),
    path("lembretes/", lembretes, name="lembretes"),
    path("relatorios/", relatorios, name="relatorios"),
    path("pagamentos/", pagamentos, name="pagamentos"),
    path("", homepage, name="homepage"),
    path("recursos/", recursos, name="recursos"),
    path("sobre/", sobre, name="sobre"),
    path("perfil/", perfil, name="perfil"),
    
]
