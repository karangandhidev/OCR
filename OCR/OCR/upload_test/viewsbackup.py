
from django.shortcuts import render
from .forms import Profile_Form
from .models import User_Profile

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import time
from gtts import gTTS

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
                pages = convert_from_path(pdf_file, 500)
                image_counter = 1
                for page in pages:
                    filename = "page_" + str(image_counter) + ".jpg"
                    page.save(filename, 'JPEG')
                    image_counter = image_counter + 1
                filelimit = image_counter - 1
                t = time.localtime()
                timestamp = time.strftime('%b-%d-%Y_%H_%M_%S', t)
                outfile = "PDF_"+str(timestamp) + ".txt"
                f = open(outfile, "a")
                file_data = ""
                for i in range(1, filelimit + 1):
                    filename = "page_" + str(i) + ".jpg"
                    text = str(((pytesseract.image_to_string(Image.open(filename)))))
                    text = text.replace('-\n', '')
                    f.write(text)
                f.close()
                # context = {'data': text}
                print(timestamp)
                audio = gTTS(text=text, lang='en', slow=False)
                audioname="audio_"+str(timestamp) + ".mp3"
                audiopath = os.path.abspath(audioname)
                print(audiopath)
                audio.save(audioname)
                return render(request, 'details.html', {'user_pr': user_pr,'file_data':text,'audio':audiopath})
            # PDF ENDS HERE
            # IMAGE STARTS HERE
            if file_type in Image_type:
                t = time.localtime()
                timestamp = time.strftime('%b-%d-%Y_%H_%M_%S', t)
                outfile = "IMAGE_" + str(timestamp) + ".txt"
                f = open(outfile, "a")
                path="C:/Google Drive/Project/SEM 3/Working/OCR/" +user_pr.upload.url
                # im = Image.open(path)
                im=cv2.imread(path)
                text = pytesseract.image_to_string(im, lang='eng')
                f.write(text)
                print(text)
                audio = gTTS(text=text, lang='en', slow=False)
                audioname = "audio_" + str(timestamp) + ".mp3"
                audiopath = os.path.abspath(audioname)
                print(audiopath)
                audio.save(audioname)
                return render(request, 'details.html',{'user_pr': user_pr,'file_data':text,'audio':audiopath})
    context = {"form": form}
    return render(request, 'create.html', context)
