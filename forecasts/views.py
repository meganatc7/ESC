from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests, json, datetime
from pprint import pprint

# 브라우저에서 직접 url로 데이터 받아보기
# http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?serviceKey=3urgccFNfwIp7ePyvIBfqtDLrK7Sxy2YZkHZ4lc33Cf%2F242KukfpnMSZ8wPOQCh716qplOd0Pp3AtewChHHfrg%3D%3D&numOfRows=10&pageNo=1&dataType=JSON&base_date=20210408&base_time=2100&nx=58&ny=74

# 위도 경도 = {}

# time_setting 함수는 현재 시간을 파악하여, 
# 날씨 데이터 중 가장 최신의 데이터를 받아 올 수 있도록
# 현재 시간을 수정하고 반환해준다.
def time_setting():
    now = datetime.datetime.now()
    now_date = datetime.date.today()
    now_time = now.strftime('%H%M')
    now_hour = now_time[:2]
    now_minite = now_time[2:]
    # ex) 13:40 이후에 13:00 데이터가 업로드 된다.
    if 0 <= int(now_minite) < 45:
        # 지금이 딱 오전 00시 근처일 때이면, 
        # 하루전 데이터를 사용자에게 보여줘야한다.
        if now_hour == '00':
            now_date = now_date - datetime.timedelta(1)
            now_hour = '23'
        else:
            now_time = now - datetime.timedelta(hours=1)
            now_hour = now_time.strftime('%H')
    # datetime 객체를 str으로 변환
    now_date = now_date.strftime('%Y%m%d')
    
    return now_date, now_hour+'00'


# Create your views here.
@login_required
def index(request):
    server_serviceKey = '3urgccFNfwIp7ePyvIBfqtDLrK7Sxy2YZkHZ4lc33Cf%2F242KukfpnMSZ8wPOQCh716qplOd0Pp3AtewChHHfrg%3D%3D'

    now_date, now_hour = time_setting()
    # now = datetime.datetime.now()
    # now_date = now.strftime('%Y%m%d')
    # now_hour = now.strftime('%H%M')

    print(now_date)
    print(type(now_hour), now_hour)
    
    # 초 단기 실황 조회
    ultra_srt_ncst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?serviceKey={server_serviceKey}&numOfRows=10&pageNo=1&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx=58&ny=74'


    # 초 단기 예보 조회 url
    ultra_srt_fcst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?serviceKey={server_serviceKey}&numOfRows=60&pageNo=1&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx=58&ny=74'


    # 예보 조회 url
    vilage_fcst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={server_serviceKey}&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx=58&ny=74'
    
    # 현재 기온 데이터 받아오기
    ncst_response = requests.get(ultra_srt_ncst_url)
    ncst_data_dict = ncst_response.json()

    print(ncst_response)
    pprint(ncst_data_dict)

    # 초단기 예보 데이터 받아오기
    srt_fcst_response = requests.get(ultra_srt_fcst_url)
    srt_fcst_dict = srt_fcst_response.json()
    print(srt_fcst_response)
    # print(len(srt_fcst_dict['response']['body']['items']['item']))
    pprint(srt_fcst_dict)

    context = {
        'T1H': ncst_data_dict['response']['body']['items']['item'][3]['obsrValue'],
        'PTY': ncst_data_dict['response']['body']['items']['item'][0]['obsrValue'],
    }
    # pprint(response[body][items][item][5]['fcstValue'])
    # pprint(response[body][items][item]['POP'])

    return render(request, 'forecasts/index.html', context)