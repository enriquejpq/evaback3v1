from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", max_length=254, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email


class CodigoForm(forms.Form):
    codigo = forms.RegexField(
        regex=r"^\d{6}$",
        label="Código de 6 dígitos",
        error_messages={"invalid": "El código debe tener exactamente 6 números."},
    )
