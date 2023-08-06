# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date, timedelta, datetime
from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
import calendar
from membro.models import Controle, Membro, Ferias, ControleFerias, SindicatoArquivo, \
    DispensaLegal, TipoDispensa, Usuario, Historico, Cargo, Banco, DadoBancario, Assinatura, TipoAssinatura
from protocolo.models import Feriado
from identificacao.models import Entidade

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Get current timezone
tz = timezone.get_current_timezone()


class TipoAssinaturaTest(TestCase):
    def test_unicode(self):
        ta = TipoAssinatura.objects.create(nome='Cheque')
        self.assertEquals(u'Cheque', ta.__unicode__())


class UsuarioTest(TestCase):
    def test_unicode(self):
        ent = Entidade.objects.create(sigla='ANSP', nome='Academic Network at São Paulo', cnpj='', fisco=True)  # @UnusedVariable
        mb = Membro.objects.create(nome='Soraya Gomes', email='soraya@gomes.com', cpf='000.000.000-00', site=True)
        usr = Usuario.objects.create(membro=mb, username='soraya', sistema='Administrativo')

        self.assertEquals('soraya', usr.__unicode__())


class MembroTest(TestCase):
    def setUp(self):
        ent = Entidade.objects.create(sigla='ANSP', nome='Academic Network at São Paulo', cnpj='', fisco=True)  # @UnusedVariable
        mb = Membro.objects.create(nome='Joice Gomes', email='soraya@gomes.com', cpf='000.000.000-00', ramal=23,
                                   site=True)
        cg = Cargo.objects.create(nome='Secretaria')
        ht = Historico.objects.create(inicio=datetime(2008, 1, 1), cargo=cg, membro=mb, funcionario=True)  # @UnusedVariable

    def test_cargo_atual(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals('Secretaria', mb.cargo_atual)

    def test_cargo_atual_depois_do_desligamento(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        ht = Historico.objects.get(pk=1)
        ht.termino = datetime(2008, 1, 2)
        ht.save()

        self.assertEquals('', mb.cargo_atual)

    def test_ramal(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals(23, mb.existe_ramal())

    def test_ramal_vazio(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        mb.ramal = None

        self.assertEqual('', mb.existe_ramal())

    def test_curriculo_vazio(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals('', mb.existe_curriculo())

    def test_curriculo(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        mb.url_lattes = 'teste'

        self.assertEquals('<center><a href="teste">teste</a></center>', mb.existe_curriculo())

    def test_unicode(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals('Joice Gomes (Secretaria)', mb.__unicode__())

    def test_unicode_depois_do_desligamento(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        ht = Historico.objects.get(pk=1)
        ht.termino = datetime(2008, 1, 2)
        ht.save()

        self.assertEquals('Joice Gomes', mb.__unicode__())


class DadoBancarioTest(TestCase):
    def setUp(self):
        mb = Membro.objects.create(nome='Joice Gomes', funcionario=True, email='soraya@gomes.com', cpf='000.000.000-00',
                                   ramal=23, site=True)
        cg = Cargo.objects.create(nome='Secretaria')
        ht = Historico.objects.create(inicio=datetime(2008, 1, 1), cargo=cg, membro=mb, funcionario=True)  # @UnusedVariable
        b = Banco.objects.create(numero=151, nome='Nossa Caixa')
        db = DadoBancario.objects.create(membro=mb, banco=b, agencia=1690, ag_digito=4, conta=123439, cc_digito='x')  # @UnusedVariable

    def test_agencia_digito(self):
        db = DadoBancario.objects.get(agencia=1690)
        self.assertEquals('1690-4', db.agencia_digito())

    def test_conta_digito(self):
        db = DadoBancario.objects.get(agencia=1690)
        self.assertEquals('123439-x', db.conta_digito())


class AssinaturaTest(TestCase):
    def setUp(self):
        mb = Membro.objects.create(nome='Soraya Gomes', email='soraya@gomes.com', cpf='312.617.028-00', site=True)
        ta = TipoAssinatura.objects.create(nome='Cheque')
        Assinatura.objects.create(membro=mb, tipo_assinatura=ta)

    def test_unicode(self):
        assinatura = Assinatura.objects.get(pk=1)
        self.assertEquals(u'Soraya Gomes | Cheque', assinatura.__unicode__())


class MembroControleTest(TestCase):
    def test_controle_permanencia_um_dia(self):
        """
        Teste de permanencia para um dia com almoço normal de uma hora
        """
        membro = Membro(nome='teste')
        controle = Controle(membro=membro, entrada=timezone.now(), saida=timezone.now()+timedelta(hours=9),
                            almoco_devido=True, almoco=60)
        self.assertEquals(controle.segundos, 8 * 60 * 60, 'Deveria ser 28800 mas e ' + str(controle.segundos))

    def test_controle_permanencia_um_dia_almoco_menor(self):
        """
        Teste de permanencia para um dia com almoço de meia hora
        """
        membro = Membro(nome='teste')
        controle = Controle(membro=membro, entrada=timezone.now(), saida=timezone.now()+timedelta(hours=9),
                            almoco_devido=True, almoco=30)
        self.assertEquals(controle.segundos, 8.5 * 60 * 60, 'Deveria ser 28800 mas e ' + str(controle.segundos))

    def test_controle_permanencia_sem_almoco(self):
        """
        Teste de permanencia em um dia sem almoco
        """
        membro = Membro(nome='teste')
        controle = Controle(membro=membro, entrada=timezone.now(), saida=timezone.now()+timedelta(hours=9),
                            almoco_devido=False, almoco=60)
        self.assertEquals(controle.segundos, 9 * 60 * 60, 'Deveria ser 32400 mas e ' + str(controle.segundos))

    def test_controle_mover_bloco(self):
        membro = Membro.objects.create(id=1, nome='teste', site=True)

        Controle.objects.create(id=1, membro=membro,
                                entrada=tz.localize(datetime(year=2000, month=01, day=01, hour=12)),
                                saida=tz.localize(datetime(year=2000, month=01, day=01, hour=18, minute=30)),
                                almoco_devido=False, almoco=60)
        Controle.objects.get(id=1)

        tempo = 20

        controle = Controle.objects.get(pk=1)
        controle.entrada = controle.entrada + timedelta(minutes=tempo)
        controle.saida = controle.saida + timedelta(minutes=tempo)
        controle.save()

        controle = Controle.objects.get(pk=1)
        entrada = tz.localize(datetime(year=2000, month=01, day=01, hour=12, minute=20))
        self.assertEquals(controle.entrada, entrada)

        saida = tz.localize(datetime(year=2000, month=01, day=01, hour=18, minute=50))
        self.assertEquals(controle.saida, saida)

    def test_controle_unicode(self):
        membro = Membro.objects.create(id=1, nome='teste', site=True)

        Controle.objects.create(id=1, membro=membro,
                                entrada=tz.localize(datetime(year=2000, month=01, day=01, hour=12)),
                                saida=tz.localize(datetime(year=2000, month=01, day=01, hour=18, minute=30)),
                                almoco_devido=False, almoco=60)
        controle = Controle.objects.get(id=1)

        self.assertEqual(controle.__unicode__(), 'teste - de 2000-01-01 12:00:00-02:00 a 2000-01-01 18:30:00-02:00')

class MembroControleHorarioTest(TestCase):

    def create_ferias(self, ano_corrente, mes_corrente, ferias_data_inicio, ferias_data_fim):
        mes_corrente_ini = date(ano_corrente, mes_corrente, 01)
        mes_corrente_fim = date(ano_corrente, mes_corrente, 01) +\
            timedelta(calendar.monthrange(ano_corrente, mes_corrente)[1])

        membro = Membro(id=1)
        ferias = Ferias(membro=membro, id=1)
        ControleFerias.objects.create(ferias=ferias, inicio=ferias_data_inicio, termino=ferias_data_fim,
                                      dias_uteis_fato=30, dias_uteis_aberto=0, oficial=True, vendeu10=False,
                                      antecipa13=False)

        # ferias_ini < mes_ini < ferias_fim  OR  mes_ini < ferias_ini < mes_fim
        controleFerias = ControleFerias.objects.filter(Q(inicio__lte=mes_corrente_ini, termino__gte=mes_corrente_ini) |
                                                       Q(inicio__gte=mes_corrente_ini, inicio__lte=mes_corrente_fim),
                                                       ferias=ferias)
        return controleFerias

    def test_controle_ferias_final_de_ano(self):
        ferias_ini = date(2012, 12, 30)
        ferias_fim = date(2013, 1, 1)

        controleFerias = self.create_ferias(2013, 01, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)

    def test_controle_ferias_inicio_de_mes(self):
        ferias_ini = date(2013, 01, 30)
        ferias_fim = date(2013, 02, 15)

        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)

    def test_controle_ferias_final_de_mes(self):
        ferias_ini = date(2013, 02, 25)
        ferias_fim = date(2013, 03, 15)

        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)

    def test_controle_ferias_meio_de_mes(self):
        ferias_ini = date(2013, 02, 10)
        ferias_fim = date(2013, 02, 25)

        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)

    def test_controle_ferias_entre_meses(self):
        ferias_ini = date(2013, 01, 15)
        ferias_fim = date(2013, 03, 15)

        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)

    def test_controle_ferias_mes_passado(self):
        ferias_ini = date(2013, 01, 15)
        ferias_fim = date(2013, 01, 30)

        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 0)

    def test_controle_ferias_ano_passado(self):
        ferias_ini = date(2012, 02, 10)
        ferias_fim = date(2012, 02, 15)

        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 0)


class DispensaLegalTest(TestCase):
    def test_dia_dispensa_mesmo_dia(self):
        membro = Membro.objects.create(id=1, site=True)

        tipo = TipoDispensa.objects.create()
        # a data é uma sexta-feira
        DispensaLegal.objects.create(membro=membro, tipo=tipo, dias_corridos=1, horas=0, minutos=0,
                                     inicio_realizada=date(2013, 7, 19), realizada=True,
                                     inicio_direito=date(2013, 7, 19), atestado=False)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 19))

        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)

    def test_dia_dispensa_mesmo_dia_meio_periodo(self):
        membro = Membro.objects.create(id=1, site=True)

        tipo = TipoDispensa.objects.create()
        # a data é uma sexta-feira
        DispensaLegal.objects.create(membro=membro, tipo=tipo, dias_corridos=0, horas=4, minutos=0,
                                     inicio_realizada=date(2013, 7, 19), realizada=True,
                                     inicio_direito=date(2013, 7, 19), atestado=False)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 19))

        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 4)

    def test_dia_dispensa_mesmo_dia_meio_periodo_e_meio(self):
        membro = Membro.objects.create(id=1, site=True)

        tipo = TipoDispensa.objects.create()
        # a data é uma sexta-feira
        DispensaLegal.objects.create(membro=membro, tipo=tipo, dias_corridos=0, horas=4, minutos=30,
                                     inicio_realizada=date(2013, 7, 19), realizada=True,
                                     inicio_direito=date(2013, 7, 19), atestado=False)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 19))

        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 4.5)

    def test_dia_dispensa_dois_dias_meio_periodo_e_meio(self):
        membro = Membro.objects.create(id=1, site=False)

        tipo = TipoDispensa.objects.create(nome='Medica')
        # a data é uma sexta-feira
        DispensaLegal.objects.create(membro=membro, tipo=tipo, dias_corridos=2, horas=4, minutos=30,
                                     inicio_realizada=date(2013, 7, 19), realizada=True,
                                     inicio_direito=date(2013, 7, 19), atestado=False)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 19))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 20))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 21))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 4.5)

    def test_dia_dispensa_dois_dias(self):
        membro = Membro.objects.create(id=1, site=True)

        tipo = TipoDispensa.objects.create(nome='Medica')
        # a data é uma sexta-feira
        DispensaLegal.objects.create(membro=membro, tipo=tipo, dias_corridos=2,
                                     inicio_realizada=date(2013, 7, 19), realizada=True,
                                     inicio_direito=date(2013, 7, 19), atestado=False)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 18))
        self.assertEqual(dispensa['is_dispensa'], False)
        self.assertEqual(dispensa['horas'], 0)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 19))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 20))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)

        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013, 7, 21))
        self.assertEqual(dispensa['is_dispensa'], False)
        self.assertEqual(dispensa['horas'], 0)

    def test_dia_dispensa_dia_diferente(self):
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=5, inicio_realizada=date(2013, 7, 19), realizada=True, )
        # dispensa para sexta, segunda, terca
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 1)

    def test_data_termino_realizada_fim_semana(self):
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=5, inicio_realizada=date(2013, 7, 19), realizada=True, )
        # dispensa para sexta, segunda, terca
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 1)

    def test_data_termino_realizada_sexta(self):
        # a data é uma sexta
        dispensaLegal = DispensaLegal(dias_corridos=1, inicio_realizada=date(2013, 7, 19), realizada=True, )
        # dispensa para sexta
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 4)

    def test_data_termino_realizada_meio_da_semana(self):
        # a data é uma segunda
        dispensaLegal = DispensaLegal(dias_corridos=3, inicio_realizada=date(2013, 7, 15), realizada=True, )
        # dispensa para segunda, terca, quarta
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 2)

    def test_data_termino_realizada_um_dia(self):
        # a data é uma segunda
        dispensaLegal = DispensaLegal(dias_corridos=1, inicio_realizada=date(2013, 7, 15), realizada=True, )

        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 15)
        # dispensa para segunda
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 0)

    def test_data_termino_realizada_zero_dia(self):
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=0, inicio_realizada=date(2013, 7, 15), realizada=True, )

        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 15)

        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 0)
        self.assertEqual(dispensaLegal.inicio_realizada.weekday(), 0)

    def test_data_termino_realizada_meio_da_semana_com_feriado(self):
        f = Feriado.objects.create(feriado=date(2013, 7, 16))  # @UnusedVariable

        # a data é uma segunda
        dispensaLegal = DispensaLegal(dias_corridos=3, inicio_realizada=date(2013, 7, 15), realizada=True, )

        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 17)

        # dispensa para segunda, terca, quarta
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 2)

    def test_data_termino_realizada_fim_semana_com_feriado_no_sabado(self):
        f = Feriado.objects.create(feriado=date(2013, 7, 20))  # @UnusedVariable

        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=3, inicio_realizada=date(2013, 7, 19), realizada=True, )
        # dispensa para sexta, segunda, terca
        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 21)

        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 6)


