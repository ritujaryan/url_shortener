from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import URLForm
from .models import LongToShort

import secrets

def home(request):
    return HttpResponse('Hello.')

def shorten(request):
    if request.method == 'POST':
        userform = URLForm(request.POST)
        ip_longurl = userform.data['longurl']
        ip_customname = userform.data['custom_name']

        if ip_customname == '':
            gen_shorturl = secrets.token_hex(3)
            final_url = gen_shorturl
            obj = LongToShort(longurl = ip_longurl, shorturl = gen_shorturl)
            obj.save()
        else:
            entries = LongToShort.objects.filter(shorturl = ip_customname)
            if len(entries) == 0:
                final_url = ip_customname
                obj = LongToShort(longurl = ip_longurl, shorturl = ip_customname)
                obj.save()
            else:
                return HttpResponse('Sorry. The custom name is already taken.')

        return HttpResponse('Your shorturl is ' + 'http://localhost:8000/redirect/' + final_url)
    else:
        myform = URLForm()
        return render(request, 'form.html', {'form': myform})

def redirect_url(request, link):
    try:
        obj = LongToShort.objects.get(shorturl = link)
        req_longurl = obj.longurl
        obj.visit_count += 1
        obj.save()
        return redirect(req_longurl)
    except Exception as e:
        print(e)
        return HttpResponse('Invalid short url.')

def get_analytics(request):
    rows = LongToShort.objects.all()
    return render(request, 'analytics.html', {'data': rows})