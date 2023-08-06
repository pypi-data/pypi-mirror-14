# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
import re
import logging

from identificacao.models import EnderecoDetalhe
from utils.models import NARADateField

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Estado(models.Model):

    # Declaração de variáveis estáticas
    PATRIMONIO_ATIVO = 22
    """
    Uma instância dessa classe representa um estado do patrimônio ou do equipamento.
    Exemplo de estado do Patrimônio: Emprestado, Mautenção, Doado, ...
    Exemplo de estado do Equipamento: Defeito, Obsoleto, Ativo, ...

    O método '__unicode__'	Retorna o nome.
    A class 'Meta'		Define a ordem de apresentação dos dados pelo nome.

    >>> e, created = Estado.objects.get_or_create(nome='Doado')

    >>> e.__unicode__()
    u'Doado'
    """
    nome = models.CharField(_(u'Nome'), max_length=30, help_text=_(u'ex. Doado'), unique=True)

    # Retorna o nome
    def __unicode__(self):
        return u'%s' % self.nome

    # Define a ordenação dos dados pelo nome
    class Meta:
        ordering = ("nome", )


class Tipo(models.Model):

    # Declaração de variáveis estáticas
    CONSIGNADO = 23
    """
    Uma instância dessa classe é um tipo de licença (ex. Free).

    O método '__unicode__'	Retorna o nome.
    A class 'Meta'		Define a ordem de apresentação dos dados pelo nome.

    >>> t, created = Tipo.objects.get_or_create(nome='Free')

    >>> t.__unicode__()
    u'Free'
    """
    nome = models.CharField(_(u'Nome'), max_length=30, help_text=_(u'ex. Open Source'), unique=True)

    # Retorna o nome
    def __unicode__(self):
        return u'%s' % self.nome

    # Define a ordenação dos dados pelo nome
    class Meta:
        ordering = ("nome", )


class Patrimonio(models.Model):

    U_TO_PX = 19
    U_TO_PT = 15.0
    U_TO_EM = 2.0
    """
    Uma instância dessa classe representa um item do patrimônio.

    """
    patrimonio = models.ForeignKey('patrimonio.Patrimonio', null=True, blank=True, verbose_name=_(u'Contido em'),
                                   related_name='contido')
    pagamento = models.ForeignKey('financeiro.Pagamento', null=True, blank=True)
    ns = models.CharField(_(u'Número de série'), null=True, blank=True, max_length=50)
    complemento = models.CharField('Compl', max_length=100, null=True, blank=True)
    valor = models.DecimalField(u'Vl unit', max_digits=12, decimal_places=2, null=True, blank=True)
    # procedencia = models.CharField(_(u'Procedência'), null=True, blank=True, max_length=100)
    obs = models.TextField(null=True, blank=True)
    agilis = models.BooleanField(_(u'Agilis?'), default=True)
    equipamento = models.ForeignKey('patrimonio.Equipamento', null=True, blank=True)
    checado = models.BooleanField(default=False)
    apelido = models.CharField(max_length=30, null=True, blank=True)
    descricao = models.TextField(_(u'Descrição NF'))
    tem_numero_fmusp = models.BooleanField('Tem nº de patrimônio oficial?', default=False)
    numero_fmusp = models.IntegerField('Nº de patrimônio oficial', null=True, blank=True)
    entidade_procedencia = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Procedência'), null=True,
                                             blank=True,
                                             help_text=u"Representa a Entidade que fornece este patrimônio.")

