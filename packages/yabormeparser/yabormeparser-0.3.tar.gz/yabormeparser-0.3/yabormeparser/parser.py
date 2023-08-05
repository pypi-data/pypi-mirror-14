#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pdfminer import pdfparser
from pdfminer import pdfdocument
from pdfminer import pdfpage
from pdfminer import pdfinterp
from pdfminer import converter
from pdfminer import layout
import optparse
import sys
import os.path
import logging
import json
from . import act
from . import loggingopt


# RAW_FILE_VERSION must be a positive integer string.
# Each new version add 1 if the result file can change.
RAW_FILE_VERSION = u'1'

MARGIN_VERTICAL_FIRST_PAGE = 600
MARGIN_VERTICAL_OTHER_PAGE = 720

BOLD_FONT = "+Arial-BoldMT"  # "AQBJAI+Arial-BoldMT"
BOLD_FONT_SIZE = 11.088
SIMPLE_FONT = "+ArialMT"  # "CGALGD+ArialMT"
SIMPLE_FONT_SIZE = 10.632


def u(unicode_escape_string):
    return unicode_escape_string.decode('unicode-escape')


class ExceptionLayout(Exception):
    pass


class Parser(object):
    """Parser for a BORME file an generate a Document with the info."""

    def __init__(self, borme_file=None, patch_file=None):
        self._log = logging.getLogger(__name__)
        self._following_incomplete_acts = 0
        self._borme_file = borme_file
        self.error_acts = []
        self.patched_acts = {}
        if patch_file:
            self.load_json_patch(patch_file)
        if borme_file:
            doc = self._get_document(borme_file)
            info = doc.info[0]
            self.document = {
                u'raw_version': RAW_FILE_VERSION,
                u'title': u(info['Title']),
                u'subject': u(info['Subject']),
                u'creation_date': u(info['CreationDate']),
                u'mod_date': u(info['ModDate']),
                u'toc': self._get_toc(doc),
                u'pages': self._parse_pages(doc)
            }
            self._assert_metadata(info)
            if not self.error_acts:
                self._assert_toc_equal_doc()

    def save_result(self, fp):
        self._save_json(fp, self.document)

    def save_skeleton(self, fp):
        skl = {}
        act_ = act.Parser("", [])
        company_skl = act_.get_empty_act()
        for error in self.error_acts:
            skl[error["code"]] = company_skl
            company_skl["error"] = error["message"]
            company_skl["code"] = error["code"]
            company_skl["branch"] = error["branch"]
            company_skl["company"] = error["company"]
            company_skl["register"] = error["register"]
        self._save_json(fp, skl)

    def _save_json(self, fp, obj):
        json.dump(obj, fp, sort_keys=True,
                  indent=4, separators=(',', ': '))

    def load_json(self, fp):
        self.document = json.load(fp)
        self._assert_toc_equal_doc()

    def load_json_patch(self, file_name):
        fp = open(file_name, "rb")
        self.patched_acts = json.load(fp)

    def _assert_metadata(self, info):
        assert info['Producer'] == 'iText 2.1.4 (by lowagie.com)'
        # assert (info['Author'] == 'Registro Mercantil' or
        #         u(info['Author']) == u'Boletín Oficial del Estado' or
        #         info['Author'] == 'Registro Mercantil. LA RIOJA')
        # It has a lot of possibilites... (Illes balears...)
        assert (info['Creator'] == 'eBOE' or
                u(info['Creator']) == u'Boletín Oficial del Estado')
        assert ('Trapped' not in info or
                str(info['Trapped']) == '/False')

    def _get_document(self, my_file):
        """Returns a PDFDocument from a file name."""
        fp = open(my_file, "rb")
        parser = pdfparser.PDFParser(fp)
        return pdfdocument.PDFDocument(parser)

    def _get_toc(self, document):
        """Returns a list of page, title dictionaries."""
        toc = []
        # enumerate(doc.get_pages()))
        # I increment it because of error in BORME-A-2009-1-08.pdf
        # sys.setrecursionlimit(2000)  # original 1000
        # More recursion with! BORME-A-2009-200-29.pdf
        sys.setrecursionlimit(4000)  # original 1000
        for outline in document.get_outlines():
            # page is not level. Perhaps dest?
            level, title, dest, a, se = outline
            # dest = self._resolve_dest(dest)
            # pageno = pages[dest[0].objid]
            toc.append({u'objid': dest[0].objid, u'title': title})
        return toc

    def _is_bold_char(self, font, size):
        is_bold = False
        if font[-len(BOLD_FONT):] == BOLD_FONT:
            assert int(size * 100) == int(BOLD_FONT_SIZE * 100)
            is_bold = True
        else:
            assert font[-len(SIMPLE_FONT):] == SIMPLE_FONT
            assert int(size * 100) == int(SIMPLE_FONT_SIZE * 100)
        return is_bold

    def _get_text(self, text, is_bold):
        newText = None
        if is_bold:
            newText = act.BoldText(text)
        else:
            newText = act.Text(text)
        return newText

    def _compress_text(self, text):
        """Seldom justified text is expanded and it is like:
        'U n  E j e m p l o' returns 'Un Ejemplo'"""
        result = text
        was_space = True
        is_expanded = False
        if len(text) > 3:
            is_expanded = True
            for letter in text:
                is_space = (letter == " ")
                if is_space:
                    was_space = True
                else:
                    if was_space:
                        was_space = False
                    else:
                        is_expanded = False
                        break
        if is_expanded:
            result = ""
            eliminate = True
            for letter in text:
                is_space = (letter == " ")
                if is_space and eliminate:
                    eliminate = False
                else:
                    eliminate = True
                    result += letter
        return result

    def _parse_line(self, line):
        """
        Parse a layout horizontal line and returns a list of act.SpecialSpace,
        act.Text and act.BoldText
        """
        box = []
        is_first = True
        is_bold = False
        text = ""
        is_complete_line_bold = True
        reference_to_last_text = None
        if type(line) != layout.LTTextLineHorizontal:
            error = "Not LTTextLineHorizontal"
            raise ExceptionLayout(error)
        for piece in line:
            if type(piece) == layout.LTAnno:
                ltanno = piece.get_text()
                if not (ltanno == "\n" or ltanno == " "):
                    raise ExceptionLayout("LTAnno char ord=%i" %
                                          ord(ltanno))
                # added: and ltanno == "\n" to evitate...
                if text and ltanno == "\n":
                    newText = self._get_text(text, is_bold)
                    if not is_bold:
                        is_complete_line_bold = False
                    box += [newText]
                    reference_to_last_text = newText
                    text = ""
                    is_first = True
                    nl = act.SpecialSpace()
                    box += [nl]
            elif type(piece) == layout.LTChar:
                char, font, size = (piece.get_text(), piece.fontname,
                                    piece.size)
                is_bold_now = self._is_bold_char(font, size)
                if is_first:
                    is_first = False
                    is_bold = is_bold_now
                    text += char
                else:
                    if is_bold == is_bold_now:
                        text += char
                    else:
                        newText = self._get_text(text, is_bold)
                        box += [newText]
                        is_complete_line_bold = False
                        is_bold = is_bold_now
                        text = ""
                        is_first = True
            else:
                err = "PDF element unknow in Line context %s" % type(line)
                raise ExceptionLayout(err)
        if is_complete_line_bold:
            assert type(reference_to_last_text) == act.BoldText
            reference_to_last_text.line_length = line.x1
            reference_to_last_text.is_complete_line_bold = True
        assert not text
        return box

    def _parse_act(self, box_horizontal, is_embedded_act=False):
        # txt = box_horizontal.get_text()
        parts = []
        # self._log.debug("%s [...] %s" % (txt[:20], txt[-18:]))
        if not is_embedded_act:
            for line in box_horizontal:
                aux = self._parse_line(line)
                parts += aux
        else:
            parts = box_horizontal
        act_ = act.Parser(parts, self.patched_acts)
        self._log.debug(act_.get_str().encode('utf-8'))
        return act_

    def _is_a_complete_act(self, box_horizontal):
        is_a_complete_act = False
        try:
            self._parse_act(box_horizontal)
            is_a_complete_act = True
        except act.ExceptionAct:
            self._log.error("Is not a complete act to the page begin." +
                            "\nOr the first act has an error.")
        return is_a_complete_act

    def _mix_acts(self, first, second):
        self._log.info("Mixing part acts because they are in different page.")
        mixed = []
        for item in first:
            mixed.append(item)
        for item in second:
            mixed.append(item)
        return mixed

    def _parse_acts(self, page, next_pages, last_page_act):
        acts = []
        counter = len(page)
        # for box in page:
        # for i in range(0, len(page)):
        is_emb_act = False
        box_index = -1
        while box_index < len(page) - 1:
            box_index += 1
            box = page[box_index]
            counter -= 1
            is_last_act = (counter == 0)
            if not is_emb_act and self._following_incomplete_acts:
                self._following_incomplete_acts -= 1
                continue
            if not is_emb_act and is_last_act and next_pages:
                for j in range(0, len(next_pages)):
                    if self._is_a_complete_act(next_pages[j][0]):
                        break
                    else:
                        self._following_incomplete_acts += 1
                        box = self._mix_acts(box, next_pages[j][0])
                        if len(next_pages[j]) > 1:
                            break
            try:
                act_ = self._parse_act(box, is_embedded_act=is_emb_act)
                is_emb_act = False
                if act_.embedded_act:
                    is_emb_act = True
                    page[box_index] = act_.embedded_act
                    box_index -= 1
                    counter += 1
                act_info = act_.get_act()
                is_branch_act_title_splitted = (not acts and last_page_act
                                                and act_info['code'] ==
                                                last_page_act['code'])

                if is_branch_act_title_splitted:
                    # This happens only if a act has two title with the format
                    # expression = ur'^(\d+) - .+$'. This occurs only in
                    # companies with branchs (sucursales) like banks.
                    assert not last_page_act['branch']
                    assert not last_page_act['annoucements']
                    last_page_act['branch'] = act_info['company']
                    last_page_act['annoucements'] = act_info['annoucements']

                else:
                    acts.append(act_info)
            except act.ExceptionAct as e:
                self.error_acts.append({"code": e.code, "message": e.message,
                                        "branch": e.branch,
                                        "company": e.company,
                                        "register": e.register})
                self._log.error(unicode(e))
                if self._is_a_dispensable_act(e.code,
                                              e.wrongtitle,
                                              is_last_act):
                    self.error_acts.pop()  # This is a very strange case.
        return acts

    def _is_a_dispensable_act(self, code, wrongtitle, is_last_act):
        """Test if is a exception to the title format.

        Seldom, 3 of 46000, times the document ends with a pseudo-act.
        This check that a error is because of this."""
        is_dispensable = False
        # The titles check, maybe is too much... But this is a seldom error and
        # could hide other exceptions
        titles = ("Fe de erratas:",
                  " - SOCIEDAD ESTATAL LOTERIAS Y APUESTAS DEL ESTADO SA.")
        if is_last_act and code == "UNKNOWN" and wrongtitle in titles:
            is_dispensable = True
        return is_dispensable

    def _parse_raw_acts(self, my_layout, is_first_page):
        acts = []
        for lt in my_layout:
            if type(lt) == layout.LTTextBoxHorizontal:
                if self._filter_tex_box_horizontal(is_first_page, lt.x0,
                                                   lt.x1, lt.y0, lt.y1):
                    acts.append(lt)
        return acts

    def _parse_pages(self, document):
        """Return the info extracted for the PDF BORME pages."""
        resource_manager = pdfinterp.PDFResourceManager()
        # value is specified not as an actual length, but as a proportion of
        # the length to the size of each character in question.
        # Two text chunks whose distance is closer than the **char_margin**
        # is considered continuous and get grouped into one.
        # it may be required to insert blank characters (spaces) as necessary
        # if the distance between two words is greater than the
        # **word_margin**.
        # as a blank between words might not be represented as a space, but
        # indicated by the positioning of each word.
        # two lines whose distance is closer than the line_margin is grouped as
        # a text box, which is a rectangular area that contains a "cluster" of
        # text portions.
        # 6.0 --> all without one
        # params = layout.LAParams(char_margin=8.0)
        params = layout.LAParams(char_margin=14.0)
        device = converter.PDFPageAggregator(resource_manager, laparams=params)
        interpreter = pdfinterp.PDFPageInterpreter(resource_manager, device)
        pdf_pages = [page for page in pdfpage.PDFPage.create_pages(document)]
        raw_pages = []
        is_first_page = True
        for page in pdf_pages:
            interpreter.process_page(page)
            my_layout = device.get_result()
            acts = self._parse_raw_acts(my_layout, is_first_page)
            raw_pages.append(acts)
            is_first_page = False
            debug_txt = "Page number: %i Acts: %i" % (len(raw_pages),
                                                      len(acts))
            self._log.debug(debug_txt)

        pages = []
        counter = len(raw_pages)
        for page in raw_pages:
            counter -= 1
            is_last_page = (counter == 0)
            next_pages = []
            if not is_last_page:
                next_pages = raw_pages[(len(raw_pages) - counter):]
            last_page_act = None
            if pages:
                if pages[-1]:
                    last_page_act = pages[-1][-1]
            acts = self._parse_acts(page, next_pages, last_page_act)
            pages.append(acts)
        return pages

    def _filter_tex_box_horizontal(self, is_first_page_, x0, x1, y0, y1):
        """Is the horizontal box (x0, x1, y0, y1) in info zone?."""
        first = MARGIN_VERTICAL_FIRST_PAGE
        other = MARGIN_VERTICAL_OTHER_PAGE
        return x0 == 57.0 and y0 < (first if is_first_page_ else other)

    def _assert_toc_equal_doc(self):
        toc_codes = []
        doc_codes = []
        is_first = True
        for line in self.document['toc']:
            if is_first:
                is_first = False
            else:
                toc_codes.append(line['title'].split()[0])
        for page in self.document['pages']:
            for act_ in page:
                doc_codes.append(act_['code'])
                if act_['branch']:  # If there is 'sucursal' twice the code
                    doc_codes.append(act_['code'])
        # purge bad codes. u'-' appears for title
        # " - SOCIEDAD ESTATAL LOTERIAS Y APUESTAS DEL ESTADO SA."
        # which is purge in the method: _is_a_dispensable_act
        if u'-' in toc_codes:
            toc_codes.remove(u'-')
        assert toc_codes == doc_codes

    def write_result(self):
        parts = self._borme_file.split(".")[:-1]
        base = ".".join(parts)
        result = ""
        if self.error_acts:
            patch_file = self._get_file(base + ".RAW.patch.TMP")
            self.save_skeleton(patch_file)
            result = base + patch_file.name
        else:
            json_file = self._get_file(base + ".RAW.json")
            self.save_result(json_file)
            result = json_file.name
        return result

    def _get_file(self, name):
        counter = 0
        base_name = name
        while os.path.exists(name):
            counter += 1
            name = base_name + "." + str(counter)
        return open(name, "w+")


def main():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--inputfile', help='Input file')
    parser.add_option('-p', '--patch', help='Patch file')
    loggingopt.optparse_logging(parser)
    (options, args) = parser.parse_args()
    if not options.inputfile:
        parser.error('Input file not given.')
    pdf_file = options.inputfile
    patch_file = options.patch
    parser = Parser(borme_file=pdf_file, patch_file=patch_file)
    result = parser.write_result()
    print "Saved in %s" % result


if __name__ == "__main__":
    main()
