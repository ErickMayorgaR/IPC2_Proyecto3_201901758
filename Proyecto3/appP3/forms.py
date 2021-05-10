from django import forms

class infoForm(forms.Form):

    file = forms.FileField()

class recibir_form(forms.Form):
    Fecha = forms.CharField(label = "Fecha")

class codigo_form(forms.Form):
    Codigo = forms.CharField(label = "Codigo")