# Campos duplicados que existem no Model de Equipamento
    tipo = models.ForeignKey('patrimonio.Tipo')
    descricao_tecnica = models.TextField(u'Descrição técnica', null=True, blank=True)
    imagem = models.ImageField(upload_to='patrimonio', null=True, blank=True)
    isbn = models.CharField(_(u'ISBN'), null=True, blank=True, max_length=20)
    titulo_autor = models.CharField(_(u'Título e autor'), null=True, blank=True, max_length=100)
    especificacao = models.FileField(u'Especificação', upload_to='patrimonio', null=True, blank=True)
    tamanho = models.DecimalField(u'Tamanho (em U)', max_digits=5, decimal_places=2, blank=True, null=True)

    revision = models.CharField(u'Revision', null=True, blank=True, max_length=30)
    version = models.CharField(u'Version', null=True, blank=True, max_length=30)

    garantia_termino = NARADateField(_(u'Data de término da garantia'), null=True, blank=True)

    def __unicode__(self):
        if self.pagamento_id:
            return u'%s - %s  - %s - %s' % (self.pagamento.protocolo.num_documento,
                                            self.apelido, self.ns, self.descricao)
        else:
            return u'%s - %s - %s' % (self.apelido, self.ns, self.descricao)

    @property
    def procedencia(self):
        if self.entidade_procedencia_id:
            return self.entidade_procedencia.sigla
        return ''

    def save(self, *args, **kwargs):
        super(Patrimonio, self).save(*args, **kwargs)

#       ROGERIO: COMENTANDO O CODIGO DE SALVAMENTO DE HISTORICOS NO FILHO
#       DEVIDO A INCONCISTENCIA NO CASO DE UPDATE DO HISTORICO ATUAL DO PATRIMONIO

#         # fazendo a busca do historico atual, pois está em cache
#         # e esta requisição pode ter mudado este valor
#         ht = self.historicolocal_set.order_by('-data', '-id')
#         if not ht: return None
#         self_historico_atual = ht[0]

