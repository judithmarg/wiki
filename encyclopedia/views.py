from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util
import markdown2 

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
