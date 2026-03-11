import streamlit as st
from lunar_python import Solar, Lunar
import pandas as pd

st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

st.markdown("""
<style>
.main-title{text-align:center;margin-bottom:30px;font-size:36px;font-weight:700}
.card{background:#f8fafc;padding:20px;border-radius:12px;margin-bottom:20px}
.saju-table{width:100%;text-align:center;font-size:22px}
.ohaeng-bar{height:18px;background:#6366f1;border-radius:6px}
.report{line-height:1.8;font-size:17px}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎸 음악인을 위한 사주통변</div>", unsafe_allow_html=True)

name=st.text_input("이름")

c1,c2,c3=st.columns(3)
with c1:
    year=st.number_input("출생년",1900,2100,1981)
with c2:
    month=st.number_input("출생월",1,12,2)
with c3:
    day=st.number_input("출생일",1,31,7)

hour=st.selectbox("출생시간",[
"모름","23~01 자시","01~03 축시","03~05 인시","05~07 묘시",
"07~09 진시","09~11 사시","11~13 오시","13~15 미시",
"15~17 신시","17~19 유시","19~21 술시","21~23 해시"
])

cal=st.radio("달력",["양력","음력"])

target_year=st.number_input("운세 연도",1900,2100,2026)

run=st.button("사주 분석")

hour_map={
"모름":None,
"23~01 자시":0,"01~03 축시":2,"03~05 인시":4,"05~07 묘시":6,
"07~09 진시":8,"09~11 사시":10,"11~13 오시":12,
"13~15 미시":14,"15~17 신시":16,"17~19 유시":18,
"19~21 술시":20,"21~23 해시":22
}

ohaeng_map={
'목':'甲乙寅卯',
'화':'丙丁巳午',
'토':'戊己辰戌丑未',
'금':'庚辛申酉',
'수':'壬癸亥子'
}

def calc_ohaeng(chars):
    result={}
    for k,v in ohaeng_map.items():
        result[k]=sum(c in v for c in chars)
    return result

def music_report(elem):

    data={
    "목":"서정적 멜로디와 감성적 작곡 능력이 강합니다. 어쿠스틱, 포크, 서사적 음악에 강점을 보입니다.",
    "화":"무대 장악력과 퍼포먼스 에너지가 강합니다. 보컬 중심 음악에서 강한 매력을 발휘합니다.",
    "토":"밴드 전체 밸런스를 잡는 능력이 좋으며 프로듀싱 감각이 뛰어납니다.",
    "금":"정교한 연주력과 사운드 디자인 감각이 뛰어납니다. 기타리스트나 엔지니어 성향.",
    "수":"몽환적이고 깊은 음악 세계를 만듭니다. 재즈, 앰비언트, 실험음악과 궁합이 좋습니다."
    }

    return data.get(elem,"")

if run:

    try:

        h=hour_map[hour]

        if cal=="양력":
            if h is None:
                lunar=Solar.fromYmd(year,month,day).getLunar()
            else:
                lunar=Solar.fromYmdHms(year,month,day,h,0,0).getLunar()
        else:
            lunar=Lunar.fromYmd(year,month,day)

        year_gz=lunar.getYearInGanZhi()
        month_gz=lunar.getMonthInGanZhi()
        day_gz=lunar.getDayInGanZhi()

        if h is None:
            time_gz="?"
        else:
            time_gz=lunar.getTimeInGanZhi()

        gan=[year_gz[0],month_gz[0],day_gz[0],time_gz[0] if time_gz!="?" else "?"]
        ji=[year_gz[1],month_gz[1],day_gz[1],time_gz[1] if time_gz!="?" else "?"]

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        df=pd.DataFrame({
        "": ["천간","지지"],
        "년주":[gan[0],ji[0]],
        "월주":[gan[1],ji[1]],
        "일주":[gan[2],ji[2]],
        "시주":[gan[3],ji[3]]
        })

        st.table(df)

        st.markdown("</div>",unsafe_allow_html=True)

        chars=year_gz+month_gz+day_gz+(time_gz if time_gz!="?" else "")

        counts=calc_ohaeng(chars)

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        st.subheader("오행 균형")

        for k,v in counts.items():
            st.write(k)
            st.markdown(f"<div class='ohaeng-bar' style='width:{v*60}px'></div>",unsafe_allow_html=True)

        max_elem=max(counts,key=counts.get)

        st.success(f"주요 오행 : {max_elem}")

        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("<div class='card report'>",unsafe_allow_html=True)

        st.subheader("음악적 재능 분석")

        st.write(music_report(max_elem))

        st.markdown("</div>",unsafe_allow_html=True)

        zodiac=lunar.getYearZhi()

        samjae_map={
        '申子辰':['寅','卯','辰'],
        '亥卯未':['巳','午','未'],
        '寅午戌':['申','酉','戌'],
        '巳酉丑':['亥','子','丑']
        }

        group=[]

        for k,v in samjae_map.items():
            if zodiac in k:
                group=v

        tz=Solar.fromYmd(target_year,1,1).getLunar().getYearZhi()

        if tz in group:
            idx=group.index(tz)
            msg=["들삼재","눌삼재","날삼재"][idx]
        else:
            msg="삼재 아님"

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        st.subheader("삼재")

        st.write(f"{target_year}년 : {msg}")

        st.markdown("</div>",unsafe_allow_html=True)

    except Exception as e:

        st.error("사주 계산 오류")
        st.write(e)
```
