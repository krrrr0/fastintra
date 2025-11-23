'''
15기 부동장입니다
이제 면학실도 예약입니다..
Last edited: 2025-11-23
면학실 hardseat 번호 호출 관련해서는 Example 코드 참고 바랍니다.
'''
import json
import datetime
import pytz

from intratools.mobile.errors import StatusNotOKError
from intratools.mobile.models import *


async def get_today_teacher(session):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/hanaSchedule.do"
    }

    data = {
        "idx": 0,
        "reg_type": "ins"
    }

    async with session.post('https://go.hana.hs.kr/json/hanaScheduleList.ajax', headers=headers, data=data) as resp:
        if resp.status == 200:
            t = json.loads(await resp.text())

            result = []

            for i in t['ScheduleList']:
                result.append(i['listStitle'])

            return result
            
        else:
            raise StatusNotOKError


async def get_my_studyroom_reserv_status(session, time_code=None):
    """
    내 면학실 예약 현황을 가져옵니다.
    :param time_code: str - 특정 타임 코드 (선택사항, 없으면 모든 타임 조회)
    :return: List[dict] - 예약 정보 리스트
    """
    
    # 여러 타임 코드 확인 (평일+주말)
    time_codes_to_check = ["29", "12", "13", "50", "51", "7", "9", "10", "26"] if not time_code else [time_code]
    
    all_reservations = []
    
    for t_code in time_codes_to_check:
        payload = {
            "code": "001",  # 면학실 코드
            "t_code": t_code
        }

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://go.hana.hs.kr",
            "Referer": "https://go.hana.hs.kr/index.do"
        }

        async with session.post('https://go.hana.hs.kr/json/hardResvList.ajax', data=payload, headers=headers) as resp:
            if resp.status == 200:
                result = json.loads(await resp.text())
                
                # r_code가 있는 것만 가져옴
                if 'result' in result and result['result']:
                    for r in result['result']:
                        # r_code가 있는 항목만 실제 예약하기
                        if r.get('r_code'):
                            all_reservations.append({
                                "t_code": t_code,                 # 타임코드
                                "s_code": r.get('s_code'),        # 좌석코드
                                "seat_name": r.get('dis_num'),    # 좌석번호 표시용임)
                                "r_code": r.get('r_code'),        # 예약코드
                                "resv_date": r.get('resv_date')   # 예약일
                            })
    
    return all_reservations


async def get_studyroom_seat_status(session, time_codes):
    """
    면학실 좌석 예약 현황을 가져옵니다.
    :param time_codes: List[str] - 타임코드 리스트 (예: ["7", "9", "10", "26"])
    :return: dict - 좌석별 예약 현황
    """
    payload = {
        "code": "001",  # 면학실 (몇층)
        "s_code": "6",  # 좌석
    }
    
    # 타임코드 추가
    for t_code in time_codes:
        payload[f"t_codes"] = t_code
    
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }
    
    async with session.post('https://go.hana.hs.kr/json/hardSeatResvViewList.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())
            return result
        else:
            raise StatusNotOKError


async def reserve_studyroom(session, seat_code, time_code):
    """
    면학실 좌석을 예약합니다.
    :param seat_code: str - 좌석 코드 (예: "78")
    :param time_code: str - 타임 코드 (예: "26")
    :return: dict - 이게 예약 결과
    """
    payload = {
        "code": "001",
        "s_code": seat_code,
        "t_code": time_code
    }
    
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }
    
    async with session.post('https://go.hana.hs.kr/json/hardResvProc.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            text = await resp.text()
            print(f"예약 API 원본 응답: {text}")  # 디버깅
            try:
                result = json.loads(text)
                return result
            except json.JSONDecodeError:
                # JSON이 아닌 경우 텍스트 그대로 반환
                return {"result": "success" if "success" in text.lower() or text.strip() == "" else "error", "raw": text}
        else:
            raise StatusNotOKError


async def cancel_studyroom(session, resv_code, time_code):
    """
    면학실 예약을 취소합니다.
    :param resv_code: str - 예약 코드 (r_code)
    :param time_code: str - 타임 코드 (t_code)
    :return: dict -> 이게 취소 결과
    """
    payload = {
        "r_code": resv_code,
        "t_code": time_code
    }
    
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }
    
    async with session.post('https://go.hana.hs.kr/json/hardCancelProc.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            text = await resp.text()
            print(f"취소 API 원본 응답: {text}")  # 디버깅
            try:
                result = json.loads(text)
                return result
            except json.JSONDecodeError:
                # JSON이 아닌 경우 텍스트 그대로 반환
                return {"result": "success" if "success" in text.lower() or text.strip() == "" else "error", "raw": text}
        else:
            raise StatusNotOKError


async def check_seat_gender(session, seat_code):
    """
    면학실 좌석의 성별 제한을 확인합니다.
    :param seat_code: str - 좌석 코드 (예: "78")
    :return: dict - 성별 정보
    """
    payload = {
        "s_code": seat_code
    }
    
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }
    
    async with session.post('https://go.hana.hs.kr/json/hardSeatSex.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())
            return result
        else:
            raise StatusNotOKError


