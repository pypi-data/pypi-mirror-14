# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Pesquisa, L2, L3
from forms import PesquisaAdminForm


class PesquisaAdmin(admin.ModelAdmin):
    """
    Filtra os dados pelo estado.
    Realiza busca por: 'sigla' e 'nome' da entidade, 'sigla' e 'nome' da natureza de gasto,
                    'ano' e 'número' do processo do termo, 'referente', 'número', 'tipo' e 'descrição' do protocolo,
                    'valor' da despesa (formato 9.99)
    """
    form = PesquisaAdminForm

    fieldsets = (
                (u'Localização', {
                    'fields': (('rede', 'laboratorio'), 'endereco', 'cidade', 'instituicao'),
                    'classes': ('wide',)
                 }),
                (u'Responsáveis', {
                    'fields': (('responsavel1', 'emailresp1'), ('responsavel2', 'emailresp2')),
                    'classes': ('wide',)
                 }),
                (u'Contatos', {
                    'fields': (('contato1', 'emailcontato1', 'telefone1'),
                               ('contato2', 'emailcontato2', 'telefone2')),
                    'classes': ('wide',)
                 }),
                (u'Equipamentos', {
                    'fields': ('estado_equipamento', 'equipamento', ('fabricante', 'modelo'),
                               ('cobre', 'otica'), ('l2', 'l2_outro'), ('l3', 'l3_outro')),
                    'classes': ('wide',)
                 }),
                (u'Observação', {
                    'fields': ('obs',),
                    'classes': ('wide',)
                 }),
    )

    list_display = ('rede', 'format_lab', 'responsavel1', 'format_contato', 'equipamento', 'format_estado', 'fabricante', 'modelo')

    list_display_links = ('format_lab', )
#     list_filter = ('estado', )
#
#     list_per_page = 10
#
#     search_fields = ('protocolo__identificacao__entidade__sigla', 'protocolo__identificacao__entidade__nome',
#                      'item_pedido__natureza_gasto__modalidade__sigla', 'item_pedido__natureza_gasto__modalidade__nome',
#                      'protocolo__termo__ano', 'protocolo__termo__processo', 'protocolo__num_documento',
#                      'protocolo__tipo_documento__nome', 'protocolo__descricao', 'valor_despesa', 'referente')
#
#     muda_estado = 0
#
#     # Altera o estado do Protocolo para 'Concluído' quando a despesa for classificada como 'Pago'
#     def save_model(self, request, obj, form, change):
#         try:
#             antigo = Despesa.objects.get(pk=obj.pk)
#             estado_anterior = antigo.estado
#         except Despesa.DoesNotExist:
#             estado_anterior = None
#
#         obj.save()
#
#         if obj.estado != estado_anterior:
#             self.muda_estado = 1
#
#         if obj.estado != estado_anterior and obj.estado.nome == u'Pago':
#             e, created = models.Estado.objects.get_or_create(nome=u'Concluído')
#
#             obj.protocolo.estado = e
#             obj.protocolo.save()
#
#     def response_change(self, request, obj):
#         if self.muda_estado:
#             self.muda_estado = 0
#             if obj.estado.nome == u'Pago':
#                 super(DespesaAdmin,self).response_change(request, obj)
#                 url = '/admin/financeiro/presta_conta/add/?despesa=%s&valor=%s&estado=%s' % (obj.id, obj.valor_despesa, obj.estado.id)
#                 return HttpResponseRedirect(url)
#
#         return super(DespesaAdmin,self).response_change(request, obj)
#
#     def response_add(self, request, obj, post_url_continue='../%s/'):
#         if self.muda_estado:
#             self.muda_estado = 0
#             if obj.estado.nome == u'Pago':
#                 super(DespesaAdmin,self).response_add(request, obj)
#                 url = '/admin/financeiro/presta_conta/add/?despesa=%s&valor=%s&estado=%s' % (obj.id, obj.valor_despesa, obj.estado.id)
#                 return HttpResponseRedirect(url)
#
#         return super(DespesaAdmin,self).response_add(request, obj)

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        r1 = super(PesquisaAdmin, self).has_change_permission(request, obj)
        if not obj:
            return r1

        r2 = (obj.usuario == request.user)
        r3 = request.user.is_superuser

        return (r1 and (r2 or r3))

admin.site.register(Pesquisa, PesquisaAdmin)
admin.site.register(L2)
admin.site.register(L3)
