'''
면학실 종합 관리 GUI
15기 부동장입니다
15기부터 면학실이 예약제로 변경되었습니다.
Last edited: 2025-11-23
'''

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import asyncio
import aiohttp
import intratools.mobile.login
import intratools.mobile.studyroom
import intratools.mobile.myinfo


# 타임코드 매핑
TIME_CODE_MAP = {
    "29": "평일 1타임 ",
    "12": "평일 2타임 ",
    "13": "평일 3타임",
    "7": "주말 1타임",
    "9": "주말 2타임",
    "10": "주말 3타임",
    "26": "주말 4타임",
    "50": "주말/공휴일 3타임",
    "51": "주말/공휴일 4타임"
}


class StudyroomViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("면학실 좌석 현황")
        self.root.geometry("1200x800")
        
        self.session = None
        self.seat_data = {}
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.my_name = None  # 내 이름 저장
        
        self.create_widgets()
    
    def create_widgets(self):
        # 상단 프레임 
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # 로그인 정보
        ttk.Label(top_frame, text="아이디:").grid(row=0, column=0, padx=5)
        self.username_entry = ttk.Entry(top_frame, width=15)
        self.username_entry.grid(row=0, column=1, padx=5)
        self.username_entry.insert(0, "yourid")
        
        ttk.Label(top_frame, text="비밀번호:").grid(row=0, column=2, padx=5)
        self.password_entry = ttk.Entry(top_frame, width=15, show="*")
        self.password_entry.grid(row=0, column=3, padx=5)
        self.password_entry.insert(0, "t=yourpw")
        
        # 타임 선택
        ttk.Label(top_frame, text="타임 선택:").grid(row=0, column=4, padx=5)
        self.time_var = tk.StringVar(value="26")
        time_combo = ttk.Combobox(top_frame, textvariable=self.time_var, width=25, state="readonly")
        time_combo['values'] = [f"{code} - {label}" for code, label in TIME_CODE_MAP.items()]
        time_combo.grid(row=0, column=5, padx=5)
        time_combo.current(6)  # 주말 4타임 기본 선택
        
        # 조회 버튼
        self.load_btn = ttk.Button(top_frame, text="좌석 현황 조회", command=self.load_seats)
        self.load_btn.grid(row=0, column=6, padx=10)
        
        # 검색 버튼
        self.search_btn = ttk.Button(top_frame, text="🔍 사람 찾기", command=self.search_person)
        self.search_btn.grid(row=0, column=7, padx=5)
        
        # 중간 프레임 
        stats_frame = ttk.Frame(self.root, padding="10")
        stats_frame.pack(fill=tk.X)
        
        self.stats_label = ttk.Label(stats_frame, text="로그인 후 조회 버튼을 클릭하세요", font=("Arial", 12))
        self.stats_label.pack()
        
        # 메인 프레임 
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 스크롤 가능한 캔버스
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        
        self.seat_frame = ttk.Frame(canvas)
        self.seat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.seat_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 범례
        legend_frame = ttk.Frame(self.root, padding="10")
        legend_frame.pack(fill=tk.X)
        
        ttk.Label(legend_frame, text="🟢 예약 가능", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        ttk.Label(legend_frame, text="🔴 예약됨", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        ttk.Label(legend_frame, text="🟡 내 예약", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
    
    def load_seats(self):
        #좌석 현황 조회    
        import threading
        threading.Thread(target=lambda: self.loop.run_until_complete(self.async_load_seats()), daemon=True).start()
    
    async def async_load_seats(self):
        #비동기 좌석 조회
        username = self.username_entry.get()
        password = self.password_entry.get()
        time_code = self.time_var.get().split(" - ")[0]
        
        if not username or not password:
            messagebox.showerror("오류", "아이디와 비밀번호를 입력하세요")
            return
        
        self.load_btn.config(state="disabled", text="조회 중...")
        
        try:
            # 로그인
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            login_result = await intratools.mobile.login.login(self.session, username, password)
            if not login_result:
                messagebox.showerror("오류", "로그인 실패!")
                self.load_btn.config(state="normal", text="좌석 현황 조회")
                return
            
            # 내 정보 가져오기 (이름)
            if not self.my_name:
                num, name, grade, cls = await intratools.mobile.myinfo.get_my_info(self.session)
                self.my_name = name
            
            # 전체 좌석 현황 조회 (reserver_name으로 내 예약 판별)
            payload = {
                "code": "001",
                "t_code": time_code
            }
            
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://go.hana.hs.kr",
                "Referer": "https://go.hana.hs.kr/index.do"
            }
            
            async with self.session.post('https://go.hana.hs.kr/json/hardResvList.ajax', 
                                        data=payload, headers=headers) as resp:
                if resp.status == 200:
                    import json
                    result = json.loads(await resp.text())
                    
                    if 'result' in result:
                        self.seat_data = {}
                        for seat in result['result']:
                            s_code = seat.get('s_code')
                            r_code = seat.get('r_code')
                            
                            # isReser 필드에서 이름 추출 -> 형식은 "학번|이름|아이디"
                            reserver_name = ''
                            if r_code and seat.get('isReser'):
                                parts = seat.get('isReser').split('|')
                                if len(parts) >= 2:
                                    reserver_name = parts[1]  # 이름 부분
                            
                            # 예약자 == 나 ?
                            is_mine = bool(r_code) and reserver_name == self.my_name
                            
                            self.seat_data[s_code] = {
                                'seat_name': seat.get('dis_num'),
                                's_code': s_code,
                                'r_code': r_code,
                                'reserved': bool(r_code),
                                'reserver': reserver_name,
                                'is_mine': is_mine
                            }
                        
                        self.display_seats(time_code)
                        
                        # 통계 업데이트
                        total = len(self.seat_data)
                        reserved = sum(1 for s in self.seat_data.values() if s['reserved'])
                        available = total - reserved
                        mine = sum(1 for s in self.seat_data.values() if s['is_mine'])
                        
                        time_label = TIME_CODE_MAP.get(time_code, f"타임 {time_code}")
                        self.stats_label.config(
                            text=f"{time_label} | 전체: {total}석 | 예약가능: {available}석 | 예약됨: {reserved}석 | 내 예약: {mine}석"
                        )
            
        except Exception as e:
            messagebox.showerror("오류", f"조회 실패: {e}")
        finally:
            self.load_btn.config(state="normal", text="좌석 현황 조회")
    
    def display_seats(self, time_code):
        #좌석을 그리드로 표시 
        # 기존 위젯 제거
        for widget in self.seat_frame.winfo_children():
            widget.destroy()
        
        # 구역별로 좌석 분류 (E, F, G, H 등) * 1학년 A ~ D, 2학년 E ~ H, 3학년 I ~ L
        zones = {}
        for s_code, seat in self.seat_data.items():
            seat_name = seat['seat_name']
            if seat_name:
                zone = seat_name[0]  # 첫 글자 
                if zone not in zones:
                    zones[zone] = []
                zones[zone].append(seat)
        
        # 구역별로 표시
        row = 0
        for zone in sorted(zones.keys()):
            # 구역 헤더
            zone_label = ttk.Label(self.seat_frame, text=f"━━━ {zone}구역 ━━━", 
                                  font=("Arial", 14, "bold"))
            zone_label.grid(row=row, column=0, columnspan=10, pady=10)
            row += 1
            
            # 좌석 버튼
            seats = sorted(zones[zone], key=lambda x: x['seat_name'])
            col = 0
            for seat in seats:
                seat_name = seat['seat_name']
                is_reserved = seat['reserved']
                is_mine = seat['is_mine']
                reserver = seat.get('reserver', '')
                
                # 색상 설정
                if is_mine:
                    bg_color = "#FFD700"  # 내예약
                    text_color = "black"
                    status = "내 예약"
                elif is_reserved:
                    bg_color = "#FF6B6B"  # ㄴㄴ
                    text_color = "white"
                    status = f"예약됨\n{reserver}" if reserver else "예약됨"
                else:
                    bg_color = "#51CF66"  # ㄱㄴ
                    text_color = "white"
                    status = "예약가능"

                seat_container = tk.Frame(self.seat_frame, bg=bg_color, 
                                         relief=tk.RAISED, bd=2,
                                         width=90, height=60,
                                         cursor="hand2")
                seat_container.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
                seat_container.grid_propagate(False)  # 크기 고정

                seat_container.bind("<Button-1>", 
                    lambda e, s=seat, t=time_code: self.on_seat_click(s, t))
                
                # 좌석 레이블
                btn_text = f"{seat_name}\n{status}"
                label = tk.Label(seat_container, text=btn_text,
                               bg=bg_color, fg=text_color,
                               font=("Arial", 9, "bold"),
                               justify=tk.CENTER,
                               cursor="hand2")
                label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
                label.bind("<Button-1>", 
                    lambda e, s=seat, t=time_code: self.on_seat_click(s, t))
                
                col += 1
                if col >= 10:  # 한 줄에 10개씩
                    col = 0
                    row += 1
            
            if col > 0:  # 마지막 줄 처리
                row += 1
    
    def on_seat_click(self, seat, time_code):
        #좌석 클릭 시 예약/취소 처리
        seat_name = seat['seat_name']
        s_code = seat['s_code']
        is_mine = seat['is_mine']
        is_reserved = seat['reserved']
        r_code = seat.get('r_code')
        reserver = seat.get('reserver', '')
        
        time_label = TIME_CODE_MAP.get(time_code, f"타임 {time_code}")
        
        if is_mine:
            # 내 예약 취소하기
            result = messagebox.askyesno(
                "예약 취소",
                f"좌석: {seat_name}\n타임: {time_label}\n\n예약을 취소하시겠습니까?"
            )
            if result:
                import threading
                threading.Thread(target=lambda: self.loop.run_until_complete(self.async_cancel_seat(r_code, time_code)), daemon=True).start()
        elif is_reserved:
            # 다른 사람 정보만 표시
            messagebox.showinfo(
                "예약 정보",
                f"좌석: {seat_name}\n타임: {time_label}\n예약자: {reserver}\n\n다른 사람이 예약한 좌석입니다."
            )
        else:
            # 예약 가능한 자리일 떄 본인 또는 다른 사람 예약 선택
            dialog = tk.Toplevel(self.root)
            dialog.title("예약 옵션")
            dialog.geometry("300x150")
            dialog.transient(self.root)
            dialog.grab_set()
            
            ttk.Label(dialog, text=f"좌석: {seat_name}\n타임: {time_label}", 
                     font=("Arial", 11)).pack(pady=10)
            
            def reserve_mine():
                dialog.destroy()
                import threading
                threading.Thread(target=lambda: self.loop.run_until_complete(
                    self.async_reserve_seat(s_code, time_code, None)), daemon=True).start()
            
            def reserve_other():
                dialog.destroy()
                # 이름 입력
                name_dialog = tk.Toplevel(self.root)
                name_dialog.title("다른 사람 예약")
                name_dialog.geometry("300x120")
                name_dialog.transient(self.root)
                name_dialog.grab_set()
                
                ttk.Label(name_dialog, text="예약할 사람의 이름:").pack(pady=10)
                name_entry = ttk.Entry(name_dialog, width=20)
                name_entry.pack(pady=5)
                name_entry.focus()
                
                def confirm():
                    other_name = name_entry.get().strip()
                    if other_name:
                        name_dialog.destroy()
                        import threading
                        threading.Thread(target=lambda: self.loop.run_until_complete(
                            self.async_reserve_seat(s_code, time_code, other_name)), daemon=True).start()
                    else:
                        messagebox.showerror("오류", "이름을 입력하세요")
                
                ttk.Button(name_dialog, text="확인", command=confirm).pack(pady=10)
                name_entry.bind('<Return>', lambda e: confirm())
            
            ttk.Button(dialog, text="내 이름으로 예약", command=reserve_mine, width=20).pack(pady=5)
            ttk.Button(dialog, text="다른 사람 이름으로 예약", command=reserve_other, width=20).pack(pady=5)
    
    async def async_reserve_seat(self, s_code, time_code, other_name=None):
        #비동기 좌석 예약
        try:
            result = await intratools.mobile.studyroom.reserve_studyroom(
                self.session, s_code, time_code
            )
            
            print(f"예약 API 응답: {result}")  # 디버깅용
            
            #형식: {'result': 'success'}
            if result['result'] == 'success':
                who = other_name if other_name else "본인"
                messagebox.showinfo("성공", f"{who}의 예약이 완료되었습니다!")
                # 좌석 현황 새로고침
                await self.async_load_seats()
            else:
                error_msg = result.get('resultMsg', result.get('resultText', '예약 실패'))
                messagebox.showerror(f"예약 실패: {error_msg}")
        except Exception as e:
            messagebox.showerror("오류", f"예약 오류: {e}")
    
    async def async_cancel_seat(self, r_code, time_code):
        #비동기 좌석 취소
        try:
            result = await intratools.mobile.studyroom.cancel_studyroom(
                self.session, r_code, time_code
            )
            
            print(f"취소 API 응답 타입: {type(result)}, 내용: {result}")  # 디버깅용
            
            # result가 dict가 아닌 경우 처리
            if isinstance(result, dict):
                if result.get('result') == 'success' or result.get('resultType') == 'ok':
                    messagebox.showinfo("성공", "예약이 취소되었습니다!")
                    await self.async_load_seats()
                else:
                    error_msg = result.get('resultMsg', result.get('resultText', str(result)))
                    messagebox.showerror("실패", f"취소 실패: {error_msg}")
            else:
                # 문자열 응답인 경우
                result_str = str(result).lower()
                if 'success' in result_str or 'ok' in result_str:
                    messagebox.showinfo("성공", "예약이 취소되었습니다!")
                    await self.async_load_seats()
                else:
                    messagebox.showerror("실패", f"취소 실패: {result}")
        except Exception as e:
            print(f"취소 오류 상세: {type(e).__name__}: {e}")
            messagebox.showerror("오류", f"취소 오류: {e}")
    
    def search_person(self):
        #사람 찾기
        if not self.seat_data:
            messagebox.showwarning("알림", "먼저 좌석 현황을 조회하세요")
            return
        
        # 검색 다이얼로그
        search_dialog = tk.Toplevel(self.root)
        search_dialog.title("사람 찾기")
        search_dialog.geometry("400x300")
        search_dialog.transient(self.root)
        search_dialog.grab_set()
        
        ttk.Label(search_dialog, text="이름 검색:", font=("Arial", 11)).pack(pady=10)
        search_entry = ttk.Entry(search_dialog, width=30)
        search_entry.pack(pady=5)
        search_entry.focus()
        
        result_frame = ttk.Frame(search_dialog)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        result_text = scrolledtext.ScrolledText(result_frame, width=45, height=12, font=("Arial", 10))
        result_text.pack(fill=tk.BOTH, expand=True)
        
        def do_search():
            query = search_entry.get().strip()
            if not query:
                messagebox.showwarning("알림", "검색할 이름을 입력하세요")
                return
            
            result_text.delete(1.0, tk.END)
            found = []
            
            for s_code, seat in self.seat_data.items():
                if seat['reserved'] and query in seat.get('reserver', ''):
                    found.append(seat)
            
            if found:
                time_code = self.time_var.get().split(" - ")[0]
                time_label = TIME_CODE_MAP.get(time_code, f"타임 {time_code}")
                result_text.insert(tk.END, f"=== '{query}' 검색 결과 ({time_label}) ===\n\n")
                for seat in found:
                    result_text.insert(tk.END, 
                        f"좌석: {seat['seat_name']}\n"
                        f"예약자: {seat['reserver']}\n"
                        f"예약코드: {seat['r_code']}\n"
                        f"{'-'*30}\n"
                    )
                result_text.insert(tk.END, f"\n총 {len(found)}개 좌석 발견")
            else:
                result_text.insert(tk.END, f"'{query}' 이름으로 예약된 좌석이 없습니다.")
        
        ttk.Button(search_dialog, text="검색", command=do_search).pack(pady=5)
        search_entry.bind('<Return>', lambda e: do_search())
    
    def on_closing(self):
        #창 닫기
        if self.session:
            self.loop.run_until_complete(self.session.close())
        self.loop.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = StudyroomViewer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
