from django.shortcuts import render
from django.views import View

# Create your views here.
class IndexView(View):
    def get(self, request):
        context = {
            'title': 'Main',
        }
        return render(request, 'index.html', context)