#         # Rogerio: após salvar o patrimonio, verifica se os patrimonios filhos estão
#         # no mesmo endereço e posição.
#         # Se não estiverem, cria um novo histórico de endereço para todos os filhos
#         if Patrimonio.objects.filter(patrimonio=self).exists():
#             filhos = Patrimonio.objects.filter(patrimonio=self)
#
#             for filho in filhos:
#                 # Rogerio: se não tiver endereço, não faz nada com os patrimonios filhos,
#                 # já que não podemos remover os endereços
#                 #
#                 # Também não modificamos se o filho possui um histórico com data mais atual
#                 if self_historico_atual:
#                     if not filho.historico_atual or \
#                         (self_historico_atual.endereco != filho.historico_atual.endereco) or \
#                         (self_historico_atual.posicao != filho.historico_atual.posicao) or \
#                         (self_historico_atual.data > filho.historico_atual.data):
#
#                         novoHistorico = HistoricoLocal.objects.create(memorando=self_historico_atual.memorando,
#                                                        patrimonio=filho,
#                                                        endereco=self_historico_atual.endereco,
#                                                        estado=self_historico_atual.estado,
#                                                        descricao="Movimentado junto com o patrimonio %s [%s]"%
# (self.id, self_historico_atual.descricao),
#                                                        data=self_historico_atual.data,
#                                                        posicao=self.historico_atual.posicao,
#                                                        )

    @property
    def marca(self):
        retorno = ''
        if self.equipamento and self.equipamento.entidade_fabricante and self.equipamento.entidade_fabricante.sigla:
            retorno = self.equipamento.entidade_fabricante.sigla
        return retorno

    @property
    def modelo(self):
        retorno = ''
        if self.equipamento_id:
            retorno = self.equipamento.modelo
        return retorno

    @property
    def part_number(self):
        retorno = ''
        if self.equipamento_id:
            retorno = self.equipamento.part_number
        return retorno

    @cached_property
    def historico_atual(self):
        """
        Objeto HistoricoLocal mais recente do Patrimonio.
        Se ocorrer de dois históricos estarem na mesma data, retorna o objeto com ID maior.
        """
        ht = self.historicolocal_set.order_by('-data', '-id')
        if not ht:
            return None
        return ht[0]

    @cached_property
    def historico_atual_prefetched(self):
        """
        Utilizar este método ao invés de historico_atual se for feito o prefetch_related antecipadamente.
        Em caso de dúvida, ou se não for utilizado o prefetch, utilizar o método historico_atual, pois
        o tempo de execução deste método será o dobro do normal.

        Exemplo de utilização, com prefetch_related:
            from django.db.models import Prefetch
            Patrimonio.objects.all().prefetch_related(Prefetch('historicolocal_set',
            queryset=HistoricoLocal.objects.select_related('k')))
        """
        # ht = sorted(self.historicolocal_set.all(), key=lambda x: x.id, reverse=True)
        ht = sorted(self.historicolocal_set.all(), key=lambda x: x.id, reverse=True)
        ht = sorted(ht, key=lambda x: x.data, reverse=True)

        if not ht:
            return None
        return ht[0]

    def posicao(self):
        ht = self.historico_atual
        if not ht:
            return u''
        return u'%s - %s' % (ht.endereco.complemento, ht.posicao)

    # Retorna os patrimônios de um termo.
    @classmethod
    def patrimonios_termo(cls, t):
        return cls.objects.filter(pagamento__protocolo__termo=t)

    # retorna o número do documento fiscal de compra do equipamento
    def nf(self):
        if self.pagamento is not None and self.pagamento.protocolo is not None:
            return u'%s' % self.pagamento.protocolo.num_documento
        else:
            return ''
    nf.short_description = u'NF'

    # retorna modalidade, parcial e pagina para exibicao no admin
    def auditoria(self):
        if not self.pagamento:
            return ''
        if not self.pagamento.origem_fapesp:
            return ''
        modalidade = self.pagamento.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
        return u'%s (%s/%s)' % (modalidade, self.pagamento.parcial(), self.pagamento.pagina())
    auditoria.short_description = u'Material (par/pág)'

    def altura_em_px(self):
        if self.tamanho:
            tamanho = self.tamanho
        else:
            tamanho = 0

        # calculando a altura em furos
        tam = int(round(tamanho * 3))
        return tam * self.U_TO_PX / 3.0

    def altura_em_pt(self):
        if self.tamanho:
            tamanho = self.tamanho
        else:
            tamanho = 0

        # calculando a altura em furos
        tam = int(round(tamanho * 3))
        return tam * self.U_TO_PT / 3.0

    # Retorna a posição Y em pixels.
    def eixoy_em_px(self):
        eixoY = 0

        # Este patrimonio precisa estar contido em um Rack para definirmos a posição
        if self.patrimonio_id is not None and self.patrimonio.equipamento_id and self.patrimonio.equipamento.tipo_id\
                and self.patrimonio.equipamento.tipo.nome == 'Rack':
            rack = self.patrimonio
            if rack.tamanho:
                rack_altura = int(rack.tamanho) * 3
            else:
                # ISSO É UM PROBLEMA DE DADOS INVÁLIDOS. PRECISA SER TRATADO
                # Configurando como 42Us ou 126 furos
                rack_altura = 126
            pos = self.historico_atual_prefetched.posicao_furo - 1

            if self.tamanho:
                tamanho = self.tamanho
            else:
                tamanho = 0

            # calculando a altura em furos
            tam = int(round(tamanho * 3))

            # calculando a posição em pixels
            eixoY = int(round(((rack_altura - pos - tam) * self.U_TO_PX) / 3.0)) - 5.0

        return eixoY

    def eixoy_em_pt(self):
        return (self.eixoy_em_px() / self.U_TO_PX * self.U_TO_PT) + 5.0

    # Verifica se o patrimonio está em posição traseira no rack
    def is_posicao_traseira(self):
        flag_traseiro = False
        if self.historico_atual_prefetched.posicao_colocacao in ('TD', 'TE', 'T', 'T01', 'T02', 'T03'):
            flag_traseiro = True

        return flag_traseiro

    # Verifica se o patrimonio é uma régua de tomadas lateral
    def is_pdu(self):
        if self.equipamento_id \
                and self.equipamento.tipo_id \
                and 'tomada' in self.equipamento.tipo.nome \
                and self.historico_atual_prefetched.posicao_colocacao in ('TD', 'TE', 'lD', 'lE', 'LD', 'LE'):

            return True
        return False

    # Retorna o estado atual
    def estado(self):
        if not self.historico_atual:
            return None
        else:
            return self.historico_atual.estado

    # Define a descrição do modelo.
    class Meta:
        verbose_name = _(u'Patrimônio')
        verbose_name_plural = _(u'Patrimônio')
        ordering = ('tipo', 'descricao')


