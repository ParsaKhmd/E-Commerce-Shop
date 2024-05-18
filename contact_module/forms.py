from django import forms

from .models import ContactUs


# from django.core import validators





class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['title', 'email', 'full_name', 'message']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
                'id': 'message'

            })
        }
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'title': 'عنوان',
            'message': 'متن'
        }
        error_messages = {
            'full_name': {
                'required': 'لطفا نام و نام خانوادگی خود را وارد کنید'
            }
        }


class ProfileForm(forms.Form):
    user_image = forms.ImageField()
