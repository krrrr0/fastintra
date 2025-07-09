import tkinter
from tkinter import messagebox

import asyncio
import aiohttp
import intratools.mobile.login
import intratools.mobile.classroom

weekday_times = [1, 4]  # 28

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

        result = await intratools.mobile.classroom.reserve_class(session, 1, "A204", "pjc2317", "21073", "승인")
        if result['resultType'] == 'ok':
            msg += "평일 1타임 - 성공! (승인)"
        else:
            msg += f"평일 1타임 - 실패! ({result['resultMsg']})"

        result = await intratools.mobile.classroom.reserve_class(session, 4, "A204", "dorm", "21073", "승인")
        if result['resultType'] == 'ok':
            msg += "\n평일 1타임 - 성공! (승인)"
        else:
            msg += f"\n평일 1타임 - 실패! ({result['resultMsg']})"

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