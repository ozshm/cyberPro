from django.shortcuts import render


from .models import Client

# Create your views here.

def client_create_view(request):

    clientFirstName = request.GET.get('fname', None)
    clientLastName = request.GET.get('lname', None)
    isSecure = request.GET.get('secure', None)

    context = {
        'page_name': 'clients',
        'client_fname': clientFirstName,
        'client_lname': clientLastName,
        'secure': isSecure
    }

    return render(request, "clients/client_create.html", context)

