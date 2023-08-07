from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from . import util
import markdown2 

class NewSearchForm(forms.Form):
    busqueda = forms.CharField(label='Search Encyclopedia')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    contenidoEntrada = util.get_entry(title)
    if contenidoEntrada is None:
        return render(request, 'encyclopedia/pageNotFound.html')
    else:
        return render(request, 'encyclopedia/page.html', {
            'contenido' : markdown2.markdown(contenidoEntrada)
        })
    
def search(request):
    posibilidades = []
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid():
            cadena = form.cleaned_data['busqueda']
            entradas = util.list_entries()
            for entrada in entradas:
                if cadena in entrada:
                    posibilidades.append(entrada)
            return render(request, 'encyclopedia/pageResults.html', {
                'posibilidades' : posibilidades 
            })
        else:
            return render(request, 'encyclopedia/pageResults.html', {
                'posibilidades': posibilidades
            })
    return render(request, 'encyclopedia/pageResults.html', {
        'posibilidades': posibilidades
    })


