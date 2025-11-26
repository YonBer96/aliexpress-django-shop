from django.http import HttpResponse

def home(request):
    return HttpResponse("AliYon API funcionando correctamente")
