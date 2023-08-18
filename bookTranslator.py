from googletrans import Translator
from os import chdir, getcwd, listdir, makedirs
from os.path import join,splitext
from docx import Document
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import fitz
import pytesseract
from pytesseract import image_to_string
from PIL import Image
from PyPDF2 import PdfReader
import io
from pdf2image import convert_from_path
import re

current_dir = getcwd()

target_folder = join(current_dir, r"C:\Users\acer\Desktop\test")
print("Target Folder Path:", target_folder)

# List files and subdirectories within a folder
file_list = listdir(target_folder)
print("Files in Target Folder:", file_list)

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
content = ""

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_Language(argument):
    switcher = {
        0: "en",
        6: "hi",
        5: "zh-CN",
        4: "ko",
        3: "ja",
        1: "de"
    }
    return switcher.get(argument, "en")

def getSelection():
    while True:
        try:
            userInput = int(input())
            if userInput < 0 or userInput > 6:
                print("Not an integer! Try again.")
                continue
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput
            break

translator = Translator()

print("0. ENGLISH")
print("6. HINDI")
print("5. Chinese")
print("4. KOREAN")
print("3. JAPANESE")
print("1. GERMAN")
tran = getSelection()
lang = get_Language(tran)
print("Selected Language:", lang)

for i in file_list:
    path = r"C:\Users\acer\Desktop\test\{}".format(i)
    def get_file_extension(path):
        return splitext(path)[1][1:]  # Remove the leading dot
    # Example usage:
    extension = get_file_extension(path)
    #print("File extension:", extension)
    if(extension == 'docx'):
        # Load the Word document
        doc = Document(path)
        # Read the content of the document
        content:str = ''
        page_content = ""
        content = "\n".join([para.text for para in doc.paragraphs])
        page_content += content
        preprocessed_content = re.sub(r'\s+', ' ', page_content).strip
        translated_text = translator.translate(page_content, dest=lang)
        print(translated_text.text)
    else:
        def check_pdf_content(pdf_path):
            has_text = False
            has_images = False
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                # Check if the PDF contains text
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text.strip():  # Check if the extracted text is not empty
                        has_text = True
                        break
                  # Check if the PDF contains images
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                if xObject:
                    for obj in xObject:
                         if xObject[obj]['/Subtype'] == '/Image':
                            has_images = True
                            break
            return has_text, has_images
        if __name__ == "__main__":
            text_present, images_present = check_pdf_content(path)

            if text_present:
                # If the page has text, extract it directly
                with open(path, 'rb') as pdf_file:
                    # Create a PDF reader object
                    pdf = PdfReader(pdf_file)
                    # Get the number of pages in the PDF
                    num_pages = len(pdf.pages)
                    # Extract text from all pages and store it in the 'text' variable
                    
                    for page_num in range(num_pages):
                        page = pdf.pages[page_num]
                        content:str = ''
                        page_content = ""
                        content += page.extract_text()
                        page_content += content
                        preprocessed_content = re.sub(r'\s+', ' ', page_content).strip
                        translated_text = translator.translate(page_content, dest=lang)
                        print(translated_text.text)
                #print("The PDF contains text.")

            elif images_present:
                # Open the PDF file and read its content using PyPDF2
                with open(path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    # Iterate through all pages
                    for page_num in range(len(pdf_reader.pages)):
                        # Convert the page to an image using pdf2image
                        images = convert_from_path(path, first_page=page_num + 1, last_page=page_num + 1, poppler_path = r"C:\Users\acer\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin")
                        # Initialize the page_content variable to store text extracted from this page
                        content:str = ''
                        page_content = ""
                        # Save each image to the output folder
                        for idx, image in enumerate(images):
                            extracted_text = pytesseract.image_to_string(Image.open(join(f"page{page_num + 1}_image{idx + 1}.jpg")))
                            page_content += extracted_text
                            preprocessed_content = re.sub(r'\s+', ' ', page_content).strip
                            translated_text = translator.translate(page_content, dest=lang)
                            print(translated_text.text)
                            #print("Detected Text:", preprocessed_content)
