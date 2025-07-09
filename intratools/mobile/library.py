import json
import datetime
import pytz

import aiohttp

from intratools.mobile.models import Student
from intratools.mobile.errors import StatusNotOKError



time_keys_normal = {
    "28": 0,
    "1": 1,
    "4": 2
}

time_keys_weekend = {

}

def seat_name_to_code(name: str) -> int:
    seat_names = {
        "1": 1,
        "2": 3,
        "3": 5,
        "4": 6,
        "5": 7,
        "6": 8,
        "7": 9,
        "8": 10,
        "9": 11,
        "10": 21,
        "11": 22,
        "12": 23,
        "13": 24,
        "14": 25,
        "15": 26,
        "16": 27,
        "17": 28,
        "18": 29,
        "19": 30,
        "20": 31,
        "21": 32,
        "22": 33,
        "23": 34,
        "24": 35,
        "25": 36,
        "26": 37,
        "27": 38,
        "28": 39,
        "29": 40,
        "30": 41,
        "31": 42,
        "32": 43,
        "33": 44,
        "34": 45,
        "35": 46,
        "36": 47,
        "37": 48,
        "38": 49,
        "39": 50,
        "40": 51,
        "41": 52,
        "42": 53,
        "43": 54,
        "44": 55,
        "45": 56,
        "46": 57,
        "47": 58,
        "48": 59,
        "49": 60,
        "50": 61,
        "51": 62,
        "52": 63,
        "53": 64,
        "54": 65,
        "55": 66,
        "56": 67,
        "57": 68,
        "58": 69,
        "59": 70,
        "60": 75,
        "61": 76,
        "62": 77,
        "63": 78,
        "64": 79,
        "65": 180,
        "66": 181,
        "67": 182,
        "68": 183,
        "69": 184,
        "70": 185,
        "71": 186,
        "72": 187,
        "73": 104,
        "74": 105,
        "75": 106,
        "76": 111,
        "77": 112,
        "78": 113,
        "79": 114,
        "80": 115,
        "81": 120,
        "82": 123,
        "83": 122,
        "84": 121,
        "1-1": 84,
        "1-2": 85,
        "1-3": 86,
        "1-4": 87,
        "1-5": 88,
        "1-6": 93,
        "1-7": 94,
        "1-8": 95,
        "1-9": 96,
        "1-10": 97,
        "1-11": 102,
        "1-12": 103,
        "1-13": 188,
        "1-14": 189,
        "1-15": 190,
        "2-13": 124,
        "2-14": 125,
    }
    return seat_names[name]


