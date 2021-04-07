from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests, json
from pprint import pprint

# Create your views here.
@login_required
def index(request):
    server_serviceKey = '3urgccFNfwIp7ePyvIBfqtDLrK7Sxy2YZkHZ4lc33Cf%2F242KukfpnMSZ8wPOQCh716qplOd0Pp3AtewChHHfrg%3D%3D'
    
    vilage_fcst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={server_serviceKey}&dataType=JSON&base_date=20210408&base_time=0000&nx=58&ny=74'
    response = requests.get(vilage_fcst_url).json()

    pprint(response)

    return render(request, 'forecasts/index.html')