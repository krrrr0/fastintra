from getpass import getpass
import asyncio
import aiohttp

import intratools.mobile.login
import intratools.mobile.classroom
import intratools.mobile.myinfo


weekday_times = [1, 4, 28, 1]
weekend_times = [7, 9, 10, 26]


async def main():
    # 인트로
    print("-" * 40)
    print("☆ 로나로나땅 슈퍼차저 V1.0 (주말공휴일용) ☆")
    print("주의: 주말1타임과 주말4타임을 모두 예약할 수 없습니다.")
    print("-" * 40, '\n')

    # 세션 시작
    session = aiohttp.ClientSession()

    # 로그인
    username = input("인트라넷 아이디 입력: ")
    password = getpass("인트라넷 비밀번호 입력: ")

    login_result = await intratools.mobile.login.login(session, username, password)
    if not login_result:
        print("[오류] 로그인 실패! 다시 시도하세요.")
        await session.close()
        return

    # 예약 정보 입력받기
    resv_time = int(input("\n예약할 타임 코드 입력 (주말1타임: 7, 주말2타임: 9, 주말3타임: 10, 주말4타임: 26): "))
    if resv_time not in weekend_times:
        print("[오류] 올바르지 않은 타임 코드입니다. 다시 시도하세요.")
        await session.close()
        return
    resv_class = input("예약할 호실 입력 (교과동만 가능): ")
    resv_status = "승인" if input("승인 만들기 여부 (많이 늦었을 경우) [Y/N]: ") == "Y" else "대기"

    stu_num, stu_name, _, _ = await intratools.mobile.myinfo.get_my_info(session)

    # 1단계: 평일 타임으로 미승인 만들기
    tmp_result = await intratools.mobile.classroom.reserve_class(session, weekday_times[weekend_times.index(resv_time)], "A204", "dorm", stu_num, resv_status)
    if tmp_result['resultType'] != 'ok':
        print("[경고] 임시 예약 생성 실패! 계속 진행합니다.")

    # 2단계: 방금 만든 미승인 예약번호 가져오기
    resv_list = await intratools.mobile.classroom.get_cls_resv_list(session, stu_name)
    
    tmp_id = 0
    for r in resv_list:
        if str(r.user.number) == str(stu_num) and str(r.time) == str(weekday_times[weekend_times.index(resv_time)]):
            tmp_id = r.index
            
    if tmp_id == 0:
        print("[오류] 수정할 임시 예약을 찾을 수 없습니다!")
        await session.close()
        return
    
    # 3단계: 임시 예약 내용 수정하기
    await intratools.mobile.classroom.edit_class(session, tmp_id, resv_time, resv_class, "dorm", stu_num, resv_status)

    # 4단계: 결과확인
    result = await intratools.mobile.classroom.get_cls_resv_list(session, stu_name)

    print("\n성공! - 예약 내역입니다:")
    print("-" * 40)
    print("학번", "타임", "상태", "예약번호", sep="\t")
    print("-" * 40)
    for r in result:
        print(r.user.number, r.time, r.status, r.index, sep="\t")

    print("-" * 40)

    await session.close()

    input("Press [Enter] to continue...")
    return

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())