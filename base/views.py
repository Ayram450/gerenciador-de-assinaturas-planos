from django.shortcuts import render

def homepage(request):
    return render(request, "base/homepage.html",)

def recursos(request):
    return render(request, "base/recursos.html",)

def sobre(request):
    return render(request, "base/sobre.html",)

