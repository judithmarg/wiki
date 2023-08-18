from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms

from . import util
import markdown2 
import random

class NewPageCreate(forms.Form):
    titulo = forms.CharField(label='Titulo de la pagina')
    contenido = forms.CharField(widget=forms.Textarea)

class NewPageEdit(forms.Form):
    contenido = forms.CharField(widget=forms.Textarea)

class NewSearchForm(forms.Form):
    busqueda = forms.CharField(label='Search Encyclopedia')

entradas = set(util.list_entries())
last_entry = None

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': NewSearchForm()
    })

def entry(request, title):
    contenidoEntrada = util.get_entry(title)
    global last_entry
    if contenidoEntrada is None:
        return render(request, 'encyclopedia/pageNotFound.html',{    
            'form': NewSearchForm()
        })
    else:
        last_entry = title 
        return render(request, 'encyclopedia/page.html', {
            'contenido' : markdown2.markdown(contenidoEntrada),
            'form': NewSearchForm()
        })
    
def pertenece(cadena, cadenaPerteneciente):
    return (cadena.capitalize()) in (cadenaPerteneciente.capitalize()) or cadena in cadenaPerteneciente
    
def search(request):
    posibilidades = []
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid():
            cadena = form.cleaned_data['busqueda']
            for entrada in entradas:
                if pertenece(cadena, entrada):
                    posibilidades.append(entrada)
                    return entry(request, entrada)
            return render(request, 'encyclopedia/pageResults.html', {
                'posibilidades' : posibilidades,
                'form': NewSearchForm()
            })
        else:
            return render(request, 'encyclopedia/pageResults.html', {
                'posibilidades' : posibilidades,
                'form': NewSearchForm()
            })
    return render(request, 'encyclopedia/layout.html', {
        'form': NewSearchForm()
    })

def new_page(request):
    return render(request, 'encyclopedia/pageCreate.html',{
        'formCreate' : NewPageCreate(),
        'form': NewSearchForm()
    } )
    
def save(request):
    if request.method == 'POST':
        form = NewPageCreate(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            contenido = form.cleaned_data['contenido']
            for entrada in entradas:
                if titulo in entrada:
                    return render(request, 'encyclopedia/pageError.html')
            util.save_entry(titulo, contenido)
            return HttpResponseRedirect(reverse('index'))
        
        else:
            return render(request, 'encyclopedia/pageCreate.html',{
                'formCreate' : NewPageCreate(),
                'form': NewSearchForm()
            } )
    else:
        return render(request, 'encyclopedia/pageCreate.html',{
            'formCreate' : NewPageCreate(),
            'form': NewSearchForm()
        } )
    
def edit(request):
    formEdit = NewPageEdit()
    ultima_entrada = util.get_entry(last_entry)
    formEdit = NewPageEdit(initial={'contenido':ultima_entrada})
    return render(request, 'encyclopedia/pageEdit.html',{
        'formEdit' : formEdit,
        'form': NewSearchForm()
    } )

def save_edit(request):
    if request.method == 'POST':
        form = NewPageEdit(request.POST)
        if form.is_valid():
            contenido = form.cleaned_data['contenido']
            util.save_entry(last_entry,contenido)
            return entry(request, last_entry)
        else:
            return render(request, 'encyclopedia/pageError.html', {
                'form': NewSearchForm()
            })
    else:
        return entry(request, last_entry)

def random_page(request):
    global entradas
    longitud = len(entradas)
    indice = random.randint(0, longitud)
    titulo_page = list(entradas)[indice]
    return entry(request, titulo_page)
