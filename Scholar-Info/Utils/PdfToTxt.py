from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import os


# PDF转为Txt 利于内容提取
def ParsePdfToTxt(filename):
    """
    pdf文档转化为txt文本
    :param filename: pdf文件路径
    :return: 同名txt文本
    """
    file = open(filename, 'rb')
    parser = PDFParser(file)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    txt_name = os.path.basename(filename).split('.')[0] + '.txt'
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrc = PDFResourceManager()
        params = LAParams()
        device = PDFPageAggregator(rsrc, laparams=params)
        interpreter = PDFPageInterpreter(rsrc, device)
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    text = x.get_text()
                    print(text)
                    with open(f'txt/{txt_name}', 'a', encoding='utf-8') as f:
                        f.write(text)
    file.close()


def ParseWordDocToTxt(filename):
    print(filename)
