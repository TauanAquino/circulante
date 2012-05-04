# coding:utf-8

from django.forms import ModelForm, ValidationError

from .models import Publicacao
from isbn import validatedISBN10


class PublicacaoModelForm(ModelForm):
    class Meta:
        model = Publicacao
     
     
    def clean_id_padrao(self):
        data = self.cleaned_data['id_padrao']
        if self.cleaned_data['tipo'] == 'livro':
            isbn = validatedISBN10(data)
            if isbn:
                data = isbn
            else:
                msg = 'For books the id_padrao need be a valid ISBN'
                raise ValidationError(msg)
        return data
