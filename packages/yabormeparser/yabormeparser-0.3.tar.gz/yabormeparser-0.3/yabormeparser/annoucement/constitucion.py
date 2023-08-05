#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.lex
import re
import datetime
import common
import logging
import filters


class Lexer(object):
    # List of token names.
    tokens = (
        'BEGIN',
        'LENGTH',
        'PURPOSE',
        'ADDRESS',
        'CAPITAL',
        'MONEY',
        'DATE',
        'TEXT',
        'STRINGDATE',
        )

    # States: inclusive or exclusive
    # We used inclusive because we thought the order is important.
    states = (
        ('begin', 'exclusive'),
        ('length', 'exclusive'),
        ('capital', 'exclusive')
    )

    # Regular expression rules for INITIAL STATES.
    t_TEXT = ur'.'
    # t_ignore = ur' '

    def __init__(self):
        self._log = logging.getLogger(__name__)

    def t_begin_length_DATE(self, t):
        ur'\d{1,2}\.\d{1,2}\.\d{1,2}[^\.]*'
        expression = ur'(\d{1,2})\.(\d{1,2})\.(\d{1,2})'
        res = re.search(expression, t.value)
        if not res:
            raise common.ParserException("Wrong date format.")
        day = int(res.group(1))
        month = int(res.group(2))
        year = int("20" + res.group(3))
        try:
            t.value = datetime.date(year, month, day)
        except ValueError as e:
            raise common.ParserException("Wrong date value: %s" % e.message)
        return t

    def t_BEGIN(self, t):
        ur'Comienzo\sde\soperaciones:'
        t.lexer.begin('begin')
        return t

    def t_begin_LENGTH(self, t):
        ur'Duración:'
        t.lexer.begin('length')
        return t

    t_begin_length_capital_ignore = u" ."

    def t_length_begin_PURPOSE(self, t):
        ur'Objeto\ssocial:'
        t.lexer.begin('INITIAL')
        return t

    def t_begin_INITIAL_ADDRESS(self, t):
        ur'Domicilio\:'
        t.lexer.begin('INITIAL')
        return t

    def t_capital_INITIAL_CAPITAL(self, t):
        ur'Capital\:|Capital\ssuscrito:|Desembolsado\:'
        t.lexer.begin('capital')
        return t

    def t_begin_length_STRINGDATE(self, t):
        ur'[A-Za-z0-9][^\.]*'
        return t

    def t_capital_MONEY(self, t):
        ur'[\d.,]+\sEuros'
        n = t.value
        n = n.translate({ord('.'): None, ord(','): ord('.')})
        n = n.rstrip(" Euros")
        t.value = float(n)
        return t

    def t_error(self, t):
        self._log.error("Illegal character '%s'" % t.value[0])

    def t_begin_error(self, t):
        self._log.error("BEGIN: Illegal character '%s'" % t.value[0])

    def t_length_error(self, t):
        self._log.error("LENGTH: Illegal character '%s'" % t.value[0])

    def t_capital_error(self, t):
        self._log.error("CAPITAL: Illegal character '%s'" % t.value[0])

    def build(self, **kwargs):
        self.lexer = ply.lex.lex(module=self, **kwargs)

    def test(self, data):
        toks = []
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            toks.append(tok)
        return toks


class Parser(object):
    def __init__(self, text):
        text = filters.ptas_to_euros(text)
        self.begin = ""  # Comienzo de operaciones
        self.length = ""  # Duración
        self.purpose = ""  # Objeto social
        self.address = ""  # Domicilio
        self.capital = 0.0  # Capital

        self.state = None
        self.state_value = None
        self.states = ('BEGIN', 'LENGTH', 'PURPOSE', 'ADDRESS', 'CAPITAL')
        self.lex = Lexer()
        self.lex.build()
        self.lex.lexer.input(text)
        while self._process_token():
            pass
        self.purpose = self.purpose.strip()
        self.address = self.address.strip()

    def _process_token(self):
        tok = self.lex.lexer.token()
        if tok:
            if tok.type in self.states:
                self._set_state(tok)
            else:
                self._set_tok(tok)
        return bool(tok)

    def _set_state(self, tok):
        self.state = tok.type
        self.state_value = tok.value

    def _set_tok(self, tok):
        processed = False
        if self.state == 'BEGIN' and tok.type == 'DATE':
            self.begin = tok.value.isoformat()
            processed = True
        if self.state == 'LENGTH' and tok.type == 'DATE':
            self.length = tok.value.isoformat()
            processed = True
        if self.state == 'BEGIN' and tok.type == 'STRINGDATE':
            self.begin = '0000-00-00'
            processed = True
        if self.state == 'LENGTH' and tok.type == 'STRINGDATE':
            self.length = "0000-00-00"
            processed = True
        elif self.state == 'PURPOSE' and tok.type == 'TEXT':
            # self.purposes.append(tok.value)
            self.purpose += tok.value
            processed = True
        elif self.state == 'ADDRESS' and tok.type == 'TEXT':
            self.address += tok.value
            processed = True
        elif self.state == 'CAPITAL' and tok.type == 'MONEY':
            if self.state_value == u'Capital:':
                self.capital = tok.value
            elif self.state_value == u'Capital suscrito:':
                self.capital = tok.value
            elif self.state_value == u'Desembolsado:':
                if self.capital == 0.0:
                    self.capital = tok.value
            processed = True
        if not processed:
            raise common.ParserException("Not processed token.")

    def to_dict(self):
        return {
            'begin': self.begin,
            'purpose': self.purpose,
            'address': self.address,
            'capital': self.capital
            }

    def to_str(self):
        res = u"Begin: %s\n" % self.begin
        res += u"Purpose: %s\n" % self.purpose
        res += u"Address: %s\n" % self.address
        res += u"Capital: %s\n" % self.capital
        return res

if __name__ == "__main__":
    c = (u"Comienzo de operaciones: 22.09.14. Objeto social:" +
         u" MANIPULACION DE TODA CLASE DE PAPEL, CARTON, CARTULINA " +
         u"O MATERIALES SIMILARES. FABRICACION DE SACOS, BOLSAS, " +
         u"CAJAS, SU DISTRIBUCION, VENTA, IMPORTACIO'N, EXPORTACION" +
         u" Y COMERCIALIZACION EN TODOS SUS ASPECTOS... Domicilio: " +
         u"C/ PINTO, 70 (PARLA). Capital: 112.500,00 Euros.")
    constitucion = c
    # m = Lexer()
    # m.build()
    # print m.test(constitucion)
    print Parser(c).to_str()
