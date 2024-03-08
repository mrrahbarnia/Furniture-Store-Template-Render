from django.shortcuts import render

from .models import Furniture


def test(request):
    furniture = Furniture.objects.all()
    context = {
        'furniture': furniture
    }

    return render(request, 'test.html', context)
