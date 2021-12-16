from django.http import response
from django.shortcuts import redirect, render

from django.http import Http404

from .models import Client

# Create your views here.

def client_create_view(request):

    if request.method == 'GET':
        clientFirstName = request.GET.get('fname', None)
        clientLastName = request.GET.get('lname', None)
    else:
        clientFirstName = request.POST.get('fname')
        clientLastName = request.POST.get('lname')
        if not (clientFirstName.replace(' ', '').isalpha()):
            return render (request, 'http404.html')

    if  clientFirstName and clientLastName:
        saveclient = Client(name= clientFirstName,lastName= clientLastName)
        saveclient.save()
    
    last_client = Client.objects.all().last

    context = {
        'last_client': last_client,
        'page_name': 'clients',
        'client_fname': clientFirstName,
        'client_lname': clientLastName,
        'isSecure': request.COOKIES['isSecure'] == 'true',
        'title': 'Clients'
    }

    return render(request, "clients/client_create.html", context)
