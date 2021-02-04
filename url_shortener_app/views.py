from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
import datetime
import requests
import geoip2.database
import socket
import re
import json
from urllib.request import urlopen
from .forms import URLForm
from .models import LongToShort
from .models import UserLocation
from django.http import FileResponse


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
                    shortene = 'https://ra-shorturl.herokuapp.com/redirect/' + ip_customname
                    context = {
                    'shortened' : shortene
                    }
                    return render(request, 'thanks1.html', context)
                else:
                    return render(request, 'sorry.html')
        shortene = 'https://ra-shorturl.herokuapp.com/redirect/' + final_url

        context = {
            'shortened' : shortene
        }
        return render(request, 'thanks.html', context)
    else:
        myform = URLForm()
        return render(request, 'form.html', {'form': myform})

def redirect_url(request, link):
    try:
        obj = LongToShort.objects.get(shorturl = link)
        req_longurl = obj.longurl
        obj.visit_count += 1
        obj.save()
        g = GeoIP2('./geoip')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        reader = geoip2.database.Reader('./geoip/GeoLite2-City.mmdb')
        response = reader.city(ip)
        tim = datetime.datetime.now()
        dat = datetime.date.today()
       
        ob = UserLocation(shorturl = link, ip = ip,  city = response.city.name, long = response.location.longitude, lat = response.location.latitude, date = dat, time = tim)
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

def thanks(request):
    return render(request, 'thanks.html')

def image(request) :
    return HttpResponse('image.jpg')
def sendLogo(request):
	res = FileResponse(open('ezgi.gif', 'rb'))
	return res