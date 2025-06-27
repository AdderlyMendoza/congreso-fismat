from django.shortcuts import render

def landing_page(request):
    return render(request, 'web/pagWeb.html')


def bases_cientificas(request):
    return render(request, 'web/bases.html')
