#!/usr/bin/env python
import logging
import docx2txt
from zipfile import ZipFile
# from pptx import Presentation
from subprocess import Popen, PIPE, STDOUT
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
            text = ""
            return text
            self.logger.error(
                "Failed to DOCX to text: " + str(e))

    def convert_doc_to_txt(self, path):
        """
        A very simple conversion function
        which returns text for parsing.

        path = The path to the file
        """
        try:
            cmd = ['antiword', path]
            p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            stdout, stderr = p.communicate()
            return stdout.decode('ascii', 'ignore')
        except Exception as e:
            text = ""
            return text
            self.logger.error(
                "Failed to DOC to text: " + str(e))

    # def convert_pptx_to_txt(self, path):
    #     prs = Presentation(path)
    #     # text_runs will be populated with a list of strings,
    #     # one for each text run in presentation
    #     text_runs = ""
    #     try:
    #         for slide in prs.slides:
    #             try:
    #                 for shape in slide.shapes:
    #                     if not shape.has_text_frame:
    #                         continue
    #                     for paragraph in shape.text_frame.paragraphs:
    #                         for run in paragraph.runs:
    #                             text_runs += str(run.text) + ' '
    #             except:
    #                 pass
    #         return text_runs
    #     except Exception as e:
    #         if text_runs:
    #             return text_runs
    #         else:
    #             text_runs = ""
    #             return text_runs
    #         self.logger.error("Failed to convert pptx: " + str(e))

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
            text = ""
            return text
            self.logger.error(
                "Failed to PDF to text: " + str(e))

    def convert_Xlsx_to_Csv(self, path):
        # Using the Xlsx2csv tool seemed easy and was in python anyhow
        # it also supported custom delim :)
        self.logger.debug("convert_Xlsx_to_Csv on file: " + str(path))
        try:
            cmd = ['xlsx2csv', path]
            p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            stdout, stderr = p.communicate()
            text = stdout.decode('ascii', 'ignore')
            return text
        except Exception as e:
            text = ""
            return text
            self.logger.error(
                "Failed to convert_Xlsx_to_Csv to text: " + str(e))

    def convert_zip_to_text(self, path, rawtext=True):
        # http://stackoverflow.com/questions/10908877/extracting-a-zipfile-to-memory
        try:
            self.logger.debug("Attempting to unzip file: " + str(path))
            input_zip = ZipFile(path)
            if rawtext:
                text = ""
                a = {name: input_zip.read(name) for name in input_zip.namelist()}
                for x in a:
                    try:
                        text += str(a[x])
                    except Exception as e:
                        print e
                        # pass
                self.logger.debug("Unzip of file complted (raw text): " + str(path))
                return text
            else:
                return {name: input_zip.read(name) for name in input_zip.namelist()}
        except Exception as e:
            print e
            text = ""
            return text
            self.logger.error(
                "Failed unzip file: " + str(e))