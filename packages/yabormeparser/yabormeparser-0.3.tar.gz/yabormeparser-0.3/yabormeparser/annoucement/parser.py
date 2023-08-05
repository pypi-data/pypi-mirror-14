#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.lex
import ampliacion_de_capital
import ceses_dimisiones
import constitucion
import nombramientos
import common

_annoucements = {
    u"Ampliación de capital": ampliacion_de_capital,
    u"Ceses/Dimisiones": ceses_dimisiones,
    u"Constitución": constitucion,
    u"Nombramientos": nombramientos
}


def process(label, value):
    annoucement = None
    try:
        if label in _annoucements:
            module = _annoucements[label]
            ann = module.Parser(value)
            annoucement = ann.to_dict()
    except ply.lex.LexError as e:
        raise common.ParserException(e)
    return annoucement
