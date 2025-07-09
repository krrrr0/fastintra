
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


