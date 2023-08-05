#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.lex
import logging
import common
import filters


class Lexer(object):
    # List of tokens names.
    tokens = (
        'CAPITAL',
        'MONEY'
    )
    t_ignore = " ."
    t_capital_ignore = " ."

    # default: INITIAL
    states = (
        ('capital', 'exclusive'),
    )

    fields = (u"Capital", u"Resultante Suscrito", u"Suscrito",
              u"Desembolsado", u"Resultante Desembolsado")

    field_re = ur'|'.join([r + ":" for r in fields])
    field_re = field_re.replace(' ', r'\s').replace(ur'.', r'\.')

    @ply.lex.TOKEN(field_re)
    def t_CAPITAL(self, t):
        t.lexer.begin('capital')
        return t

    def t_capital_MONEY(self, t):
        ur'[\d.,]+\sEuros'
        n = t.value
        n = n.translate({ord('.'): None, ord(','): ord('.')})
        n = n.rstrip(" Euros")
        t.value = float(n)
        t.lexer.begin('INITIAL')
        return t

    def build(self, **kwargs):
        self.lexer = ply.lex.lex(module=self, **kwargs)

    def t_error(self, t):
        self._log.error("Illegal character '%s'" % t.value[0])

    def t_capital_error(self, t):
        self._log.error("ROLE: Illegal character '%s'" % t.value[0])

    def test(self, data):
        toks = []
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            toks.append(tok)
        return toks

    def __init__(self):
        self._log = logging.getLogger(__name__)


class Parser(object):
    def __init__(self, text):
        text = filters.ptas_to_euros(text)
        text = filters.delete_modificacion_duracion(text)
        self.capital = 0.0
        self.resultante_suscrito = 0.0
        self.suscrito = 0.0
        self.desembolsado = 0.0
        self.resultante_desembolsado = 0.0
        self.state = None
        self.field = None
        self.states = ('CAPITAL')
        self.lex = Lexer()
        self.lex.build()
        self.lex.lexer.input(text)
        while self._process_token():
            pass

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
        self.field = tok.value

    def _set_tok(self, tok):
        is_wrong_state = (self.state != 'CAPITAL' or tok.type != 'MONEY'
                          or not self.field)
        if is_wrong_state:
            raise common.ParserException("Wrong token order.")

        if self.field == u"Capital:":
            self.capital = tok.value
        elif self.field == u"Resultante Suscrito:":
            self.resultante_suscrito = tok.value
        elif self.field == u"Suscrito:":
            self.suscrito = tok.value
        elif self.field == u"Desembolsado:":
            self.desembolsado = tok.value
        elif self.field == u"Resultante Desembolsado:":
            self.resultante_desembolsado = tok.value

    def to_dict(self):
        return {
            'capital': self.capital,
            'resultante_suscrito': self.resultante_suscrito,
            'suscrito': self.suscrito,
            'desembolsado': self.desembolsado,
            'resultante_desembolsado': self.resultante_desembolsado
            }

    def to_str(self):
        res = "Capital: %s\n" % self.capital
        res += "Resultante_suscrito: %s\n" % self.resultante_suscrito
        res += "Suscrito: %s\n" % self.suscrito
        res += "Desembolsado: %s\n" % self.desembolsado
        res += "Resultante_desembol.: %s\n" % self.resultante_desembolsado
        return res

if __name__ == "__main__":
    c_1 = u"Capital: 72.144,00 Euros. Resultante Suscrito: 75.150,00 Euros."
    c = u"Suscrito: 248.999,24 Euros. Desembolsado: 248.999,24 Euros. Resultante Suscrito: 4.760.122,36 Euros. Resultante Desembolsado: 4.760.122,36 Euros."
    capital = c
    # m = Lexer()
    # m.build()
    # m.test(capital)
    print Parser(c_1).to_str()
    print Parser(capital).to_str()
