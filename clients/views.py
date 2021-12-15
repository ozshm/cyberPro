from django.shortcuts import render


from .models import Client

# Create your views here.

def client_create_view(request):


    if request.method == 'GET':
        clientFirstName = request.GET.get('fname', None)
        clientLastName = request.GET.get('lname', None)
    else:
        clientFirstName = request.POST.get('fname', None)
        clientLastName = request.POST.get('lname', None)


    # clientFirstName = request.GET.get('fname', None)
    # clientLastName = request.GET.get('lname', None)
    # # isSecure = request.GET.get('secure', None)

    context = {
        'page_name': 'clients',
        'client_fname': clientFirstName,
        'client_lname': clientLastName,
        'isSecure': request.COOKIES['isSecure'] == 'true'
    }

    # if clientFirstName and clientLastName and isSecure:
    #     saveclient = Client(name= clientFirstName,lastName= clientLastName)
    #     saveclient.save()

    
    return render(request, "clients/client_create.html", context)