async def get_library_status(session, time_code):
    """
    지정된 타임의 현재 도서관 상황을 가져옵니다.
    """
    # print(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"))

    payload = {
        "code": "001",         # -> 도서관, 토의실 구분 (001은 도서관, 002는 토의실)
        "t_code": time_code    # 타임 구분
    }

    headers = {
        # "cookie": "JSESSIONID=FBC07BEA4BC36996BF093BA91E3FBCCC",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Content-Type": "multipart/form-data",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }

    """
    원래는 libSeatResvViewList.ajax -> libCheckRule.ajax -> libSeatSex.ajax -> libSeatNoUseReason.ajax -> libResvProc.ajax 순서대로 해야지 신청 가능

    """

    async with session.post('https://go.hana.hs.kr/json/libResvList.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())

            # restTime == 'N' 일 경우 휴관?
            if result['restTime'] == 'N':
                # 휴관
                # return []
                closed = True

            else:
                closed = False

            # 고려할 것들
            # 1. 정체불명의 delegate 키?
            # 2. 36번 자리 reason 키?

            # TODO: 원래 코로나때문에 "안 되는 자리"
            unavail_seat_names = [
                "6", "8", "10", 
                "11", "13", "15", 
                "18", "20", "22", "24", 
                "25", "27", "29", "31", 
                "34", "36", "37", "39", 
                "42", "44", "46", "48", 
                "52", "54", "56", "58", 
                "62", "63", "66", "67", 
                "70", "71", 
                "2-13", "2-14", 
                "1-2", "1-4", "1-6", 
                "1-7", "1-9", "1-11", 
                "1-14"
            ]

            fuck = []

            for s in result['result']:
                if s['isReser']:
                    # 사람이 있는 경우
                    stu_num, stu_name, stu_username = s['isReser'].split('|')
                    stu = Student(stu_num, stu_name, username=stu_username)

                    fuck.append({
                        "seat_name": s['dis_num'],
                        "seat_code": s['s_code'],
                        "reserved": True,
                        "available": False,
                        "resv_code": s['r_code'],   # 예약코드
                        "student": stu
                    })
                else:
                    fuck.append({
                        "seat_name": s['dis_num'],
                        "seat_code": s['s_code'],   
                        "reserved": False,
                        "available": not (s['dis_num'] in unavail_seat_names)
                    })
            return fuck, closed

        else:
            raise StatusNotOKError

async def reserve_library(session, seat_code, time_code):
    """
    도서관을 예약합니다.
    """
    # print(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"))

    payload = {
        "code": "001",              # -> 도서관, 토의실 구분 (001은 도서관, 002는 토의실)
        "t_code": time_code,        # 타임 코드
        "s_code": seat_code         # 자리 코드
    }

    headers = {
        # "cookie": "JSESSIONID=FBC07BEA4BC36996BF093BA91E3FBCCC",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Content-Type": "multipart/form-data",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }

    """
    원래는 libSeatResvViewList.ajax -> libCheckRule.ajax -> libSeatSex.ajax -> libSeatNoUseReason.ajax -> libResvProc.ajax 순서대로 해야지 신청 가능

    """
    timeout = aiohttp.ClientTimeout(total=5)

    async with session.post('https://go.hana.hs.kr/json/libResvProc.ajax', data=payload, headers=headers, timeout=timeout) as resp:
        if resp.status == 200:
            # 20230323 업데이트
            
            try:
                result = json.loads(await resp.text())
            except:
                print("*** reserve_library 오류! - json load failed")
                return False
            if result['result'] == "success":
                # print(result)
                return True
            else: 
                print("ERROR", result)
                return False
        else:
            raise StatusNotOKError



async def get_seat_reserv_status(session, seat_code, time_codes=["28", "1", "4"]):
    """
    지정된 좌석의 금일 예약현황을 불러옵니다.
    """

    payload = {
        "code": "001",
        "s_code": seat_code,
        "t_codes": time_codes
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }

    async with session.post('https://go.hana.hs.kr/json/libSeatResvViewList.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())

            fuck = []

            for r in result['result']:
                stu = Student(r['musr_SchoolNo'], r['musr_Name'], sex=r['muser_Sex'], username=r['musr_ID'], birthcode=r['musr_RegNo'][:6])

                fuck.append({
                    "time_code": r['t_code'],
                    "seat_code": r['s_code'],
                    "resv_code": r['r_code'],
                    "student": stu
                })

            return fuck
        else:
            raise StatusNotOKError


async def get_my_library_reserv_status(session):
    """
    내 도서관 예약 현황을 가져옵니다.
    :return: List[예약코드]
    """

    payload = {
        "reserdate_from": datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"),
        "reserdate_to": datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d")    
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }

    async with session.post('https://go.hana.hs.kr/json/libMyResvList.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())

            fuck = []

            for r in result['result']:
                fuck.append({
                    "time_code": r['t_code'],     # 타임코드
                    "seat_name": r['dis_num'],    # 좌석번호
                    "resv_code": r['r_code']      # 코드
                })
            return fuck
        else:
            raise StatusNotOKError

async def cancel_library(session, time_code, resv_code):
    payload = {
        "r_code": resv_code,
        "t_code": time_code
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }

    async with session.post('https://go.hana.hs.kr/json/libCancelProc.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            try:
                result = json.loads(await resp.text())

                if result['result'] == "success": 
                    return True
                else: 
                    return False
            except json.decoder.JSONDecodeError:
                # 다른 사람 예약인 경우
                return False

        else:
            raise StatusNotOKError

