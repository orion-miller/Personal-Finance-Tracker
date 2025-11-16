from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello world")

class HelloEthiopia(View):
    def get(self, reqquest):
        return HttpResponse("Hello Ethiopia")