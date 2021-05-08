from django import forms

class infoForm(forms.Form):

    file = forms.FileField()