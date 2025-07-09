from django.db import models


class Subscription(models.Model):
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
    nomeAssi = models.CharField(max_length=100, null=False, blank=False)
    empresa = models.CharField(max_length=100, null=False, blank=False)
    data_venc = models.DateField(null=False, blank=False)
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


class RelatorioMensal(models.Model):
    mes = models.IntegerField()  # 1 a 12
    ano = models.IntegerField()
    total_assinaturas = models.IntegerField()
    total_valor_mensal = models.DecimalField(max_digits=10, decimal_places=2)
    proximos_vencimentos = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mes', 'ano')
        ordering = ['-ano', '-mes']

    def __str__(self):
        return f"Relatório {self.mes:02d}/{self.ano}"