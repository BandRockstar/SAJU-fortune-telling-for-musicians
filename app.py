import streamlit as st
from lunar_python import Solar, Lunar

st.set_page_config(page_title="음악인을 위한 사주통변", layout="centered")

st.markdown("""
<style>
.main-title{text-align:center;margin-bottom:20px}
.saju-grid{display:flex;gap:10px;margin-bottom:20px}
.saju-box{flex:1;background:#f1f5f9;padding:15px;border-radius:10px;text-align:center;font-size:20px}
.ohaeng{margin-top:20px}
.bar{height:20px;background:#4f46e5;margin:5px 0;border-radius:5px}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎸 음악인을 위한 사주통변</h1>", unsafe_allow_html=True)

# 입력
name = st.text_input("이름")

col1,col2,col3 = st.columns(3)

with col1:
    year = st.number_input("출생년",1900,2100,1981)

with col2:
    month = st.number_input("출생월",1,12,2)

with col3:
    day = st.number_input("출생일",1,31,7)

hour = st.selectbox("출생시간",[
"모름","23~01 자시","01~03 축시","03~05 인시","05~07 묘시",
"07~09 진시","09~11 사시","11~13 오시","13~15 미시",
"15~17 신시","17~19 유시","19~21 술시","21~23 해시"
])

cal = st.radio("달력",["양력","음력"])

target_year = st.number_input("운세 연도",1900,2100,2026)

run = st.button("사주 분석")

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

        st.subheader("사주 팔자")

        st.markdown(f"""
        <div class="saju-grid">
        <div class="saju-box">년주<br>{year_gz}</div>
        <div class="saju-box">월주<br>{month_gz}</div>
        <div class="saju-box">일주<br>{day_gz}</div>
        <div class="saju-box">시주<br>{time_gz}</div>
        </div>
        """,unsafe_allow_html=True)

        chars=year_gz+month_gz+day_gz+(time_gz if time_gz!="?" else "")

        counts=calc_ohaeng(chars)

        st.subheader("오행 분석")

        for k,v in counts.items():

            st.write(k)

            st.markdown(f"<div class='bar' style='width:{v*40}px'></div>",unsafe_allow_html=True)

        max_elem=max(counts,key=counts.get)

        st.success(f"가장 강한 오행 : {max_elem}")

        st.subheader("삼재")

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

        st.write(f"{target_year}년 : {msg}")

    except Exception as e:

        st.error("사주 계산 오류")

        st.write(e)
