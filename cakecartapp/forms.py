from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from .models import Client

User = get_user_model()


class TableForm(forms.Form):
    num = forms.IntegerField(label='Please Enter Number:')


class CreationForm(UserCreationForm):
    phone_number = PhoneNumberField(region='RU',
                                    max_length=20,
                                    label='Телефонный номер',)
    client_name = forms.CharField(label='Имя',
                                  max_length=200,)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if Client.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Пользователь с этим номером телефона уже существует!")
        return phone_number

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'client_name',)
        help_texts = {
            ''
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'cake__textinput'})
        }
