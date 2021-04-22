from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests, json, datetime
from pprint import pprint

# 브라우저에서 직접 url로 데이터 받아보기
# http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?serviceKey=3urgccFNfwIp7ePyvIBfqtDLrK7Sxy2YZkHZ4lc33Cf%2F242KukfpnMSZ8wPOQCh716qplOd0Pp3AtewChHHfrg%3D%3D&numOfRows=10&pageNo=1&dataType=JSON&base_date=20210408&base_time=2100&nx=58&ny=74

add2xy = {
    '광주': [58, 74],
    '서울': [60, 127],
    '부산': [98, 76],
    '대구': [89, 90],
    '인천': [55, 124],
    '대전': [67, 100],
    '울산': [102, 84],
    '세종': [66, 103],
    '경기': [60, 120],
    '강원': [73, 134],
    '충북': [69, 107],
    '충남': [68, 100],
    '전북': [63, 89],
    '전남': [51, 67],
    '경북': [89, 91],
    '경남': [91, 77],
    '제주': [52, 38],
}


# time_setting 함수는 현재 시간을 파악하여, 
# 날씨 데이터 중 가장 최신의 데이터를 받아 올 수 있도록
# 현재 시간을 수정하고 반환해준다.
def time_setting():
    now = datetime.datetime.now()
    now_date = datetime.date.today()
    now_time = now.strftime('%H%M')
    now_hour = now_time[:2]
    now_minite = now_time[2:]
    # 현재 시간이 9시 20분이면 8시 00분 데이터를 받아와야한다.
    if 0 <= int(now_minite) < 30:
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


def processing_data(data_dict):
    
    times = []  # 기상 예측 시간
    temps = []  # 기온
    skys = []  # 하늘 상태
    ptys = []  # 강수 형태 precipitation type

    for item_dict in data_dict['response']['body']['items']['item']:
        if len(temps) < 4 and item_dict['category'] == 'T1H':
            elem = item_dict['fcstValue']
            temps.append(elem)

            # time
            pred_time_str = item_dict['fcstTime']
            times.append(pred_time_str[:2] + ':' + pred_time_str[2:] )
        if len(skys) < 4 and item_dict['category'] == 'SKY':
            # 하늘 상태: 날씨 정보가 번호로 저장되어있는데, 이를 의미를 가진 문자열로 변환
            elem = item_dict['fcstValue']
            if elem == '1':
                elem = '말금'
            elif elem == '3':
                elem = '구름 많음'
            else:
                elem = '흐림'
            skys.append(elem)

        if len(ptys) < 4 and item_dict['category'] == 'PTY':
            # 강수 형태: 날씨 정보가 번호로 저장되어있는데, 이를 의미를 가진 문자열로 변환
            elem = item_dict['fcstValue']
            if elem == '0':
                elem = '비가 오지 않습니다.'
            elif elem == '1':
                elem = '비가 옵니다.'
            elif elem == '3':
                elem = '눈이 옵니다...ㅜ'
            else:
                elem = '비 또는 눈이 약하게 떨어지고 있습니다.'
            ptys.append(elem)

    processed_data = []
    for j in range(len(temps)):
        tmp = {
            'time': times[j],
            'temp': temps[j],
            'sky': skys[j],
            'pty': ptys[j],
        }
        processed_data.append(tmp)

    return processed_data

# 현재 기온과 예측된 기온의 차이를 활용하는 함수
# def f_temps(c_t, arr):
#     len_arr = len(arr)
#     abs_dif = [0] * len_arr
#     dif = [0] * len_arr
#     for i in range(len_arr):
#         dif[i] =  arr[i] - c_t
#         abs_dif[i] = abs(dif)
    
#     max_abs_dif_idx = abs_dif.index(max(abs_dif))
#     pixels = [0] * len_arr
#     for i in range(abs)
#         if i != max_abs_dif_idx:
            
#         else:

# Create your views here.
@login_required
def detail(request):
    server_serviceKey = '3urgccFNfwIp7ePyvIBfqtDLrK7Sxy2YZkHZ4lc33Cf%2F242KukfpnMSZ8wPOQCh716qplOd0Pp3AtewChHHfrg%3D%3D'
    
    # user 주소에 해당하는 지역의 날씨를 보여준다.
    user_address = request.user.address[:2]
    # default 값은 서울로 지정했다.
    user_nx, user_ny = add2xy.get(user_address, add2xy['서울'])

    # 현재 시간으로는 날씨 정보 조회가 불가능 하므로, 커스터 마이징 해서 요청을 보냄
    now_date, now_hour = time_setting()

    print(f'now_date: {now_date}')
    print(f'now_hour: {now_hour}')
    
    # 초 단기 실황 조회
    ultra_srt_ncst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?serviceKey={server_serviceKey}&numOfRows=10&pageNo=1&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx={user_nx}&ny={user_ny}'


    # 초 단기 예보 조회 url
    ultra_srt_fcst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?serviceKey={server_serviceKey}&numOfRows=100&pageNo=1&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx={user_nx}&ny={user_ny}'


    # 동네 예보 조회 url
    # vilage_fcst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={server_serviceKey}&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx=58&ny=74'
    
    # 초단기 실황 데이터 받아오기
    # 초단기 실황 데이터 아이템 개수: 8
    for _ in range(3):
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