import json
import aiohttp

from intratools.mobile.errors import StatusNotOKError

async def get_token(session, username, password, retried=False):
    payload = {
        "mUsr_ID": username,
        "mUsr_PW": password,
        "loginArr": "test1,test2,test6,teste,teste10,teste11,teste12,teste13,teste2,teste3,teste4,teste5,teste7,teste8,testest,testI,testm,testo,testp,tests,tests1,tests2,tests22,tests3",
        "push_Token": ""
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

    # 20230321 Intratools: implement timeout
    timeout = aiohttp.ClientTimeout(total=20)

    async with session.post('https://go.hana.hs.kr/json/loginProc.ajax', data=payload, headers=headers, timeout=timeout) as resp:
        if resp.status == 200:
            # print(resp.headers)
            try:
                return json.loads(await resp.text()) # , resp.cookies['JSESSIONID'].value
            except:
                if retried == False:
                    return await get_token(session, username, password, retried=True)
                else:
                    raise ValueError()

        else:
            raise StatusNotOKError

async def login(session, username, password):
    login_result = await get_token(session, username, password)
    # print(login_result)

    if login_result['result'] == "fail":
        # 아이디, 비밀번호 불일치
        # print("fail")
        return False

    elif login_result['result'] == "loginCheck":
        # 재시도
        # print("logincheck")
        login_result = await get_token(session, username, password)

        if login_result['result'] == "success":
            # print(key)
            return True
        else:
            # print("로그인 2/2 실패")
            return False
        
    elif login_result['result'] == "success":
        # 로그인 성공, 헤더 Set-Cookie 받아가기
        # print("success")
        # print(key)
        return True


