from email import message
from tkinter.messagebox import showinfo
from django import forms

class ContactForm(forms.Form):
    name =forms.CharField(max_length=100)
    message =forms.CharField(widget=forms.Textarea)
    email =forms.EmailField()
    forcefield=forms.CharField(required=False,widget=forms.HiddenInput,label="leave empty",validators=[])
