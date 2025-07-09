# (주말) 12시 1분~30초 전에 실행하세요

import tkinter
from tkinter import messagebox

import asyncio
import aiohttp
import intratools.mobile.login
import intratools.mobile.discuss
from intratools.mobile.discuss import TIME_WEEKEND_1TIME, TIME_WEEKEND_2TIME, TIME_WEEKEND_3TIME


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
            ["12", "14", "15", "16", "18", "19", "20"], # 주의! 17 사용 안함
            TIME_WEEKEND_1TIME,
            # 박정연 조인수 김세훈 양희준 최보석 김기현 심영민
            ["username", "joinsoo", "mantaray", "didg4123", "05bosuk", "thskrl32", "shimym9"],
            ["Y", "N", "N", "N", "N", "N", "N"]
        )

        if result == True:
            msg += "주말 1타임 - 성공!"
        else:
            msg += "주말 1타임 - 실패!"

        # ======================================================

        result = await intratools.mobile.discuss.reserve_discuss(
            session,
            ["12", "14", "15", "16", "18", "19", "20"], # 주의! 17 사용 안함
            TIME_WEEKEND_2TIME,
            # 박정연 조인수 김세훈 양희준 최보석 김기현 심영민
            ["joinsoo", "didg4123", "05bosuk",  "username", "shimym9", "mantaray", "thskrl32", ],
            ["Y", "N", "N", "N", "N", "N", "N"]
        )

        if result == True:
            msg += "\n주말 2타임 - 성공!"
        else:
            msg += "\n주말 2타임 - 실패!"

        # ======================================================

        result = await intratools.mobile.discuss.reserve_discuss(
            session,
            ["12", "14", "15", "16", "18", "19",], # 주의! 17 사용 안함
            TIME_WEEKEND_3TIME,
            # 박정연 조인수 김세훈 양희준 최보석 심영민
            ["mantaray", "shimym9", "joinsoo", "didg4123", "05bosuk", "username",],
            ["Y", "N", "N", "N", "N", "N"]
        )

        if result == True:
            msg += "\n주말 3타임 - 성공!"
        else:
            msg += "\n주말 3타임 - 실패!"


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