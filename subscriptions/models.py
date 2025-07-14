from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    METODO_PAGAMENTO_CHOICES = [
        ("debito", "Débito"),
        ("credito", "Crédito"),
        ("boleto", "Boleto"),
        ("pix", "Pix"),
    ]
    CATEGORIA_CHOICES = [
        ("entretenimento", "Entretenimento"),
        ("musica", "Música"),
        ("jogos", "Jogos"),
        ("educacao", "Educação"),
        ("produtividade", "Produtividade"),
        ("design", "Design / Criativo"),
        ("financeiro", "Financeiro"),
        ("alimentacao", "Alimentação"),
        ("saude", "Saúde"),
        ("transporte", "Transporte"),
        ("casa", "Casa e Serviços"),
        ("pets", "Pets"),
        ("compras", "Compras / Delivery"),
        ("internet", "Internet / Dados"),
        ("softwares", "Softwares / Apps"),
        ("beleza", "Beleza e Estética"),
        ("bem-estar", "Bem-estar"),
        ("comunicacao", "Comunicação"),
        ("outros", "Outros"),
    ]
    
    STATUS_PAGAMENTO = [
            ("pendente", "Pendente"),
            ("pago", "Pago"),
            ("atrasado", "Atrasado"),
        ]
    
    nomeAssi = models.CharField(max_length=100, null=False, blank=False)
    empresa = models.CharField(max_length=100, null=False, blank=False)
    data_venc = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_PAGAMENTO, default="pendente")
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        null=False,
        blank=False,
        default="debito",
    )
    metPagar = models.CharField(
        max_length=50,
        choices=METODO_PAGAMENTO_CHOICES,
        null=False,
        blank=False,
        default="entretenimento",
    )
    valorMens = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    data_pagamento = models.DateField(null=True, blank=True)
    def verificar_status(self):
            if self.status == 'pendente' and self.data_venc < timezone.now().date():
                self.status = 'atrasado'
                self.save()


class RelatorioMensal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    mes = models.IntegerField()
    ano = models.IntegerField()
    total_assinaturas = models.IntegerField()
    total_valor_mensal = models.DecimalField(max_digits=10, decimal_places=2)

    assinaturas_pagas = models.IntegerField(default=0)
    valor_pagas = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    assinaturas_pendentes = models.IntegerField(default=0)
    valor_pendentes = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    assinaturas_atrasadas = models.IntegerField(default=0)
    valor_atrasadas = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    proximos_vencimentos = models.IntegerField(default=0)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'mes', 'ano')
        ordering = ['-ano', '-mes']

    def __str__(self):
        return f"Relatório {self.mes:02d}/{self.ano}"
    
    
class AssinaturaRelatorio(models.Model):
    relatorio = models.ForeignKey(RelatorioMensal, on_delete=models.CASCADE, related_name='assinaturas')

    nomeAssi = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    data_venc = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ("pendente", "Pendente"),
        ("pago", "Pago"),
        ("atrasado", "Atrasado"),
    ])
    categoria = models.CharField(max_length=50, choices=[
        ("entretenimento", "Entretenimento"),
        ("musica", "Música"),
        ("jogos", "Jogos"),
        ("educacao", "Educação"),
        ("produtividade", "Produtividade"),
        ("design", "Design / Criativo"),
        ("financeiro", "Financeiro"),
        ("alimentacao", "Alimentação"),
        ("saude", "Saúde"),
        ("transporte", "Transporte"),
        ("casa", "Casa e Serviços"),
        ("pets", "Pets"),
        ("compras", "Compras / Delivery"),
        ("internet", "Internet / Dados"),
        ("softwares", "Softwares / Apps"),
        ("beleza", "Beleza e Estética"),
        ("bem-estar", "Bem-estar"),
        ("comunicacao", "Comunicação"),
        ("outros", "Outros"),
    ])
    metPagar = models.CharField(max_length=50, choices=[
        ("debito", "Débito"),
        ("credito", "Crédito"),
        ("boleto", "Boleto"),
        ("pix", "Pix"),
    ])
    valorMens = models.DecimalField(max_digits=10, decimal_places=2)