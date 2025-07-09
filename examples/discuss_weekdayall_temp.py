# (평일) 13시 1분~30초 전에 실행하세요

import tkinter
from tkinter import messagebox

import asyncio
import aiohttp
import intratools.mobile.login
import intratools.mobile.discuss
from intratools.mobile.discuss import TIME_WEEKDAY_0TIME, TIME_WEEKDAY_1TIME, TIME_WEEKDAY_2TIME


async def main():
    print("Working...")
    try:
        session = aiohttp.ClientSession()
        login_result = await intratools.mobile.login.login(session, "username", "password")
        if not login_result:
            messagebox.showerror("오류", "로그인 실패!")
            await session.close()
            return

        msg = ""


        result = await intratools.mobile.discuss.reserve_discuss(
            session,
            ["12", "13", "14", "15", "16", "18"], # 주의! 17 사용 안함
            TIME_WEEKDAY_0TIME,
            # 박정연A, 정찬훈, 조인수, 김세훈, 오서준, 양희준(0T만)
            # 박정연A, 오서준, 조인수, 이신재, 심영민, 허재준, 김기현, ???
            ["username", "Burning",  "joinsoo", "mantaray", "osjoon005", "didg4123"],
            ["Y", "N", "N", "N", "N", "N"]
        )

        if result == True:
            msg += "평일 0타임 - 성공!"
        else:
            msg += "평일 0타임 - 실패!"

        # ======================================================

        result = await intratools.mobile.discuss.reserve_discuss(
            session,
            ["12", "13", "14", "15", "16", "18"], # 주의! 17 사용 안함
            TIME_WEEKDAY_1TIME,
            # 박정연A, 정찬훈, 조인수, 김세훈, 오서준, 양희준(0T만)
            # 박정연A, 오서준, 조인수, 이신재, 심영민, 허재준, 김기현, ???
            ["username", "Burning",  "joinsoo", "mantaray", "osjoon005"],
            ["N", "Y", "N", "N", "N",]
        )

        if result == True:
            msg += "\n평일 1타임 - 성공!"
        else:
            msg += "\n평일 1타임 - 실패!"

        # ======================================================

        result = await intratools.mobile.discuss.reserve_discuss(
            session,
            ["12", "13", "14", "15", "16", "18"], # 주의! 17 사용 안함
            TIME_WEEKDAY_2TIME,
            # 박정연A, 정찬훈, 조인수, 김세훈, 오서준, 양희준(0T만)
            # 박정연A, 오서준, 조인수, 이신재, 심영민, 허재준, 김기현, ???
            ["username", "Burning",  "joinsoo", "mantaray", "osjoon005"],
            ["N", "N", "Y", "N", "N",]
        )

        if result == True:
            msg += "\n평일 2타임 - 성공!"
        else:
            msg += "\n평일 2타임 - 실패!"


        messagebox.showinfo("결과", msg)
        await session.close()
    except Exception as exp:
        messagebox.showerror("오류", f"{exp}")
        return
    return

if __name__ == "__main__":
    root = tkinter.Tk()
    root.withdraw()
    asyncio.run(main())