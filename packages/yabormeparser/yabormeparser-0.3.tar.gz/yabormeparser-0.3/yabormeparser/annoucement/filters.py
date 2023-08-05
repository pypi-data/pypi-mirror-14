#!/usr/bin/python
# -*- coding: utf-8 -*-
import re


def _convert(match):
    ptas = int(match.group(1).replace('.', ''))
    euros = str(round(ptas / 166.39, 2)).replace('.', ',')
    return euros + " Euros."


def ptas_to_euros(text):
    re_ptas = ur'([0-9\.]+)\s+Ptas\.'
    return re.sub(re_ptas, _convert, text)


def delete_modificacion_duracion(text):
    i = text.find(u"Modificación de duración: ")
    if i >= 0:
        text = text[0:i].rstrip()
    return text


def delete_dni(text):
    embedded_dni = ur'\s\:\s*[A-Z]?[0-9]{6,10}[A-Z]?\s*.'
    return re.sub(embedded_dni, '', text)
