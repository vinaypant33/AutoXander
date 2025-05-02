import os
import sys
import contextlib
import json
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
import tkinter as tk
from tkinter import filedialog
import pdfplumber # For reading the pdf files


from llama_cpp import Llama
import warnings

# Ignroe the warnings : from the 
warnings.filterwarnings('ignore')



def single_chat(current_prompt , number_control = 8192 , verbose_confirm  = False , number_batch  = 128 , number_threads = 8 ):
    llm  = Llama(model_path=r"models\chat_model.gguf" , n_ctx=number_control , verbose=verbose_confirm , n_batch=number_batch , n_threads=number_threads)
    response = llm(current_prompt , max_tokens=512 , stop=["</s>"] )
    return (response['choices'][0]["text"])




def fileOpener():
    file_name  =  filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    ext = os.path.splitext(file_name)[1].lower()
    try:
        if ext == '.txt':
            with open(file_name, 'r', encoding='utf-8') as f:
                return f.read()

        elif ext == '.csv':
            df = pd.read_csv(file_name)
            return df.head(10).to_string()

        elif ext == '.json':
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, indent=2)[:1000]

        elif ext == '.pdf':
            text = ""
            with pdfplumber.open(file_name) as pdf:
                for i, page in enumerate(pdf.pages[:3]):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip() if text else "(No extractable text found in PDF)"

        elif ext == '.docx':
            doc = Document(file_name)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

        else:
            return f"Unsupported file type: {ext}"

    except Exception as e:
        return f"Error parsing file: {e}"
