# -*- coding: utf-8 -*-
# from ..models import MyObjects
#
# from django.db import models
# from jsonfield import JSONField
#
#
# from repositories import custom_models
# from repositories.faturamento.models import Colecao, Plano
#
# class Contrato(models.Model):
#
# id = models.AutoField(db_column="contrato_id", primary_key=True)
#     id = custom_models.BigAutoField(db_column="contrato_id", primary_key=True)
#     nome = models.CharField(db_column="contrato_nome", max_length=255)
#     ativo = models.BooleanField(db_column="contrato_ativo", default=True)
#     codigo = models.CharField(db_column="contrato_codigo", max_length=255, unique=True)
#     dominio = models.CharField(db_column="contrato_dominio", max_length=255)
#     url_institucional = models.CharField(db_column="contrato_url_institucional", max_length=255)
#     parametros = JSONField(u'Parametros do contrato', db_column="contrato_parametros", null=True)
#     tipo = models.CharField(db_column="contrato_tipo", max_length=32)
#
#     data_inicio = models.DateField(db_column='contrato_data_inicio')
#     dia_vencimento = models.IntegerField(default=None, null=True, db_column='contrato_dia_vencimento', blank=True)
#
#     minimo_mensal_valor = models.DecimalField(db_column="contrato_minimo_mensal_valor", max_digits=16, decimal_places=2, null=0.00)
#     minimo_mensal_inicio_em_meses = models.IntegerField(db_column="contrato_minimo_mensal_inicio_em_meses", null=True, default=0)
#
#     razao_social = models.CharField(db_column="contrato_razao_social", max_length=255)
#     tipo_pessoa = models.CharField(db_column="contrato_tipo_pessoa", max_length=2, null=True, default='PJ')
#     cpf_cnpj = models.CharField(db_column="contrato_cpf_cnpj", max_length=15, null=True, default=None)
#     nome_responsavel = models.CharField(db_column="contrato_nome_responsavel", max_length=128, null=True, default=None)
#     email_nota_fiscal = models.CharField(db_column="contrato_email_nota_fiscal", max_length=128, null=True, default=None)
#     telefone_principal = models.CharField(db_column="contrato_telefone_principal", max_length=11, null=True, default=None)
#     telefone_celular = models.CharField(db_column="contrato_telefone_celular", max_length=11, null=True, default=None)
#     endereco_logradouro = models.CharField(db_column="contrato_endereco_logradouro", max_length=128, null=True, default=None)
#     endereco_numero = models.CharField(db_column="contrato_endereco_numero", max_length=32, null=True, default=None)
#     endereco_complemento = models.CharField(db_column="contrato_endereco_complemento", max_length=128, null=True, default=None)
#     endereco_bairro = models.CharField(db_column="contrato_endereco_bairro", max_length=50, null=True, default=None)
#     endereco_cep = models.CharField(db_column="contrato_endereco_cep", max_length=8, null=True, default=None)
#     endereco_cidade_ibge = models.IntegerField(db_column="contrato_endereco_cidade_ibge", null=True, default=None)
#     endereco_estado = models.CharField(u'Estado', db_column="contrato_endereco_estado", max_length=2, null=True, default=None)
#
#     url_termo = models.TextField(db_column="contrato_url_termo", null=True, default=None)
#     headtags = models.TextField(db_column="contrato_headtags", null=True, default=None)
#
#     chave = models.CharField(db_column="contrato_chave", max_length=32)
#
#     objects = MyObjects()
#
#     colecao = models.ForeignKey('faturamento.Colecao', db_column="colecao_id")
#
# def __str__(self):              # __unicode__ on Python 2
#         return "%s the restaurant" % self.dominio
#
#     class Meta:
# app_label = 'repositories_plataforma'
#         db_table = u"plataforma\".\"tb_contrato"
#
#
# class Conta(models.Model):
#
#     CONTA_SITUACOES = [
#         ('ATIVA', 'Loja ATIVA'),
#         ('BLOQUEADA', 'Loja BLOQUEADA'),
#         ('CANCELADA', 'Loja CANCELADA')
#     ]
#
# id = models.AutoField(db_column="conta_id", primary_key=True)
#     id = custom_models.BigAutoField(db_column="conta_id", primary_key=True)
#     apelido = models.CharField(db_column="conta_apelido", max_length=32)
#     nome = models.CharField(db_column="conta_loja_nome", max_length=128, null=False)
#     email = models.CharField(db_column="conta_loja_email", max_length=128, null=True, default=None)
#     dominio = models.CharField(db_column="conta_loja_dominio", max_length=128, null=True, default=None)
#     situacao = models.CharField(db_column="conta_situacao", max_length=32, null=False, default='ATIVA', choices=CONTA_SITUACOES)
#     modo = models.CharField(db_column="conta_loja_modo", max_length=32, null=False, default="loja")
#     verificada = models.BooleanField(db_column="conta_verificada", default=False)
#
#     logo = models.CharField(db_column="conta_logo", max_length=128, null=True, default=None)
#     telefone = models.CharField(db_column="conta_loja_telefone", max_length=20, null=True, default=None)
#     facebook = models.CharField(db_column="conta_loja_facebook", max_length=128, null=True, default=None)
#     google_plus = models.CharField(db_column="conta_loja_google_plus", max_length=128, null=True, default=None)
#     twitter = models.CharField(db_column="conta_loja_twitter", max_length=128, null=True, default=None)
#     youtube = models.CharField(db_column="conta_loja_youtube", max_length=128, null=True, default=None)
#     instagram = models.CharField(db_column="conta_loja_instagram", max_length=128, null=True, default=None)
#     pinterest = models.CharField(db_column="conta_loja_pinterest", max_length=128, null=True, default=None)
#     blog = models.URLField(db_column="conta_loja_blog", max_length=256, null=True)
#     whatsapp = models.CharField(db_column="conta_loja_whatsapp", max_length=20, null=True, default=None)
#     skype = models.CharField(db_column='conta_loja_skype', max_length=64, null=True, default=None)
#     endereco = models.CharField(db_column="conta_loja_endereco", max_length=128, null=True, default=None)
#
#     loja_manutencao = models.BooleanField(db_column="conta_loja_manutencao", default=False)
#
#     habilitar_facebook = models.BooleanField(db_column='conta_habilitar_facebook', default=False)
#     habilitar_mercadolivre = models.BooleanField(db_column='conta_habilitar_mercadolivre', default=False)
#     habilitar_mobile = models.BooleanField(db_column='conta_habilitar_mobile', default=True)
#
#     data_criacao = models.DateTimeField(db_column="conta_data_criacao", auto_now_add=True)
#     data_modificacao = models.DateTimeField(db_column="conta_data_modificacao", auto_now=True, null=True)
#     data_cancelamento = models.DateTimeField(db_column="conta_data_cancelamento", null=True)
#
#     objects = MyObjects()
#
#     contrato = models.ForeignKey(Contrato, db_column="contrato_id")
#     plano = models.ForeignKey('faturamento.Plano', db_column="plano_id")
#
#     class Meta:
# app_label = 'repositories_plataforma'
#         db_table = u"plataforma\".\"tb_conta"
#
#     @property
#     def url_dominio(self):
#         if self.dominio:
#             return self.dominio
#         else:
#             return self.url_subdominio
#
#     @property
#     def url_subdominio_facebook(self):
#         return "%s-facebook.%s" % (self.apelido, self.contrato.dominio)
#
#     @property
#     def url_subdominio(self):
#         return "%s.%s" % (self.apelido, self.contrato.dominio)
#
#     @property
#     def email_contato(self):
#         if self.email:
#             return self.email
#         try:
#             return self.usuarios.all()[0].email
#         except IndexError:
#             return None