class FeriasTest(TestCase):
    def test_total_dias_uteis_aberto(self):
        """
        Teste de permanencia para um dia com almoço normal de uma hora
        """
        membro = Membro.objects.create(id=1, nome='teste', site=True)

        ferias = Ferias.objects.create(id=10, membro=membro, inicio=datetime.now(), realizado=True)

        ControleFerias.objects.create(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=20,
                                      dias_uteis_aberto=10, oficial=True, vendeu10=False, antecipa13=False)
        ControleFerias.objects.create(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=0,
                                      dias_uteis_aberto=30, oficial=True, vendeu10=False, antecipa13=False)
        ControleFerias.objects.create(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=0,
                                      dias_uteis_aberto=30, oficial=True, vendeu10=False, antecipa13=False)
        ControleFerias.objects.create(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=30,
                                      dias_uteis_aberto=0, oficial=True, vendeu10=False, antecipa13=False)

        self.assertEquals(Ferias().total_dias_uteis_aberto(1), 20 * 8 * 60 * 60)


class MembroSindicatoArquivoTest(TestCase):
    def setUp(self):
        ent = Entidade.objects.create(sigla='ANSP', nome='Academic Network at São Paulo', cnpj='', fisco=True)  # @UnusedVariable
        mb = Membro.objects.create(nome='Joice Gomes', email='soraya@gomes.com', cpf='000.000.000-00', ramal=23,
                                   site=True)
        arquivo = SindicatoArquivo.objects.create(arquivo='/teste/arquivo.pdf', ano='2013', membro=mb)  # @UnusedVariable

    def test_membro_sindicatoarquivo_unicode(self):

        arquivo = SindicatoArquivo.objects.get(pk=1)
        self.assertEquals(arquivo.__unicode__(), '2013 - /teste/arquivo.pdf')
