from .models import User_Profile
from pdf2image import convert_from_path
from OCR import settings
from django.shortcuts import render
from .forms import Profile_Form
import io
import os
import time
import pytesseract
from PIL import Image
from gtts import gTTS
from wand.image import Image as wi
import numpy as np
import cv2
poppler_path = r'D:\poppler\bin'
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
FILE_TYPES = ['png', 'jpg', 'jpeg', 'pdf']
Image_type=['png', 'jpg', 'jpeg']

def get_form(request):
    form = Profile_Form()
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.upload = request.FILES['upload']
            file_type = user_pr.upload.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in FILE_TYPES:
                return render(request, 'error.html')
            user_pr.save()
            # PDF STARTS HERE
            if file_type=='pdf':
                pdf_file = "C:/Google Drive/Project/SEM 3/Working/OCR/" + user_pr.upload.url
                pdf = wi(filename=pdf_file, resolution=100)
                pdfImage = pdf.convert('jpeg')
                imageBlobs = []
                originaltext = ''
                for img in pdfImage.sequence:
                    imgPage = wi(image=img)
                    imageBlobs.append(imgPage.make_blob('jpeg'))
                for imgBlob in imageBlobs:
                    im = Image.open(io.BytesIO(imgBlob))
                    text = pytesseract.image_to_string(im, lang='eng')
                    originaltext += text
                    #saving file from here
                    t = time.localtime()
                    timestamp = time.strftime('%b-%d-%Y_%H_%M_%S', t)
                    outfile = "PDF_" + str(timestamp) + ".rtf"
                    f = open(outfile, "a")
                    f.write(originaltext)
                    f.close()
                    print(timestamp)
                audio = gTTS(text=text, lang='en', slow=False)
                audioname="audio_"+str(timestamp) + ".mp3"
                audiopath = os.path.abspath(audioname)
                print(audiopath)
                audio.save(audioname)
                return render(request, 'details.html', {'user_pr': user_pr,'file_data':originaltext,'audio':audiopath})
            # PDF ENDS HERE
            # IMAGE STARTS HERE
            if file_type in Image_type:
                path="C:/Google Drive/Project/SEM 3/Working/OCR/" +user_pr.upload.url
                # im = Image.open(path)
                im=cv2.imread(path)
                text = pytesseract.image_to_string(im, lang='eng')
                t = time.localtime()
                timestamp = time.strftime('%b-%d-%Y_%H_%M_%S', t)
                outfile = "IMAGE_" + str(timestamp) + ".txt"
                f = open(outfile, "a")
                f.write(text)
                # print(text)
                audio = gTTS(text=text, lang='en', slow=False)
                # audioname = "audio_" + str(timestamp) + ".mp3"
                # audiopath = os.path.abspath(audioname)
                audioname = "audio_" + str(timestamp) + ".mp3"
                audiopath = os.path.join(settings.MEDIA_ROOT, audioname)
                #audiopath="C:/Google Drive/Project/SEM 3/Working/OCR/audio_Oct-26-2020_12_12_21.mp3"
                print(audiopath)

                audio.save(audiopath)
                return render(request, 'details.html',{'user_pr': user_pr,'file_data':text,'audio':audioname})
    context = {"form": form}
    return render(request, 'create.html', context)



