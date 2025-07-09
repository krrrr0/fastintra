import aiohttp
import asyncio

from intratools import login, library


async def run():
    session = aiohttp.ClientSession()
    login_result = await login.login(session, 'username', 'password')

    # 28 1 4
    # print(login_result)

    weekend_times = [None, 7, 9, 10, 26]
    weekday_times = [28, 1, 4]

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

    # for i in weekday_times:
    #     for j, k in seat_names.items():
    #         if j not in unavail_seat_names:
    #             r = await library.reserve_library(session, k, i)
    #             print(j, r)

    resv_codes = []

    res = await library.get_my_library_reserv_status(session)
    for j in res:
        # print(j)
        # if j['available'] == True:
        resv_codes.append(j['resv_code'])
    print(resv_codes)



    for i in resv_codes:
        for j in weekday_times:
            result = await library.cancel_library(session, j, i)
        print(result)
    await session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    

"""
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    import login
    session = loop.run_until_complete(login.login("username", "password"))
    print(session)
    result = loop.run_until_complete(get_cls_resv_list(session, ""))
    print(result)

    loop.run_until_complete(session.close())



    if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    import login
    token = loop.run_until_complete(login.login("username", "password"))
    print(token)
    result = loop.run_until_complete(reserve_library(token, 28, 28))    # 9번 좌석 0타임
    print(result)

"""

"""
28  평일 0타임
1   평일 1타임
4   평일 2타임

7   주말공휴일 1타임
9   주말공휴일 2타임
10  주말공휴일 3타임
26  주말공휴일 4타임
"""

"""
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    import login
    token = loop.run_until_complete(login.login("username", "password"))
    print(token)
    result = loop.run_until_complete(get_student_list(token, 1, 1))
    print(result)
"""