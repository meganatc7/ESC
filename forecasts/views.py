from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests, json
from pprint import pprint

# Create your views here.
@login_required
def index(request):
    my_serviceKey = '3urgccFNfwIp7ePyvIBfqtDLrK7Sxy2YZkHZ4lc33Cf%2F242KukfpnMSZ8wPOQCh716qplOd0Pp3AtewChHHfrg%3D%3D'
    
    vilage_fcst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={my_serviceKey}&dataType=JSON&base_date=20210408&base_time=0000&nx=58&ny=74'
    response = requests.get(vilage_fcst_url).json()

    pprint(response)

    # 동네 예보 조회 url
    # vilage_fcst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={server_serviceKey}&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx=58&ny=74'
    
    # 초단기 실황 데이터 받아오기
    # 초단기 실황 데이터 아이템 개수: 8
    ncst_response = requests.get(ultra_srt_ncst_url)
    print(ncst_response.text)

    ncst_data_dict = ncst_response.json()  # 딕셔너리 자료형
    c_PTY = ncst_data_dict['response']['body']['items']['item'][0]['obsrValue']
    if c_PTY == '0':
        c_PTY = '비가 오지 않습니다.'
    elif c_PTY == '1':
        c_PTY = '비가 옵니다.'
    elif c_PTY == '3':
        c_PTY = '눈이 옵니다...ㅜ'
    else:
        c_PTY = '비 또는 눈이 약하게 떨어지고 있습니다.'

    c_T1H = ncst_data_dict['response']['body']['items']['item'][3]['obsrValue']

    # 초단기 예보 데이터 받아오기
    srt_fcst_response = requests.get(ultra_srt_fcst_url)
    print(srt_fcst_response.text)
    srt_fcst_dict = srt_fcst_response.json()  # 딕셔너리 자료형
    
    processed_pred_data = processing_data(srt_fcst_dict)
    print(processed_pred_data)
    context = {
        'c_TIME': now_hour[:2] + ':' + now_hour[2:],
        'c_T1H': c_T1H,
        'c_PTY': c_PTY,
        'user_address': user_address,
        'processed_pred_data': processed_pred_data,
    }

    return render(request, 'forecasts/detail.html', context)
