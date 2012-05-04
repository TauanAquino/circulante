# coding:utf-8

from .models import Publicacao, Credito
from django.shortcuts import render, get_object_or_404
from isbn import isValidISBN10, validatedISBN10
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from .forms import PublicacaoModelForm
from django.utils.http import urlquote

def search(request):
    errors = []
    pubs = None
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append(u'Enter with a search term.')
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
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    errors = []
    if request.method == 'GET':
        form = PublicacaoModelForm()
        formset = CreditoInlineFormSet()
    elif request.method == 'POST':
        form = PublicacaoModelForm(request.POST)
        formset = CreditoInlineFormSet(request.POST)
        if form.is_valid():
            #isbn = validatedISBN10(form.cleaned_data['id_padrao'])
            isbn = form.cleaned_data['id_padrao']
            if isbn:
                pub = form.save()
                formset = CreditoInlineFormSet(request.POST,instance = pub)
                formset.save()
                title = form.cleaned_data['titulo']
                return HttpResponseRedirect(reverse('search')+'?q='+urlquote(title))
            else:
                errors.append(u'Please, insert a ISBN.')

    return render(request,'catalogo/catalog.html',{'form': form,'errors':errors,'formset':formset})
    
    
def edit(request, primary_key):
    CreditoInlineFormSet = inlineformset_factory(Publicacao, Credito)
    pub = get_object_or_404(Publicacao, pk=primary_key)
    
    if request.method == 'GET':
        form = PublicacaoModelForm(instance=pub)
        formset = CreditoInlineFormSet(instance=pub)
    elif request.method == 'POST':
        form = PublicacaoModelForm(request.POST, instance=pub)
        formset = CreditoInlineFormSet(request.POST,instance = pub)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset = CreditoInlineFormSet(request.POST,instance = pub)
            formset.save()
            title = form.cleaned_data['titulo']
            return HttpResponseRedirect(reverse('search')+'?q='+urlquote(title))
            
    return render(request,'catalogo/catalog.html',{'form': form,'formset':formset})
