from django.http import HttpResponse
from django.shortcuts import render
from .Scarpe import scrape_experience

# Create your views here.
def hello(request):
    context = {}
    context['hello'] = "Hello World"
    return render(request, 'yty.html', context)


# 表单
def search_form(request):
    return render(request, 'search_form.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    try:
        if 'q' in request.GET and request.GET['q']:
            linkedin_url = request.GET['q']
            context = scrape_experience(linkedin_url)
        return render(request, 'yty.html', context)
    except:
        return render(request, "error")