class PatrimonioRack(Patrimonio):

    @staticmethod
    def get_racks_as_list(endereco_id):
        patrimonio_racks = PatrimonioRack.objects.filter(equipamento__tipo__nome='Rack',
                                                         historicolocal__endereco__id=endereco_id)\
            .prefetch_related('historicolocal_set')

        patrimonio_racks = list(patrimonio_racks)
        # Ordena os racks pela posição. Ex: R042 - ordena pela fila 042 e depois pela posição R
        patrimonio_racks.sort(key=lambda x: x.historico_atual_prefetched.posicao_rack_letra, reverse=False)
        patrimonio_racks.sort(key=lambda x: x.historico_atual_prefetched.posicao_rack_numero, reverse=True)

        return patrimonio_racks

    def get_patrimonios(self):
        # ordena os equipamentos do rack conforme a posição no rack
        hist = self.contido.annotate(hist=Max('historicolocal__data')).values_list('pk')
        pts = list(self.contido.filter(pk__in=hist)
                   .select_related('equipamento', 'equipamento__tipo', 'equipamento__dimensao',
                                   'patrimonio__equipamento', 'patrimonio__equipamento__tipo',
                                   'patrimonio__equipamento__dimensao')
                   .prefetch_related('historicolocal_set'))
        pts.sort(key=lambda x: x.historico_atual_prefetched.posicao_furo, reverse=True)

        return pts

    def altura_furos(self):
        if self.tamanho:
            rack_altura = int(self.tamanho) * 3
        else:
            # ISSO É UM PROBLEMA DE DADOS INVÁLIDOS. PRECISA SER TRATADO
            rack_altura = 126
        return rack_altura

    class Meta:
        proxy = True


