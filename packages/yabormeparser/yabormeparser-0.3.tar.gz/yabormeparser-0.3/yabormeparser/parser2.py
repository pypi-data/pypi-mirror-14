#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import optparse
import os.path
import parser
import logging
from . import loggingopt
from . import annoucement


RAW_FILE_VERSION = parser.RAW_FILE_VERSION
# Thousands file version. Represent the file version part corresponding to this
# parser (parser2)
TH_FILE_VERSION = u"7"
# The file version depends on parser one and parser two. It is coded to avoid
# that the parser I change and the parser II does not.
FILE_VERSION = u"%i" % (int(RAW_FILE_VERSION) + 1000 * int(TH_FILE_VERSION))


class ExceptionVersion(Exception):
    pass


class Parser2(object):

    def __init__(self, raw_file, patch_file=None):
        self._log = logging.getLogger(__name__)
        self.raw_file = raw_file
        self.doc = None
        self.error_annoucements = []

        p = parser.Parser()
        fp = open(raw_file, "rb")
        p.load_json(fp)
        doc = p.document
        if patch_file:
            patch = self.load_json_patch(patch_file)
            doc = self._patch(doc, patch)
        doc = self._version(doc)
        doc = self._annoucements(doc)
        doc = self._date(doc)
        doc = self._delete_toc(doc)
        self.document = doc

    def write_result(self):
        base = self.raw_file[:-len(".RAW.json")]
        result = ""
        if self.error_annoucements:
            patch_file = self._get_file(base + ".patch.TMP")
            self.save_skeleton(patch_file)
            result = patch_file.name
        else:
            json_file = self._get_file(base + ".json")
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

    def save_skeleton(self, fp):
        self._save_json(fp, self.error_annoucements)

    def save_result(self, fp):
        self._save_json(fp, self.document)

    def _save_json(self, fp, obj):
        json.dump(obj, fp, sort_keys=True,
                  indent=4, separators=(',', ': '))

    def load_json_patch(self, file_name):
        fp = open(file_name, "rb")
        patch = json.load(fp)
        return patch

    def _patch(self, doc, patch):
        patch.reverse()
        correction = None
        if patch:
            correction = patch.pop()
        for p in doc["pages"]:
            for act in p:
                for ann in act["annoucements"]:
                    if ((correction and
                         act["code"] == correction["code"] and
                         ann["label"] == correction["label"])):
                        ann["value"] = correction["value"]
                        correction = None
                        if patch:
                            correction = patch.pop()
        return doc

    def _annoucements(self, doc):
        for p in doc["pages"]:
            for ac in p:
                for an in ac["annoucements"]:
                    try:
                        d = annoucement.parser.process(an["label"],
                                                       an["value"])
                        if d:
                            an.pop("value")
                            for k in d:
                                an[k] = d[k]
                    except annoucement.common.ParserException as e:
                        error = {
                            "label": an["label"],
                            "value": an["value"],
                            "error": unicode(e),
                            "code": ac["code"]
                        }
                        self._log.error("Annoucement parser. " + str(error))
                        self.error_annoucements.append(error)
        return doc

    def _version(self, doc):
        if doc['raw_version'] != RAW_FILE_VERSION:
            raise ExceptionVersion("Raw version: %s. Needed: %s." %
                                   (doc['raw_version'], RAW_FILE_VERSION))
        doc['version'] = FILE_VERSION
        return doc

    def _date(self, doc):
        """ -- PDF Metadata --
        'creation_date': 'D:20131211134125+01'00'',
        'mod_date': 'D:20131211144732+01'00'',
        CreationDate:   Wed Dec 11 13:41:25 2013
        ModDate:        Wed Dec 11 14:47:32 2013"""
        doc['creation_date'] = self._process_date(doc['creation_date'])
        doc['mod_date'] = self._process_date(doc['mod_date'])
        return doc

    def _delete_toc(self, doc):
        doc.pop('toc')
        return doc

    def _process_date(self, text):
        year, month, day = int(text[2:6]), int(text[6:8]), int(text[8:10])
        hour, minut, sec = int(text[10:12]), int(text[12:14]), int(text[14:16])
        return "%04i-%02i-%02i %02i:%02i:%02i" % (year, month, day, hour,
                                                  minut, sec)


def main():
    parser_o = optparse.OptionParser()
    parser_o.add_option('-i', '--inputfile', help='Input file')
    parser_o.add_option('-p', '--patch', help='Patch file')
    loggingopt.optparse_logging(parser_o)
    (options, args) = parser_o.parse_args()
    if not options.inputfile:
        parser_o.error('Input file not given.')
    json_raw_file = options.inputfile
    patch_file = options.patch
    parser2 = Parser2(raw_file=json_raw_file, patch_file=patch_file)
    result = parser2.write_result()
    print "Saved in %s" % result


if __name__ == "__main__":
    main()
