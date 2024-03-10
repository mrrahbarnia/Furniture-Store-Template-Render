from django.shortcuts import render


def test(request):
    # furniture = Furniture.objects.all()
    # context = {
    #     'furniture': furniture
    # }

    return render(request, 'test.html')
