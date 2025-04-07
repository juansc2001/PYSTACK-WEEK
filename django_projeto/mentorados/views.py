from django.shortcuts import render, HttpResponse
# Create your views here.

def mentorados(request):
    return render(request, 'mentorados.html')