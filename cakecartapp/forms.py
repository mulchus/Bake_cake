from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()


class TableForm(forms.Form):
    num = forms.IntegerField(label='Please Enter Number:')


class CreationForm(UserCreationForm):
    phone_number = PhoneNumberField(region='RU',
                                    max_length=20,
                                    label='Телефонный номер',)
    client_name = forms.CharField(label='Имя клиента',
                                  max_length=200,)
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'client_name',)
        help_texts = {
            ''
        }
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'cake__textinput'})
        # }
