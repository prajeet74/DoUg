from django.shortcuts import render

def home_view(request):
    return render(request, 'products/home.html')

def dogs_view(request):
    return render(request, 'products/dogs.html')