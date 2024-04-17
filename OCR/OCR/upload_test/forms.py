from django import forms
from .models import User_Profile

#DataFlair #File_Upload
class Profile_Form(forms.ModelForm):

    class Meta:
        model = User_Profile
        # fields = [
        # 'fname',
        # 'lname',
        # 'technologies',
        # 'email',
        # 'display_picture'
        # ]
        fields=['upload']
        labels = {'upload':('Upload File(Allowed files: .jpg, .jpeg, .png, .pdf)'),
        }