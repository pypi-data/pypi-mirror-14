#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.lex
import logging
import common
import positiondict
import filters

position = positiondict.POSITION


class Lexer(object):

    roles = tuple(position.keys())

    tokens = (  # ply.lex required
        'ROLE',
        'TEXT',
        'SEPARATOR',
        'END'
        )

    # States: inclusive or exclusive
    # We used inclusive because we thought the order is important.
    # INITIAL --> default state.
    def __init__(self):
        self._log = logging.getLogger(__name__)

    role_re = ur'|'.join([r + ":" for r in roles])
    role_re = role_re.replace(' ', r'\s').replace(ur'.', r'\.')
    role_re = role_re.replace(ur'V-', r'V-\s?')
    ignore_case = ur'(?iu)'

    @ply.lex.TOKEN(ignore_case + role_re)
    def t_ROLE(self, t):
        return t

    t_SEPARATOR = ur';'
    t_TEXT = ur'[^;:]'

    # def t_role_END(self, t):
    #     ur"\."
    #     t.lexer.begin('INITIAL')
    #     return t

    def t_error(self, t):
        self._log.error("Illegal character '%s'" % t.value[0])

    t_ignore = ""

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

    def find_new_positions(self, data):
        text = []
        tok = None
        self.lexer.input(data)
        while True:
            try:
                tok = self.lexer.token()
            except ply.lex.LexError:
                msg = "ERROR: %s" % "".join(text)
                raise common.ParserException(msg)
            if not tok:
                break
            if tok.type == 'TEXT':
                text.append(tok.value)


class Parser(object):
    def __init__(self, text):
        text = filters.delete_modificacion_duracion(text)
        text = filters.delete_dni(text)
        self.role = None
        self.name = ""
        self.roles = []
        self.state = None
        self.states = ('ROLE')
        self.lex = Lexer()
        self.lex.build()
        self.lex.lexer.input(text)
        while self._process_token():
            pass
        if self.name:
            self._add_role()

    def _process_token(self):
        tok = self.lex.lexer.token()
        if tok:
            if tok.type in self.states:
                self._set_state(tok)
            else:
                self._set_tok(tok)
        return bool(tok)

    def _set_state(self, tok):
        if self.name:
            self._add_role()
        self.state = tok.type
        self.role = tok.value

    def _set_tok(self, tok):
        if self.state != 'ROLE' or tok.type == 'ROLE' or not self.role:
            raise common.ParserException("Wrong token order.")
        if tok.type == 'TEXT':
            self.name += tok.value
        elif tok.type == 'SEPARATOR' and self.name:
            self._add_role()

    def _add_role(self):
        rolekey = self._rolekey()
        role = position[rolekey]
        name = self.name.strip().strip('.')
        self.roles.append((role, name))
        self.name = ""

    def _rolekey(self):
        rolekey = self.role[:-1].upper()
        rolekey = rolekey.replace('V- ', 'V-')
        return rolekey

    def to_dict(self):
        return {"roles": self.roles}

    def to_str(self):
        result = ""
        for role in self.roles:
            result += role[0] + "\t" + role[1] + "\n"
        return result


if __name__ == "__main__":
    n = u"Consejero: BARTOLOME SANZ MARIA VICTORIA;BARTOLOME SANZ SONIA;BARTOLOME SANZ EUGENIO;BARTOLOME SANZ MARIA JOSE;BARTOLOME SANZ MARIA ELENA;BARTOLOME SANZ GINES. Presidente: BARTOLOME SANZ EUGENIO. Secretario: BARTOLOME SANZ MARIA VICTORIA. Cons.Del.Man: BARTOLOME SANZ MARIA VICTORIA;BARTOLOME SANZ SONIA;BARTOLOME SANZ EUGENIO;BARTOLOME SANZ MARIA JOSE;BARTOLOME SANZ MARIA ELENA;BARTOLOME SANZ GINES."
    nombramiento = n
    # m = Lexer()
    # m.build()
    # m.test(nombramiento)
    print Parser(nombramiento).to_str()
