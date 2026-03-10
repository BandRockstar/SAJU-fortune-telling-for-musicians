import streamlit as st
from korean_lunar_calendar import KoreanLunarCalendar
import pandas as pd
import datetime

st.set_page_config(page_title="뮤지션을 위한 사주보기", layout="wide")
st.title("🎸 뮤지션을 위한 사주보기")

element_map = {
"甲":"목","乙":"목",
"丙":"화","丁":"화",
"戊":"토","己":"토",
"庚":"금","辛":"금",
"壬":"수","癸":"수",
"寅":"목","卯":"목",
"巳":"화","午":"화",
"辰":"토","戌":"토","丑":"토","未":"토",
"申":"금","酉":"금",
"亥":"수","子":"수"
}

ten_gods = {
"목":{"목":"비견","화":"식신","토":"편재","금":"편관","수":"편인"},
"화":{"목":"편인","화":"비견","토":"식신","금":"편재","수":"편관"},
"토":{"목":"편관","화":"편인","토":"비견","금":"식신","수":"편재"},
"금":{"목":"편재","화":"편관","토":"편인","금":"비견","수":"식신"},
"수":{"목":"식신","화":"편재","토":"편관","금":"편인","수":"비견"}
}

hour_branch = {
"자(23-01)":"子","축(01-03)":"丑","인(03-05)":"寅","묘(05-07)":"卯",
"진(07-09)":"辰","사(09-11)":"巳","오(11-13)":"午","미(13-15)":"未",
"신(15-17)":"申","유(17-19)":"酉","술(19-21)":"戌","해(21-23)":"亥"
}

st.header("출생 정보")

c1,c2,c3 = st.columns(3)

gender = c1.selectbox("성별",["남","여"])
calendar_type = c2.selectbox("달력",["양력","음력"])
leap = c3.selectbox("윤달",["아니오","윤달"])

c4,c5,c6 = st.columns(3)

year = int(c4.number_input("출생 연도",1900,2050,1985))
month = int(c5.number_input("출생 월",1,12,1))
day = int(c6.number_input("출생 일",1,31,1))

hour = st.selectbox("출생 시간",[
"모름",
"자(23-01)","축(01-03)","인(03-05)","묘(05-07)",
"진(07-09)","사(09-11)","오(11-13)","미(13-15)",
"신(15-17)","유(17-19)","술(19-21)","해(21-23)"
])

target_year = int(st.number_input("분석할 년도",1900,2050,2026))

if st.button("사주 분석"):

    try:

        if calendar_type == "양력":
            datetime.date(year,month,day)

        cal = KoreanLunarCalendar()

        if calendar_type == "양력":
            cal.setSolarDate(year,month,day)
        else:
            is_leap = True if leap=="윤달" else False
            cal.setLunarDate(year,month,day,is_leap)

        try:
            ganji_raw = cal.getChineseGapJaString()
        except:
            ganji_raw = cal.getGapJaString()

        tokens = (
            ganji_raw
            .replace("년"," ")
            .replace("월"," ")
            .replace("일"," ")
            .strip()
            .split()
        )

        if len(tokens) < 3:
            st.error("사주 계산 실패")
            st.stop()

        year_p = tokens[0][:2]
        month_p = tokens[1][:2]
        day_p = tokens[2][:2]

        hour_p = "--"
        if hour != "모름":
            hour_p = hour_branch[hour]

        pillars = [year_p, month_p, day_p]

        st.header("사주 팔자")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("년주",year_p)
        c2.metric("월주",month_p)
        c3.metric("일주",day_p)
        c4.metric("시지",hour_p)

        elements = {"목":0,"화":0,"토":0,"금":0,"수":0}

        for p in pillars:

            if len(p) != 2:
                continue

            g = p[0]
            j = p[1]

            if g in element_map:
                elements[element_map[g]] += 1

            if j in element_map:
                elements[element_map[j]] += 1

        st.header("오행 분석")

        df = pd.DataFrame({
            "오행": list(elements.keys()),
            "개수": list(elements.values())
        })

        df["개수"] = df["개수"].astype(int)

        st.bar_chart(df.set_index("오행"))

        day_stem = day_p[0]
        day_element = element_map.get(day_stem,"")

        st.header("십신 분석")

        ten_list = []

        for p in pillars:

            g = p[0]
            g_el = element_map.get(g,"")

            if day_element and g_el:
                tg = ten_gods[day_element][g_el]
                ten_list.append((p,tg))

        tg_df = pd.DataFrame(ten_list,columns=["기둥","십신"])
        st.table(tg_df)

        st.header("뮤지션 성향")

        music = []

        if elements["목"]>=2: music.append("작곡 능력")
        if elements["화"]>=2: music.append("무대 퍼포먼스")
        if elements["금"]>=2: music.append("리듬 감각")
        if elements["수"]>=2: music.append("감성 표현")
        if elements["토"]>=2: music.append("밴드 안정형")

        if len(music)==0:
            music.append("올라운드 뮤지션")

        for m in music:
            st.write("•",m)

        st.header("추천 장르")

        genre = []

        if elements["화"]>=2: genre.append("록")
        if elements["목"]>=2: genre.append("블루스")
        if elements["수"]>=2: genre.append("발라드")
        if elements["금"]>=2: genre.append("재즈")
        if elements["토"]>=2: genre.append("팝")

        if len(genre)==0:
            genre.append("올라운드 장르")

        for g in genre:
            st.write("•",g)

        st.header(f"{target_year}년 운세")

        current_year = datetime.datetime.now().year
        diff = target_year - current_year

        if diff > 0:
            st.write("새로운 기회가 생길 가능성")
        elif diff < 0:
            st.write("정리와 재정비의 시기")
        else:
            st.write("변화가 많은 해")

        st.success("분석 완료 🎵")

    except Exception:
        st.error("날짜 입력 오류 또는 사주 계산 실패")
