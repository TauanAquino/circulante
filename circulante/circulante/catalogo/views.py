# coding:utf-8

from .models import Publicacao
from django.shortcuts import render
from isbn import isValidISBN10, validatedISBN10
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import PublicacaoModelForm

def search(request):
    errors = []
    pubs = None
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append(u'Enter a search term.')
        elif len(q) > 30:
            errors.append(u'Please enter at most 30 characters.')
        else:
            isbn = validatedISBN10(q)
            if isbn:
                pubs = Publicacao.objects.filter(id_padrao=isbn)
            else:
                pubs = Publicacao.objects.filter(titulo__icontains=q)
    vars_template = {'errors': errors, 'querry': q}
    if pubs is not None:
        vars_template['publications'] = pubs
        vars_template['search'] = True
    return render(request,'catalogo/search.html',vars_template)
    
def catalog(request):
    errors = []
    if request.method != 'POST':
        form = PublicacaoModelForm()
    else:
        form = PublicacaoModelForm(request.POST)
        if form.is_valid():
            isbn = validatedISBN10(form.cleaned_data['id_padrao'])
            if isbn:
                form.save()
                titulo = form.cleaned_data['titulo']
                return HttpResponseRedirect(reverse('search')+'?q='+titulo)
            else:
                errors.append(u'ISBN invalid.')

    return render(request,'catalogo/catalog.html',{'form': form,'errors':errors})
