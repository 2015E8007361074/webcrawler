# coding:utf-8
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open


def read_pdf(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laprams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laprams)
    process_pdf(rsrcmgr, device, pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

pdf_file = open("webdav.pdf", 'rb')
output_string = read_pdf(pdf_file)
print(output_string)
pdf_file.close()