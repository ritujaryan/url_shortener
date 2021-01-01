from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.contrib.gis.utils import GeoIP
#from django.template import  RequestContext
#from django.shortcuts import render_to_response
from django.utils import timezone

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
        #res = requests.get('https://ipinfo.io/')
        #data = res.jason()
        #location = data['loc'],split(',')
        #llat = float(location[1])
        #llong = float(location[0])
        #ob = UserLocation(shorturl = link, city = data['city'], long = llong, lat = llat)
        #ob.save() 
        return redirect(req_longurl)
    except Exception as e:
        print(e)
        return render(request, 'invalid.html')


def get_analytics(request):
    rows = LongToShort.objects.all()
    return render(request, 'analytics.html', {'data': rows})