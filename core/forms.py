from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Note, UserProfile

# class UserForm(UserCreationForm):
#     class Meta:
#         model = UserProfile
#         fields = []
        



class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
                 'email',
                 'first_name',
                 'last_name'
                )
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'first_name': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'email': forms.TextInput(attrs={'class': 'myfieldclass'}),
            
        }
        def __init__(self, *args, **kwargs):
                super(NoteForm, self).__init__(*args, **kwargs)
                self.fields['email'].widget.attrs.update({'class': 'input-box'})
                self.fields['first_name'].widget.attrs.update({'class': 'input-box'})
                self.fields['last_name'].widget.attrs.update({'class': 'input-box'})
class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'linkedin', 'instagram', 'image')

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'linkedin': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'instagram': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'image': forms.TextInput(attrs={'class': 'myfieldclass'}),
            
        }
        def __init__(self, *args, **kwargs):
                super(NoteForm, self).__init__(*args, **kwargs)
                self.fields['email'].widget.attrs.update({'class': 'input-box'})
                self.fields['first_name'].widget.attrs.update({'class': 'input-box'})
                self.fields['last_name'].widget.attrs.update({'class': 'input-box'})


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['note_title','note_content', 'image', 'video']
        widgets = {
            'note_title': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }
        def __init__(self, *args, **kwargs):
            super(NoteForm, self).__init__(*args, **kwargs)
            self.fields['video'].widget.attrs.update({'class': 'myfieldclassvideo'})
            self.fields['image'].widget.attrs.update({'class': 'myfieldclassvideo'})
      