class HistoricoLocal(models.Model):
    """
    Uma instância dessa classe representa o histórico de um patrimônio.

    O método '__unicode__' 	Retorna os campos 'data', 'patrimonio', 'endereco'.
    A class 'Meta' 		Define a descrição do modelo (singular e plural), a ordenação dos dados pelo campo 'data'
     e a unicidade dos dados pelos campos 'patrimonio', 'endereco', 'descricao' e 'data'.
    """
    memorando = models.ForeignKey('memorando.MemorandoSimples', null=True, blank=True)
    patrimonio = models.ForeignKey(Patrimonio, verbose_name=_(u'Patrimônio'))
    endereco = models.ForeignKey('identificacao.EnderecoDetalhe', verbose_name=_(u'Localização'))
    estado = models.ForeignKey(Estado, verbose_name=_(u'Estado do Patrimônio'))
    descricao = models.TextField(_(u'Ocorrência'), help_text=_(u'ex. Empréstimo'))
    data = models.DateField(_(u'Data'))
    posicao = models.CharField(u'Posição', max_length=50, null=True, blank=True,
                               help_text=_(u"<b>[rack:</b>XXX<b>].F[furo:</b>000<b>]."
                                           u"[posicao:</b>T,TD,TE,T01,T02,LD,LE,01,02<b>]</b>"))
    pai = models.ForeignKey(Patrimonio, null=True, blank=True, related_name='filhos')

    # Retorna a data o patrimônio e o endereco.
    def __unicode__(self):
        return u'%s - %s | %s' % (self.data.strftime('%d/%m/%Y'), self.patrimonio, self.endereco or '')

    # Define a descrição do modelo e a ordenação dos dados pelo campo 'nome'.
    class Meta:
        verbose_name = _(u'Histórico Local')
        verbose_name_plural = _(u'Histórico Local')
        ordering = ('-data', 'id')
        unique_together = (('patrimonio', 'endereco', 'descricao', 'data'), )

    @cached_property
    def posicao_rack(self):
        """
        Retorna o código do Rack do campo de posição.

        Ex: em uma posição com valor R042.F085.TD
            o código do Rack é o R042.
        """
        retorno = None
        if self.posicao:
            rack_str = self.posicao.split('.')

            if len(rack_str) == 1:
                rack_str = self.posicao.split('-')

            if len(rack_str) >= 2:
                retorno = rack_str[0]
        return retorno

    @cached_property
    def posicao_rack_letra(self):
        """
        Retorna a letra do Rack, a partir do campo de Posicao.

        Ex: em uma posição com valor R042.F085.TD
            a letra do Rack é o R.
        """
        retorno = None
        if self.posicao:
            rack_str = self.posicao.split('.')

            if len(rack_str) == 1:
                rack_str = self.posicao.split('-')

            if len(rack_str) >= 2:
                eixoLetra = re.findall(r'[a-zA-Z]+', rack_str[0])
                if len(eixoLetra) == 1:
                    retorno = eixoLetra[0]

        return retorno

    @cached_property
    def posicao_rack_numero(self):
        """
        Retorna o número do Rack, a partir do campo de Posicao.

        Ex: em uma posição com valor R042.F085.TD
            o número do Rack é o 042.
        """
        retorno = None
        if self.posicao:
            rack_str = self.posicao.split('.')
            if len(rack_str) == 1:
                rack_str = self.posicao.split('-')

            if len(rack_str) >= 2:
                eixoNumero = re.findall(r'\d+', rack_str[0])
                if len(eixoNumero) == 1:
                    retorno = eixoNumero[0]
        return retorno

    @cached_property
    def posicao_furo(self):
        """
        Retorna o furo em que o equipamento está posicionado, a partir do campo de Posicao.

        Ex: em uma posição com valor R042.F085.TD
            o furo é o 085
        """
        retorno = -1
        if self.posicao:
            # verifica se possui a posição já configurada
            if self.posicao.isdigit():
                retorno = int(self.posicao)
            else:
                # verifica se é possível recuperar a posição de furo de uma string como R042.F085.TD
                furo_str = self.posicao.split('.F')
                if len(furo_str) > 1:
                    pos_str = furo_str[1].split('.')
                    if len(pos_str) >= 1 and pos_str[0].isdigit():
                        retorno = int(pos_str[0])
                    else:
                        pos_str = furo_str[1].split('-')
                        if len(pos_str) > 1:
                            retorno = int(pos_str[0])

        return retorno

    @cached_property
    def posicao_colocacao(self):
        """
        Retorna o código em que o equipamento está colocado, a partir do campo de Posicao.
        Como padrão utilizamos os códigos:
        T - traseira
        TD - traseira direita
        TE - traseira esquerda
        piso - posicionado sobre o piso

        Ex: em uma posição com valor R042.F085.TD
            o código retornado é o TD.
        """
        retorno = None
        if self.posicao:
            # verifica se é possível recuperar a posição TD de uma string como R042.F085.TD ou R042.F085-TD
            furo_str = self.posicao.split('.F')
            if len(furo_str) >= 2:
                pos_str = furo_str[1].split('.')
                if len(pos_str) >= 2:
                    retorno = pos_str[1]
                else:
                    pos_str = furo_str[1].split('-')
                    if len(pos_str) > 1:
                        retorno = pos_str[1]

            else:
                # verifica se é possível recuperar a posição piso de uma string como R042.piso
                pos_str = self.posicao.split('.')
                if len(pos_str) == 2:
                    retorno = pos_str[1]
                else:
                    # verifica se é possível recuperar a posição piso de uma string como R042-piso
                    pos_str = self.posicao.split('-')
                    if len(pos_str) == 2:
                        retorno = pos_str[1]

        return retorno


