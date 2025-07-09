# 토의실 대응 업데이트 2022.10.07

import json
import datetime
import pytz

from intratools.mobile.errors import StatusNotOKError


"""
타임 키가 다르다?
t_code
평일 2타임 - 13

s_code
12부터 시작한다
17은 사용하지 않는다! (중요)
"""

TIME_WEEKDAY_0TIME = "29"
TIME_WEEKDAY_1TIME = "12"
TIME_WEEKDAY_2TIME = "13"

TIME_WEEKEND_1TIME = "14"
TIME_WEEKEND_2TIME = "15"
TIME_WEEKEND_3TIME = "16"
TIME_WEEKEND_4TIME = "27"





async def reserve_discuss(session, seat_code, time_code, user_ids, delegates):
    """
    도서관을 예약합니다.
    """
    # print(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"))

    payload = {
        "code": "002",              # -> 도서관, 토의실 구분 (001은 도서관, 002는 토의실)
        "t_code": time_code,        # 타임 코드 (도서관 / 토의실이 다름)
        "s_codes": seat_code,         # 자리 코드 (12부터 시작) - 배열 가능
        "user_ids": user_ids,
        "delegates": delegates
    }

    headers = {
        # "cookie": "JSESSIONID=FBC07BEA4BC36996BF093BA91E3FBCCC",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Content-Type": "multipart/form-data",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "TE": "trailers",
        "Host": "go.hana.hs.kr",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/libraryResvList.do"
    }


    async with session.post('https://go.hana.hs.kr/json/discussResvProc.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())
            if result['result'] == "success":
                # print(result)
                return True
            else: 
                print("ERROR", result)
                return False
        else:
            raise StatusNotOKError


