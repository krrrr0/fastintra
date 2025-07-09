import json
import datetime
import pytz

import aiohttp

from intratools.mobile.errors import StatusNotOKError

async def get_today_type(session) -> int:
    """
    오늘이 평일인지, 아니면 주말 일과인지 판단합니다.
    return: (평일) 1, (주말공휴일) 2
    """
    # print(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d"))

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


    async with session.get('https://go.hana.hs.kr/libraryResvList.do', headers=headers) as resp:
        if resp.status == 200:
            result = await resp.text()

            if '평일 1타임' in result:
                return 1
            else:
                return 2

        else:
            raise StatusNotOKError