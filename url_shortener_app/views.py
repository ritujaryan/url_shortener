from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
#from django.template import  RequestContext
#from django.shortcuts import render_to_response
from django.utils import timezone
import requests
import geoip2.database
import socket
import re
import json
from urllib.request import urlopen
from .forms import URLForm
from .models import LongToShort
from .models import UserLocation

import secrets

def home(request):
    return HttpResponse('Hello.')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
                ob = LongToShort.objects.get(shorturl= ip_customname)
                if ob.longurl == ip_longurl:
                    return HttpResponse('Your shorturl is ' + 'https://ra-shorturl.herokuapp.com/redirect/' + ip_customname)
                else:
                    return render(request, 'sorry.html')

        return HttpResponse('Your shorturl is ' + 'https://ra-shorturl.herokuapp.com/redirect/' + final_url)
    else:
        myform = URLForm()
        return render(request, 'form.html', {'form': myform})

def redirect_url(request, link):
    try:
        obj = LongToShort.objects.get(shorturl = link)
        req_longurl = obj.longurl
        obj.visit_count += 1
        obj.save()
        # host_name = socket.gethostname()
        # response = urlopen('https://ipinfo.io/json')
        # data = json.load(response)

        g = GeoIP2('./geoip')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        reader = geoip2.database.Reader('./geoip/GeoLite2-City.mmdb')
        response = reader.city(ip)
        #print(response.city.name)
        #print(response)
        # loc = g.city(ip)
        # print(loc)
        # ab = data['loc'].split(',')
        ob = UserLocation(shorturl = link, city = response.city.name, long = response.location.longitude, lat = response.location.latitude)
        ob.save()
        return redirect(req_longurl)
    except Exception as e:
        print(e)
        return render(request, 'invalid.html')


def get_views(request):
    rows = LongToShort.objects.all()
    return render(request, 'views.html', {'data': rows})


def get_analytics(request):
    rows = UserLocation.objects.all()
    return render(request, 'analytics.html', {'data': rows})