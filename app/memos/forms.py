from django import forms
from django.contrib.auth import get_user_model

from .models import Memos

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Memos
        fields = ['title', 'text', 'priority']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class':'form-control'
                },
            ),
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '230자 이내'
                }
            ),
            'priority': forms.CheckboxInput(
                attrs={
                    'type': 'checkbox'
                }
            ),
        }
        labels = {
            'title': '제목',
            'text': '내용',
            'priority': '중요',
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '15자 이내로 입력 가능',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
        labels = {
            'username': '사용자명',
            'email': '이메일',
            'password': '비밀번호',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15