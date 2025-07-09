import aiohttp
import asyncio
import json

from intratools.mobile.errors import StatusNotOKError
from intratools.mobile.models import Student

async def get_student_list(session, school_grade="", school_class=""):
    # print(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"))
    payload = {
        "musr_schoolGrade": school_grade,
        "musr_schoolClass": school_class
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

    async with session.post('https://go.hana.hs.kr/json/scrStudentList.ajax', data=payload, headers=headers) as resp:
        if resp.status == 200:
            result = json.loads(await resp.text())

            fuck = []

            for stu in result['studentList']:
                fuck.append(
                    Student(
                        stu['musr_schoolNo'],
                        stu['musr_name'],
                        stu['musr_schoolClass'],
                        stu['musr_schoolGrade']
                    )
                )
            
            return fuck
        else:
            raise StatusNotOKError


