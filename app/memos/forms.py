from django import forms

from .models import Memos


class PostForm(forms.ModelForm):
    class Meta:
        models = Memos
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
    pass