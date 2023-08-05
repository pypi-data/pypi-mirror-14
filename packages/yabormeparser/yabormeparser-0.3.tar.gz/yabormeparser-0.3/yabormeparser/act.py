#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import logging

COMPLETE_LINE_MIN_LENGTH = 537.1


class ExceptionAct(Exception):
    def __init__(self, message, code,
                 branch="", company="", register="", wrongtitle=""):
        self.message = message
        self.code = code
        self.branch = branch
        self.company = company
        self.register = register
        self.wrongtitle = wrongtitle

    def __str__(self):
        return "The Act code: **%s** has error: **%s**" % (self.code,
                                                           self.message)


class Text(object):
    """Represents a piece of line with text no bold."""
    def __init__(self, text):
        self._text = text

    def get_str(self):
        return "[T:%s]" % self._text

    def text(self):
        return self._text


class BoldText(Text):
    def __init__(self, text):
        Text.__init__(self, text)
        self.line_length = 0
        self.is_complete_line_bold = False

    """Represents a piece of line with text bold."""
    def get_str(self):
        return "[B:%s]" % self._text


class SpecialSpace(object):
    """Represents a new line or a Space"""
    def __init__(self):
        pass

    def get_str(self):
        return "[N]"


class Parser(object):
    """Reads a list of objects and returns a JSON"""
    def __init__(self, texts, patched_acts):
        self._log = logging.getLogger(__name__)
        self.annoucement_types = {
            u"Revocaciones": self._get_simple,
            u"Reelecciones": self._get_simple,
            u"Nombramientos": self._get_simple,
            u"Ceses/Dimisiones": self._get_simple,
            u"Cancelaciones de oficio de nombramientos": self._get_simple,
            u"Sociedad unipersonal": self._get_bold,
            u"Pérdida del caracter de unipersonalidad": self._get_null,
            u"Empresario Individual": self._get_simple,
            u"Declaración de unipersonalidad": self._get_bold,
            # self._get_bold_simple,
            u"Reducción de capital": self._get_simple,
            u"Emisión de obligaciones": self._get_simple,
            u"Ampliación de capital": self._get_simple,
            u"Reapertura hoja registral": self._get_null,
            u"Situación concursal": self._get_simple,
            u"Constitución": self._get_simple,  # u"Constitución de sociedad",
            u"Convocatoria de Junta": self._get_simple,
            u"Extinción": self._get_simple_or_null,
            u"Disolución": self._get_simple,
            u"Fusiones y absorciones de empresas": self._get_simple,
            u"Fusión por absorción": self._get_simple,
            u"Depósitos de proyectos de fusión por absorción":
            self._get_simple,
            u"Transformación de sociedad.": self._get_simple,
            u"Modificaciones estatutarias": self._get_simple,
            u"Cambio de objeto social": self._get_simple,
            u"Cambio de domicilio social": self._get_simple,
            u"Cambio de denominación social": self._get_simple,
            u"Ampliacion del objeto social": self._get_simple,
            u"Otros anuncios y avisos legales ": self._get_simple,
            u"Otros conceptos": self._get_simple,
            u"Fe de erratas": self._get_simple,
            u"Datos registrales": self._get_simple,
            # This are not in the original list.
            u"Escisión total": self._get_bold_and_simple,
            u"Desembolso de dividendos pasivos": self._get_simple,
            u"Página web de la sociedad": self._get_simple,
            u"Articulo 378.5 del Reglamento del Registro Mercantil":
            self._get_simple,
            u"Cesión global de activo y pasivo": self._get_simple,
            u"Transformación de sociedad": self._get_simple,
            u"Primera sucursal de sociedad extranjera": self._get_simple,
            u"Reactivación de la sociedad (Art. 242 del" +
            u" Reglamento del Registro Mercantil)": self._get_null,
            u"Escisión parcial": self._get_simple,
            u"Suspensión de pagos": self._get_simple,
            u"Modificación de poderes": self._get_simple,
            u"Quiebra": self._get_simple,
            u"Fusión por unión": self._get_simple,
            u"Sucursal": self._get_simple,
            u"Segregación": self._get_simple,
            u"Apertura de sucursal": self._get_simple,
            u"Adaptación Ley 2/95": self._get_null,
            u"Primera inscripcion (O.M. 10/6/1.997)": self._get_simple,
            u"Adaptación de sociedad": self._get_null,
            u"Modificación de duración": self._get_simple,
            u"Cierre provisional hoja registral art. 137.2 Ley " +
            u"43/1995 Impuesto de Sociedades": self._get_null,
            u"Crédito incobrable": self._get_null,
            u"Cierre de Sucursal": self._get_null,
            u"Cierre provisional hoja registral por baja en el índice de" +
            u" Entidades Jurídicas": self._get_null,
            u"Cierre provisional hoja registral por revocación del NIFde" +
            u" Entidades Jurídicas": self._get_null,
            u"Cierre provisional de la hoja registral por revocación del NIF":
            self._get_null,
            u"Acuerdo de ampliación de capital social sin ejecutar." +
            u" Importe del acuerdo": self._get_simple,
            u"Adaptada segun D.T. 2 apartado 2 Ley 2/95": self._get_null
        }
        if not texts:
            self._log.error("Instanced parser void")
            return
        self._index = 0
        self.annoucements = []
        self._texts = texts
        self.code = "UNKNOWN"
        self._clean_special_spaces()
        code, company, branch, register = self._get_title()
        self._log.debug("ACT: ----------- CODE: %s ------------ TITLE: %s"
                        % (code, company))
        self._index += 1
        self.code = code
        self.company = company
        self.branch = branch
        self.register = register
        self.embedded_act = self._get_embedded_act()
        texts_wo_emb = texts[:len(texts) - len(self.embedded_act)]
        self._texts = self._get_texts_without_new_lines(texts_wo_emb)
        self._index = 0
        # if code in ["247808"]:
        #    return get_annoucements_ --> indicate it is manual filling.
        if patched_acts and code in patched_acts:
            self._log.info("Patched act: %s" % code)
            act = patched_acts[code]
            self.annoucements = act["annoucements"]
            self.branch = act["branch"]
            assert self.code == act["code"]
            self.company = act["company"]
            self.register = act["register"]
        else:
            self._get_annoucements()

    def _clean_special_spaces(self):
        while type(self._texts[self._index]) == SpecialSpace:
            self._index += 1

    def get_json(self):
        return self.company

    def _is_title(self, index):
        rich_text = self._texts[index]
        if type(rich_text) != BoldText:
            return False
        if not rich_text.is_complete_line_bold:
            return False
        expression = ur'^(\d+) - .+$'
        res = re.search(expression, rich_text.text())
        if not res:
            return False
        code = res.group(1)
        self._log.info("There is a embebbed title with code: %s" % code)
        return True

    def _is_next_line_parted_title(self, index):
        rich_text = self._texts[index]
        # if rich_text.line_length < COMPLETE_LINE_MIN_LENGTH:
        #    return False
        if index + 2 >= len(self._texts):
            return False
        index += 1
        rich_text = self._texts[index]
        assert type(rich_text) == SpecialSpace
        index += 1
        rich_text = self._texts[index]
        if type(rich_text) != BoldText:
            return False
        if not rich_text.is_complete_line_bold:
            return False
        text = rich_text.text()
        label = self._test_label_special_case(text)
        if label:
            return False
        expression = ur'^\s*([\/\s\w]+)[\.:]\s*(.*)\s*$'
        pattern = re.compile(expression, re.UNICODE)
        res = pattern.search(text)
        if res:
            label = self._space_uniq(res.group(1).strip())
            if label in self.annoucement_types:
                return False
        return True

    def _get_title(self):
        """ Extract the title info in a act.

        This module was degenerating to a mesh because of several workarounds
        that were done to fix special cases. It would be nice fix this by
        refactoring."""
        code = ""
        company = ""
        register = ""
        branch = ""  # sucursal bancaria
        # Parse the act title. There are two types of titles.
        text = self._texts[self._index]
        # assert type(text) == BoldText
        if type(text) != BoldText:
            raise ExceptionAct('Title is not bold', self.code)
        # text.is_complete_line_bold, text.line_length
        title = text.text()
        expression = ur'^(\d+) - .+$'
        res = re.search(expression, title)
        if not res:
            raise ExceptionAct('Title format is not: %s' % expression,
                               self.code, wrongtitle=title)
        code_first_line = res.group(1)
        while self._is_next_line_parted_title(self._index):
            # Pattern like the first line?
            self._index += 1
            assert type(self._texts[self._index]) == SpecialSpace
            self._index += 1
            rich_text = self._texts[self._index]
            line = rich_text.text()
            assert type(text) == BoldText
            expression = ur'^(\d+) - (.+)$'
            res = re.search(expression, line)
            if res:
                code_other_line = res.group(1)
                assert code_first_line == code_other_line
                # title += " " + res.group(2)
                branch = res.group(2)
            else:
                title += " " + line
        # 532404 - SIGUEME, GESTION SL(R.M. SANTIAGO DE COMPOSTELA).
        expression = ur'^(\d+) - (.*)\((.*)\)\.$'
        res = re.search(expression, title)
        if res:
            code = res.group(1)
            company = res.group(2)
            register = res.group(3)
        else:
            # 532404 - SIGUEME, GESTION SL
            # or
            # 532404 - SIGUEME, GESTION SL.
            expression = ur'^(\d+) - (.*)$'
            res = re.search(expression, title)
            assert res
            code = res.group(1)
            company = res.group(2)
            register = ""
        return (code, company, branch, register)

    def _get_embedded_act(self):
        embedded_texts = []
        begin_emb = 0
        is_embedded = False
        for i in range(self._index, len(self._texts)):
            if self._is_title(i):
                is_embedded = True
                begin_emb = i
                break
        if is_embedded:
            self._log.info("There is a embedded act")
            embedded_texts = self._texts[begin_emb:]
        return embedded_texts

    def _get_bold_text_without_new_lines(self, texts):
        result = ""
        while self._index < len(texts):
            t = texts[self._index]
            if type(t) == SpecialSpace:
                self._index += 1
                result += " "
            elif type(t) == BoldText:
                self._index += 1
                result += t.text()
            if type(t) == Text:
                break
        return BoldText(result)

    def _get_unbold_text_without_new_lines(self, texts):
        result = ""
        while self._index < len(texts):
            t = texts[self._index]
            if type(t) == SpecialSpace:
                self._index += 1
                result += " "
            elif type(t) == Text:
                self._index += 1
                result += t.text()
            if type(t) == BoldText:
                break
        return Text(result)

    def _get_texts_without_new_lines(self, texts):
        texts_wo_nl = []
        while self._index < len(texts):
            t = texts[self._index]
            if type(t) == SpecialSpace:
                self._index += 1
            elif type(t) == BoldText:
                texts_wo_nl += [self._get_bold_text_without_new_lines(texts)]
            elif type(t) == Text:
                texts_wo_nl += [self._get_unbold_text_without_new_lines(texts)]
        return texts_wo_nl

    def _test_label_special_case(self, label):
        result = ""
        # Special cases. With dot (.) in the middle.
        ###
        labels = [u"Articulo 378.5 del Reglamento del Registro Mercantil. ",
                  (u"Reactivación de la sociedad (Art. 242 del " +
                   u"Reglamento del Registro Mercantil). "),
                  u"Primera inscripcion (O.M. 10/6/1.997). ",
                  (u"Cierre provisional hoja registral art. 137.2 Ley " +
                   u"43/1995 Impuesto de Sociedades. "),
                  (u"Acuerdo de ampliación de capital social sin ejecutar." +
                   u" Importe del acuerdo: "),
                  u"Adaptada segun D.T. 2 apartado 2 Ley 2/95. "]
        for l in labels:
            if label[:len(l)] == l:
                result = l[:-2]
                if len(l) < len(label):
                    trail = label[len(l):]
                    self._log.error("TRAIL(SC): " + trail)
                    self._index -= 1
                    self._texts[self._index] = BoldText(trail)
                break
        return result

    def _parse_semicolon(self, text):
        label = ""
        value = ""
        expression = ur'^\s*([\/\s\w]+)[\.:]\s*(.*)\s*$'
        pattern = re.compile(expression, re.UNICODE)
        res = pattern.search(text)
        if res:
            label = self._space_uniq(res.group(1).strip())
            value = unicode(res.group(2))
        return label, value

    def _get_annoucement(self):
        # Get Label
        label = u''
        value = u''
        label_aux = u''
        rich_text = self._texts[self._index]
        self._index += 1
        self._log.debug("_get_annoucement: %s", rich_text.text())
        if type(rich_text) == Text:  # A label not Bold is a exception
            label_aux, trail = self._parse_semicolon(rich_text.text())
            if trail:
                self._log.error("TRAIL(Text): " + trail)
                self._index -= 1
                self._texts[self._index] = Text(trail)
        else:  # BoldText
            assert type(rich_text) == BoldText
            text = rich_text.text()
            label_aux = self._test_label_special_case(text)
            if not label_aux:
                label_aux, trail = self._parse_semicolon(text)
                if label_aux:
                    if trail:
                        self._log.error("TRAIL(BoldText): " + trail)
                        self._index -= 1
                        self._texts[self._index] = BoldText(trail)
                else:
                    self._log.error("NO REGEXP MATCH: %s" % text)
        if label_aux in self.annoucement_types:
            label = label_aux
            value = self.annoucement_types[label]()
        else:
            message = "UNKNOWN LABEL: %s" % rich_text.text()
            raise ExceptionAct(message, self.code,
                               self.branch, self.company, self.register)
        if value is not None:
            value = value.strip()
        self.annoucements.append({u'label': label, u'value': value})

    def _space_uniq(self, text):
        return " ".join([i for i in text.split(" ") if i != ""])

    def _get_annoucements(self):
        while self._index < len(self._texts):
            self._get_annoucement()

    def get_str(self):
        result = "Code: %s\n" % self.code
        result += "Company: %s\n" % self.company
        result += "Branch: %s\n" % self.branch
        result += "Register: %s\n" % self.register
        result += "Annoucements:\n"
        for a in self.annoucements:
            result += str(a) + "\n"
        return result

    def get_act(self):
        return self._get_act(self.code, self.company, self.branch,
                             self.register, self.annoucements)

    def get_empty_act(self):
        annoucements = [{"label": "", "value": ""}, {"label": "", "value": ""}]
        return self._get_act("", "", "", "", annoucements)

    def _get_act(self, code, company, branch, register,
                 annoucements):
        return {
            u'code': code,
            u'company': company,
            u'branch': branch,
            u'register': register,
            u'annoucements': annoucements
        }

    def _get_null(self):
        pass

    def _get_simple(self):
        rich_text = self._texts[self._index]
        self._index += 1
        assert type(rich_text) == Text
        return rich_text.text()

    def _get_simple_or_null(self):
        rich_text = self._texts[self._index]
        self._index += 1
        if type(rich_text) == Text:
            return rich_text.text()
        else:
            self._index -= 1

    def _get_bold(self):
        rich_text = self._texts[self._index]
        assert type(rich_text) == BoldText
        text = rich_text.text()
        # get out text to return
        parts = text.split(".")
        result = parts[0]
        is_trailed = False
        trailed_text = ""
        for i in range(1, len(parts)):
            if parts[i].strip():
                test_key = parts[i].strip()
                if test_key[-1] == ":":
                    test_key = test_key[:-1]
                if test_key in self.annoucement_types or is_trailed:
                    is_trailed = True
                    trailed_text += parts[i]
                    if i < len(parts) - 1:
                        trailed_text += "."
                else:
                    result += "." + parts[i]
        if is_trailed:
            self._texts[self._index] = BoldText(trailed_text)
        else:
            self._index += 1
        return result

    def _get_bold_and_simple(self):
        rich_text = self._texts[self._index]
        assert type(rich_text) == BoldText
        text = rich_text.text()
        # get out text to return
        parts = text.split(".")
        result_bold = parts[0]
        if (len(parts) > 1 and parts[1].strip()):
            self._texts[self._index] = BoldText(parts[1] + ".")
        else:
            self._index += 1
        rich_text = self._texts[self._index]
        self._index += 1
        assert type(rich_text) == Text
        result_simple = rich_text.text()
        return result_bold + result_simple
