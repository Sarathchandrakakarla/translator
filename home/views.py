from django.shortcuts import render,redirect
from .models import HotelForm
import google.generativeai as genai
import os
from PIL import Image
from django.templatetags.static import static
import pytesseract
from PIL import Image
from deep_translator import GoogleTranslator
from googletrans import LANGUAGES

# Create your views here.
def index(request):
    return render(request, 'index.html')

def scan(request):
    languages=list(LANGUAGES.values())
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
 
        if form.is_valid():
            form.save()
            out_lang =  request.POST['To_Lang']
            img_name = request.FILES['Image'].name
            key='AIzaSyAEZDvFV5ItWN_E4n_dE3SYZ5ZR88KCudk'
            genai.configure(api_key=key)
            generation_config={"temperature":0.9,"top_p":1,"top_k":1,"max_output_tokens":2048}
            model=genai.GenerativeModel("gemini-pro-vision",generation_config=generation_config)
            image=Image.open("C:/Users/Admin/Desktop/OCR/translator/static/img/"+str(img_name))
            response=model.generate_content(["give me the language present in the text.give me only the ISO-639 code of the language",image],stream=True)
            response.resolve()
            detected_lang=response.text
            detected_lang=detected_lang.replace(" ","")
            if detected_lang=="ta":
                lang="tam"
            elif detected_lang=="hin":
                detected_lang="hindi"
                lang="hindi"    
            else:
                lang=detected_lang
            pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
            image = Image.open("C:/Users/Admin/Desktop/OCR/translator/static/img/"+img_name)
            text_from_image = pytesseract.image_to_string(image, lang=lang)
            translated_text=GoogleTranslator(source=detected_lang, target=list(LANGUAGES.keys())[languages.index(out_lang)]).translate(text_from_image)

            return render(request, 'scan.html', {'form': form,'Languages':languages,'Translated_Text':translated_text})
    else:
        form = HotelForm()
    return render(request, 'scan.html', {'form': form,'Languages':languages})