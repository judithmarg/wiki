from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from . import util
import markdown2 

class NewPageCreate(forms.Form):
    titulo = forms.CharField(label='Titulo de la pagina')
    contenido = forms.CharField(widget=forms.Textarea)

class NewSearchForm(forms.Form):
    busqueda = forms.CharField(label='Search Encyclopedia')

entradas = set(util.list_entries())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': NewSearchForm()
    })

def entry(request, title):
    contenidoEntrada = util.get_entry(title)
    if contenidoEntrada is None:
        return render(request, 'encyclopedia/pageNotFound.html')
    else:
        return render(request, 'encyclopedia/page.html', {
            'contenido' : markdown2.markdown(contenidoEntrada)
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
        'formCreate' : NewPageCreate()
    } )
    