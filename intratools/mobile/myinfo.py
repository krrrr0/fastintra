from intratools.mobile.errors import StatusNotOKError



# async def get_my_name(session):
#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "same-origin",
#         "Sec-GPC": "1",
#         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
#         "X-Requested-With": "XMLHttpRequest",
#         "Origin": "https://go.hana.hs.kr",
#         "Referer": "https://go.hana.hs.kr/index.do"
#     }
# 
#     async with session.get('https://go.hana.hs.kr/setting.do', headers=headers) as resp:
#         if resp.status == 200:
#             result = await resp.text()
# 
#             return result.split('<span class="name">')[1].split('</span>')[0]
# 
#         else:
#             raise StatusNotOKError

async def get_homeroom_teacher_name(session):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/index.do"
    }

    async with session.get('https://go.hana.hs.kr/sGoOutRegisterForm.do', headers=headers) as resp:
        if resp.status == 200:
            result = await resp.text()

            return result.split('(담임 : ')[1].split(' 선생님)</td>')[0]

        else:
            raise StatusNotOKError

async def get_my_info(session):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://go.hana.hs.kr",
        "Referer": "https://go.hana.hs.kr/scrApplicationList.do"
    }

    data = {
        "idx": 0,
        "reg_type": "ins"
    }

    async with session.post('https://go.hana.hs.kr/scrApplicationRegister.do', headers=headers, data=data) as resp:
        if resp.status == 200:
            result = await resp.text()
            tmp = result.split("html += \"\t<td>")[1:5]
            num, name, grade, cls = map(lambda x: x.split('</td>";\r\n\t\t')[0], tmp)
            grade = int(grade.removesuffix("학년"))
            cls = int(cls.removesuffix("반"))

            return num, name, grade, cls

        else:
            raise StatusNotOKError



