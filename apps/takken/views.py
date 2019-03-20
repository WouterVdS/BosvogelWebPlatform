from django.shortcuts import render


def index(request):
    return render(request, 'takken/index.html', {'title_suffix': ' - Takken'})
