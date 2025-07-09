
import json
import datetime
import pytz

from intratools.mobile.errors import StatusNotOKError
from intratools.mobile.models import *


teachers = [{
    "장경훈": "ibanez8",
    "장재은": "jangdang",
    "조상규": "josg99",
    "박준혁": "junhyuk7101",
    "박서은": "mathse6",
    "최미영": "miyoungc",
    "이재진": "ssokr1",
    "김명진": "wahrheit93"
},{
    "최수경": "blancura99",
    "이효근": "catzeye",
    "권상운": "cloud2446",
    "조우진": "lunarian1104",
    "이영수": "masuri",
    "박종철": "pjc2317",
    "김세미": "samie",
    "김성해": "shaekim"
},{
    "임준호": "bulgom",
    "박찬규": "chandler",
    "이항로": "ggoomgil",
    "우영주": "jjuooo",
    "이서유": "koreansy",
    "박성훈": "psh1136",
    "정형식": "ssdream",
    "김윤구": "veblen"
}]

def get_teacher_username(teacher_name, grade):
    return teachers[grade-1][teacher_name]


async def reserve_class(session, timecode, classroom, teacher, student_number, flag="대기"):
    payload = {
        "reg_type": "ins",
        "idx": "0",
        "appDate": datetime.datetime.strftime(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')), "%Y-%m-%d"),   # 데이트 조작은 안되는듯
        "appTime": str(timecode),
        "appTimeStr": "",
        "appClassRoom": classroom,
        "appTitle": "스터디",
        "appAim": "기타",
        "appNoise": "조용함",   # lol: "요란함" ㅋㅋㅋ
        "appTeacher": teacher,
        "appFlag": flag,  # 승인 works!
        "regStudentArr": student_number,
        "appClassRoomReg": "특별_교과" # 특별_기타
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
        "Referer": "https://go.hana.hs.kr/scrApplicationRegister.do"
    }

    async with session.post('https://go.hana.hs.kr/json/scrApplicationSave.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            # print(resp.headers)
            return json.loads(await resp.text()) # , resp.cookies['JSESSIONID'].value

        else:
            raise StatusNotOKError

async def edit_class(session, idx, timecode, classroom, teacher, student_number, flag="대기"):
    payload = {
        "reg_type": "upd",
        "idx": str(idx),
        "appDate": datetime.datetime.strftime(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')), "%Y-%m-%d"),   # 데이트 조작은 안되는듯
        "appTime": str(timecode),
        "appTimeStr": "",
        "appClassRoom": classroom,
        "appTitle": "스터디",
        "appAim": "기타",
        "appNoise": "조용함",   # lol: "요란함" ㅋㅋㅋ
        "appTeacher": teacher,
        "appFlag": flag,  # 승인 works!
        "regStudentArr": student_number,
        "appClassRoomReg": "특별_교과" # 특별_기타
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
        "Referer": "https://go.hana.hs.kr/scrApplicationRegister.do"
    }

    async with session.post('https://go.hana.hs.kr/json/scrApplicationSave.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            # print(resp.headers)
            return json.loads(await resp.text()) # , resp.cookies['JSESSIONID'].value

        else:
            raise StatusNotOKError



async def get_cls_resv_list(session, search, page=1):
    # print(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"))
    payload = {
        "appdate_from": datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"),
        "pageIndex": page,  # 원래 str이나 int로 해도 전혀 상관이 없네 ㅋㅋ
        "keyword": search
    }

    # 한번에 15개씩 받아옴 (pageUnit, pageSize), 1부터 page_last번째까지 받아오면 됨. (scrAppliCnt)

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

    async with session.post('https://go.hana.hs.kr/json/scrApplicationList.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())

            fuck = []

            if result['scrAppliCnt'] > 0:
                for i in result['scrAppliList']:

                    resrv = ClassReservation(
                        i.get('appAim'), # 개설목적
                        datetime.datetime.strptime(i.get('regDate', "2000-01-01 00:00:00.00").split('.')[0], "%Y-%m-%d %H:%M:%S"), # 개설일시
                        i.get('appFlag'),      # 상태
                        i.get('appTitle'),     # 제목
                        i.get('appClassRoom'), # 호실
                        i.get('appNoise'),     # 소음도
                        i.get('appTime'),      # 타임
                        Student(
                            i.get('appStudent'), # 학번
                            i.get('musr_name'),  # 이름
                            i.get('musr_schoolClass'),  # 반,
                            i.get('musr_schoolGrade')   # 학년
                        ),
                        i.get("idx")            # Index
                    )

                    fuck.append(resrv)

                if result['page_last'] > 1 and page == 1:
                    for j in range(2, result['page_last'] + 1):
                        fuck = fuck + await get_cls_resv_list(session, search, j)
                return fuck
            else: 
                return [] 

        else:
            raise StatusNotOKError


