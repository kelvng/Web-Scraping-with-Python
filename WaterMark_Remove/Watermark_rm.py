import fnmatch
import os
import aspose.words as aw
source_path = r"H:\PycharmProjects\Source\WaterMark_Remove\Input"
dest_path = r"H:\PycharmProjects\Source\WaterMark_Remove\Output"

# for in_file in os.listdir(source_path):
#     print("remnove")
#     if fnmatch.fnmatch(in_file,'*.rtf'):
#         doc = aw.Document(source_path+in_file)
#         out_name = os.path.splitext(in_file)[0]  # get file name only
#         print (out_name) # print the file name
#
#         doc.watermark.remove() #remove the watermark
#         print("remnove")
#         doc.save(dest_path+out_name+".pdf", aw.SaveFormat.PDF)

# def remove_watermark_text(doc) :
#
#     for hf in doc.get_child_nodes(aw.NodeType.HEADER_FOOTER, True) :
#         hf = hf.as_header_footer()
#         print("remnove")
#         for shape in hf.get_child_nodes(aw.NodeType.SHAPE, True) :
#             shape = shape.as_shape()
#             print("remnove")
#             if shape.name.find("WaterMark") >= 0 :
#                 shape.remove()
#                 print("remnove")
#     doc.save(r'H:\PycharmProjects\Source\WaterMark_Remove\Output\6664888426_20200417_092255.pdf')
# doc = aw.Document(r'H:\PycharmProjects\Source\WaterMark_Remove\Input\6664888426_20200417_092255.pdf')
# remove_watermark_text(doc)

from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_
def remove_watermark(wm_text, inputFile, outputFile):


    with open(inputFile, "rb") as f:
        source = PdfFileReader(f, "rb")
        output = PdfFileWriter()

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]

                    if isinstance(text, str) and text.startswith(wm_text):
                        operands[0] = TextStringObject('')

            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        with open(outputFile, "wb") as outputStream:
            output.write(outputStream)


wm_text = 'www.facebook.com/hoc247.net'
inputFile = r'H:\PycharmProjects\Source\WaterMark_Remove\Input\10734132448_20220405_173301.pdf'
outputFile = r"H:\PycharmProjects\Source\WaterMark_Remove\Output\10734132448_20220405_173301.pdf"
remove_watermark(wm_text, inputFile, outputFile)