class Direcao(models.Model):
    origem = models.CharField(max_length=15)
    destino = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s - %s' % (self.origem, self.destino)

    class Meta:
        verbose_name = u'Direção'
        verbose_name_plural = u'Direções'


class DistribuicaoUnidade(models.Model):
    nome = models.CharField(max_length=45)
    sigla = models.CharField(max_length=4)

    def __unicode__(self):
        return u'%s - %s' % (self.sigla, self.nome)


class Distribuicao(models.Model):
    inicio = models.IntegerField()
    final = models.IntegerField()
    unidade = models.ForeignKey('patrimonio.DistribuicaoUnidade')
    direcao = models.ForeignKey('patrimonio.Direcao')

    def __unicode__(self):
        return u'%s - %s' % (self.inicio, self.final)

    class Meta:
        verbose_name = u'Distribuição'
        verbose_name_plural = u'Distribuições'


class UnidadeDimensao(models.Model):
    nome = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        verbose_name = u'Unidade da dimensão'
        verbose_name_plural = u'Unidade das dimensões'


class Dimensao(models.Model):
    altura = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    largura = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    profundidade = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    peso = models.DecimalField('Peso (kg)', max_digits=6, decimal_places=3, null=True, blank=True)
    unidade = models.ForeignKey('patrimonio.UnidadeDimensao')

    def __unicode__(self):
        return u'%s x %s x %s %s - %s kg' % (self.altura, self.largura, self.profundidade, self.unidade,
                                             (self.peso or '-'))

    class Meta:
        verbose_name = u'Dimensão'
        verbose_name_plural = u'Dimensões'


class TipoEquipamento(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        ordering = ('nome',)


class Equipamento(models.Model):
    '''
    Modelo que guarda um "tipo", um "modelo" de equipamento
    '''
    tipo = models.ForeignKey('patrimonio.TipoEquipamento', null=True, blank=True)
    descricao = models.TextField(_(u'Descrição'))
    part_number = models.CharField(null=True, blank=True, max_length=50)

    # TERMINADA A ASSOCIAÇÃO COM A ENTIDADE, DESABILITAR O CAMPO MARCA(CHARFIELD)
    # marca = models.CharField(_(u'Marca ou Editora'), null=True, blank=True, max_length=100)
    entidade_fabricante = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Marca/Editora'),
                                            null=True, blank=True,
                                            help_text=u"Representa a Entidade que fabrica este equipamento.")

    modelo = models.CharField(null=True, blank=True, max_length=100)
    tamanho = models.DecimalField(u'Tamanho (em U)', max_digits=5, decimal_places=2, null=True, blank=True)
    dimensao = models.ForeignKey('patrimonio.Dimensao', null=True, blank=True)
    especificacao = models.FileField(u'Especificação', upload_to='patrimonio', null=True, blank=True)

    imagem = models.ImageField(u'Imagem Frontal do equipamento', upload_to='patrimonio', null=True, blank=True)
    imagem_traseira = models.ImageField(u'Imagem Traseira do equipamento', upload_to='patrimonio',
                                        null=True, blank=True)

    convencoes = models.ManyToManyField('patrimonio.Distribuicao', verbose_name=u'Convenções')
    titulo_autor = models.CharField(_(u'Título e autor'), null=True, blank=True, max_length=100)
    isbn = models.CharField(_(u'ISBN'), null=True, blank=True, max_length=20)

    # utilizado somente para carga de arquivos de especificação
    # url_equipamento = models.CharField(_(u'url_equipamento'), null=True, blank=True, max_length=200)

    def __unicode__(self):
        return u'%s - %s' % (self.descricao, self.part_number)

    class Meta:
        ordering = ('descricao',)


