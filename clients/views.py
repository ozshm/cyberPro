from django.http import response
from django.shortcuts import redirect, render

from django.http import Http404

from .models import Client

# Create your views here.

def client_create_view(request):

    res = None
    last_client = None

    if request.method == 'GET':
        clientFirstName = request.GET.get('fname', None)
        clientLastName = request.GET.get('lname', None)
    else:
        clientFirstName = request.POST.get('fname')
        clientLastName = request.POST.get('lname')
        if not (clientFirstName.replace(' ', '').isalpha()) or not (clientLastName.replace(' ', '').isalpha()): 
            return render (request, 'http404.html')

    if  clientFirstName and clientLastName:
        saveclient = Client(name= clientFirstName,lastName= clientLastName)
        saveclient.save()
    
        if request.COOKIES['isSecure'] == 'true':
            get_last_client_query = "SELECT * FROM clients_client order by id DESC LIMIT 1;"
            res = Client.objects.raw(get_last_client_query)

        else:
            get_client_query = f"SELECT * FROM clients_client WHERE name = '%s'  AND lastName = '%s';" % (clientFirstName, clientLastName)
            res = Client.objects.raw(get_client_query)
            
    else:
        get_last_client_query = "SELECT * FROM clients_client order by id DESC LIMIT 1;"
        res = Client.objects.raw(get_last_client_query)
        #res = Client.objects.all().last


    context = {
        #'last_client': last_client,
        'page_name': 'clients',
        'client_fname': clientFirstName,
        'client_lname': clientLastName,
        'isSecure': request.COOKIES['isSecure'],
        'title': 'Clients',
        'c': res
    }

    return render(request, "clients/client_create.html", context)
