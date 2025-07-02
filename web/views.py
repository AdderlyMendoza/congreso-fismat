from django.shortcuts import render

def landing_page(request):
    return render(request, 'web/pagWeb.html')


def bases_cientificas(request):
    return render(request, 'web/bases.html')

def bases_bases(request):
    return render(request, 'web/bases-bases.html')

def bases_informacion(request):
    return render(request, 'web/bases-informacion.html')
