from django.http import JsonResponse
from django.shortcuts import render
import film.service as film_service
# Create your views here.

def start(request):
    print(request.method)
    if request.method == 'POST':
        film_name = request.POST.get('film_name')
        return get_films(request, film_name)
    return render(request, 'film/start.html')

def get_films(request, film_name=None):
    return JsonResponse(film_service.select_films(film_name), safe=False)

def index(request):
    return 'index.html'