class PlantaBaixaDataCenter(models.Model):
    endereco = models.ForeignKey(EnderecoDetalhe, verbose_name=_(u'Data center'))
    w = models.IntegerField(default=800)
    h = models.IntegerField(default=600)
    cor = models.CharField(max_length=7, null=True, blank=True, default='#fff')

    def __unicode__(self):
        return u'%s' % self.endereco.complemento

    class Meta:
        verbose_name = u'Planta baixa - Data Center'
        verbose_name_plural = u'Planta baixa - Data Centers'


class PlantaBaixaObjeto(models.Model):
    data_center = models.ForeignKey(PlantaBaixaDataCenter, verbose_name=_(u'Data center'))
    patrimonio = models.ForeignKey(Patrimonio, verbose_name=_(u'Patrimônio'), null=True, blank=True)
    titulo = models.CharField(max_length=80)
#    imagem = models.FileField(u'Planta Baixa', upload_to='planta_baixa', null=True, blank=True)

    def __unicode__(self):
        retorno = ''
        if self.data_center:
            retorno = '%s' % self.data_center
        if self.patrimonio:
            retorno = '%s - %s' % (retorno, self.patrimonio.apelido)
        if self.titulo:
            retorno = '%s - %s' % (retorno, self.titulo)
        else:
            retorno = '%s - <sem_titulo>' % retorno
        return retorno

    class Meta:
        verbose_name = u'Planta baixa - Objeto'
        verbose_name_plural = u'Planta baixa - Objetos'


class PlantaBaixaPosicao(models.Model):
    objeto = models.ForeignKey(PlantaBaixaObjeto)
    descricao = models.CharField(max_length=80, null=True, blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    w = models.IntegerField(default=100)
    h = models.IntegerField(default=100)
    cor = models.CharField(max_length=6, null=True, blank=True, default='EEEEEE')

    def __unicode__(self):
        return u'%s' % self.objeto.titulo

    class Meta:
        verbose_name = u'Planta baixa - Posição'
        verbose_name_plural = u'Planta baixa - Posições'


# Classe para definição de permissões de views e relatórios da app patrimonio
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_tec_planta_baixa_edit", u"Rel. Téc. - Planta baixa - Racks"),  # /patrimonio/planta_baixa_edit
            ("rel_tec_racks", u"Rel. Téc. - Racks "),     # /patrimonio/racks
            ("rel_tec_por_estado", u"Rel. Téc. - Patr por estado do item"),     # /patrimonio/relatorio/por_estado
            ("rel_tec_por_local", u"Rel. Téc. - Patr por localização"),     # /patrimonio/relatorio/por_local
            ("rel_tec_por_local_rack", u"Rel. Téc. - Patr por local e rack"),     # /patrimonio/relatorio/por_local_rack
            ("rel_tec_por_local_termo", u"Rel. Téc. - Patr por localização (com Termo)"),     # /patrimonio/relatorio/por_local_termo
            ("rel_tec_por_marca", u"Rel. Téc. - Patr por marca"),     # /patrimonio/relatorio/por_marca
            ("rel_adm_por_termo", u"Rel. Adm. - Patr por termo de outorga"),     # /patrimonio/relatorio/por_termo
            ("rel_tec_por_tipo", u"Rel. Téc. - Patr por tipo"),     # /patrimonio/relatorio/por_tipo
            ("rel_tec_por_tipo_equipamento", u"Rel. Téc. - Busca por tipo de equip"),     # /patrimonio/relatorio/por_tipo_equipamento
            ("rel_tec_patr_tipo_equipamento", u"Rel. Téc. - Patr por tipo de equip"),     # /patrimonio/relatorio/por_tipo_equipamento2
            ("rel_adm_presta_contas", u"Rel. Adm. - Prestação de contas patrimonial"),     # /patrimonio/relatorio/presta_contas
            ("rel_tec_relatorio_rack", u"Rel. Téc. - Relatório por rack"),     # /patrimonio/relatorio_rack
        )
