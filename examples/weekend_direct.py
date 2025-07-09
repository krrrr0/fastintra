import tkinter
from tkinter import messagebox

import asyncio
import aiohttp
import intratools.mobile.login
import intratools.mobile.classroom


weekend_times = [7, 9, 10, 26]

async def main():
    print("Working...")
    session = aiohttp.ClientSession()
    login_result = await intratools.mobile.login.login(session, "username", "password")
    if not login_result:
        messagebox.showerror("오류", "로그인 실패!")
        await session.close()
        return

    msg = ""

    for i, time in enumerate(weekend_times):
        result = await intratools.mobile.classroom.reserve_class(session, time, "A204", "dorm", "21073", "승인")
        if result['resultType'] == 'ok':
            msg += f"주말공휴일 {i + 1}타임 - 성공! (승인)\n"
        else: 
            msg += f"주말공휴일 {i + 1}타임 - 실패! ({result['resultMsg']})\n"
    
    messagebox.showinfo("결과", msg.removesuffix("\n"))
    await session.close()
    return

if __name__ == "__main__":
    root = tkinter.Tk()
    root.withdraw()
    asyncio.run(main())