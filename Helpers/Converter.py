#!/usr/bin/env python
import helpers
import logging
import docx2txt
from subprocess import Popen, PIPE
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


class Converter(object):

    def __init__(self, verbose=False):
        try:
            self.logger = logging.getLogger("SimplyEmail.Converter")
            self.verbose = verbose
        except Exception as e:
            print e

    def convert_docx_to_txt(self, path):
        """
        A very simple conversion function
        which returns unicode text for
        parsing.

        path = The path to the file
        """
        # https://github.com/ankushshah89/python-docx2txt
        try:
            text = docx2txt.process(path)
            self.logger.debug("Converted docx to text: " + str(path))
            return unicode(text)
        except Exception as e:
            self.logger.debug(
                "Failed to DOCX to text: " + str(e))

    def convert_doc_to_txt(self, path):
        """
        A very simple conversion function
        which returns text for parsing.

        path = The path to the file 
        """
        try:
            cmd = ['antiword', path]
            p = Popen(cmd, stdout=PIPE)
            stdout, stderr = p.communicate()
            return stdout.decode('ascii', 'ignore')
        except Exception as e:
            self.logger.debug(
                "Failed to DOC to text: " + str(e))

    def convert_pdf_to_txt(self, path):
        """
        A very simple conversion function
        which returns text for parsing from PDF.

        path = The path to the file 
        """
        try:
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(
                rsrcmgr, retstr, codec=codec, laparams=laparams)
            fp = file(path, 'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            maxpages = 0
            caching = True
            pagenos = set()
            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                          check_extractable=True):
                interpreter.process_page(page)
            text = retstr.getvalue()
            fp.close()
            device.close()
            retstr.close()
            return text
        except Exception as e:
            self.logger.debug(
                "Failed to PDF to text: " + str(e))

    def convert_Xlsx_to_Csv(self, path):
        # Using the Xlsx2csv tool seemed easy and was in python anyhow
        # it also supported custom delim :)
        self.logger.debug("convert_Xlsx_to_Csv on file: " + str(path))
        try:
            cmd = ['xlsx2csv', path]
            p = Popen(cmd, stdout=PIPE)
            stdout, stderr = p.communicate()
            text = stdout.decode('ascii', 'ignore')
            return text
        except Exception as e:
            self.logger.debug(
                "Failed to convert_Xlsx_to_Csv to text: " + str(e))
