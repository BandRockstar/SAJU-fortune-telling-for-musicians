import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정 (모바일 브라우저 최적화)
st.set_page_config(
    page_title="정통 사주 분석", 
    page_icon="☯️",
    layout="centered"  # 모바일 가독성을 위해 중앙 정렬
)

# 모바일용 커스텀 CSS (카드 스타일 및 폰트 크기 조정)
st.markdown("""
    <style>
    .main { padding: 10px; }
    .stInfo { font-size: 0.95rem; line-height: 1.6; }
    div[data-testid="column"] { margin-bottom: -15px; }
    .stCodeBlock { padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("☯️ 정통 사주 명리 분석")

# 2. 사주 정보 입력 섹션 (1층)
with st.expander("📝 내 사주 정보 입력", expanded=True):
    name = st.text_input("성함", value="", placeholder="이름을 입력하세요")
    
    # 날짜 입력 한 줄로 배치 (모바일 대응)
    c1, c2, c3 = st.columns(3)
    with c1: year = st.number_input("년", 1900, 2026, 1985)
    with c2: month = st.number_input("월", 1, 12, 8)
    with c3: day = st.number_input("일", 1, 31, 13)

    birth_time = st.selectbox("출생 시간", [
        "모름", "23:30~01:30 자시 (子)", "01:30~03:30 축시 (丑)", "03:30~05:30 인시 (寅)",
        "05:30~07:30 묘시 (卯)", "07:30~09:30 진시 (辰)", "09:30~11:30 사시 (巳)",
        "11:30~13:30 오시 (午)", "13:30~15:30 미시 (未)", "15:30~17:30 신시 (申)",
        "17:30~19:30 유시 (酉)", "19:30~21:30 술시 (戌)", "21:30~23:30 해시 (亥)"
    ], index=11) # 술시 기본값
    
    col_radio1, col_radio2 = st.columns(2)
    with col_radio1: calendar_type = st.radio("달력", ["양력", "음력"], horizontal=True)
    with col_radio2: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달")
    else:
        is_leap_month = False

# 3. 분석 버튼 (모바일에서 누르기 좋게 크게)
if st.button("🎭 내 사주 결과 확인하기", use_container_width=True):
    if name:
        # 데이터 처리 (라이브러리 연동)
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_date = f"양력 {year}-{month:02d}-{day:02d}"
        else:
            lunar_obj = Lunar.fromYmd(year, month, day)
            display_date = f"음력 {year}-{month:02d}-{day:02d}" + (" (윤)" if is_leap_month else "")

        eight_char = lunar_obj.getEightChar()
        gan_ko = {"甲":"갑", "乙":"을", "丙":"병", "丁":"정", "戊":"무", "己":"기", "庚":"경", "辛":"신", "壬":"임", "癸":"계"}
        zi_ko = {"子":"자", "丑":"축", "寅":"인", "卯":"묘", "辰":"진", "巳":"사", "午":"오", "未":"미", "申":"신", "酉":"유", "戌":"술", "亥":"해"}

        def fmt(gz):
            if not gz: return "?", "?"
            return f"{gz[0]}({gan_ko.get(gz[0],'')})", f"{gz[1]}({zi_ko.get(gz[1],'')})"

        # 시간 보정 로직
        if birth_time == "모름":
            t_gan, t_zi = "?", "?"
            precise_eight_char = eight_char
        else:
            target_hour = {"子":0,"丑":2,"寅":4,"卯":6,"辰":8,"巳":10,"午":12,"未":14,"申":16,"酉":18,"戌":20,"亥":22}.get(birth_time.split("(")[1][0], 0)
            precise_eight_char = (Solar.fromYmdHms(year, month, day, target_hour, 0, 0) if calendar_type == "양력" else Lunar.fromYmdHms(year, month, day, target_hour, 0, 0)).getEightChar()
            t_gan, t_zi = fmt(precise_eight_char.getTime())

        y_gan, y_zi = fmt(precise_eight_char.getYear())
        m_gan, m_zi = fmt(precise_eight_char.getMonth())
        d_gan, d_zi = fmt(precise_eight_char.getDay())

        # 2층: 사주 원국 (모바일 2x2 그리드)
        st.subheader("📊 사주 원국")
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1: st.info(f"**시주**\n\n{t_gan}\n{t_zi}")
        with r1_c2: st.info(f"**일주**\n\n{d_gan}\n{d_zi}")
        
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1: st.info(f"**월주**\n\n{m_gan}\n{m_zi}")
        with r2_c2: st.info(f"**년주**\n\n{y_gan}\n{y_zi}")

        # 3층: 삼재 (심플 카드)
        my_year_zi = precise_eight_char.getYear()[1]
        samjae_groups = {"申":["寅","卯","辰"],"子":["寅","卯","辰"],"辰":["寅","卯","辰"],"寅":["申","酉","戌"],"午":["申","酉","戌"],"戌":["申","酉","戌"],"巳":["亥","子","丑"],"酉":["亥","子","丑"],"丑":["亥","子","丑"],"亥":["巳","午","미"]}
        target_zi = Solar.fromYmd(2026, 1, 1).getLunar().getEightChar().getYear()[1]
        
        st.markdown("---")
        if target_zi in samjae_groups.get(my_year_zi, []):
            st.error("🚫 **2026년 삼재 해당** (조심이 필요한 시기)")
        else:
            st.success("✅ **2026년 삼재 아님** (평온한 운의 흐름)")

        # 4층: 심층 통변 (가독성 강화)
        st.markdown("---")
        st.subheader("📜 정밀 분석 리포트")
        
        gan_ele = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
        zi_ele = {"寅":"木","卯":"木","巳":"火","午":"火","申":"金","酉":"金","亥":"水","子":"水","辰":"土","戌":"土","丑":"土","未":"土"}
        all_c = [y_gan[0], y_zi[0], m_gan[0], m_zi[0], d_gan[0], d_zi[0], t_gan[0], t_zi[0]]
        counts = {k: 0 for k in ["木", "火", "土", "金", "水"]}
        for c in all_c:
            if c in gan_ele: counts[gan_ele[c]] += 1
            elif c in zi_ele: counts[zi_ele[c]] += 1

        # 오행 요약 바(Bar)
        st.write(f"**[{name}님 오행 분포]**")
        st.code(" | ".join([f"{k}:{v}" for k, v in counts.items()]))
        st.caption(f"본인 일간: {d_gan[0]} ({gan_ele.get(d_gan[0],'')})")

        # 실시간 조립 통변
        max_e = max(counts, key=counts.get)
        p1 = f"{name}님은 현재 {max_e}의 기운이 {counts[max_e]}개로 가장 강성합니다. "
        p1 += "주관이 뚜렷하고 신념을 관철하는 강인한 성정입니다. " if counts[max_e] >= 3 else "매사에 원만하고 균형 감각이 뛰어난 성품입니다. "
        
        my_e = gan_ele.get(d_gan[0],'')
        p2 = f"일간 {d_gan[0]}은 {my_e}를 상징하며, "
        p2 += {"木":"창의적인 기획력과 진취적인 마음을,", "火":"열정적이고 강력한 표현력을,", "土":"신중하고 변함없는 신의를,", "金":"냉철한 결단력과 완벽주의적 성향을,", "水":"유연하고 깊은 감수성과 영감을"}.get(my_e, "")
        p2 += " 지니고 있습니다. "

        p3 = "주체적인 환경에서 역량을 발휘할 때 성과가 큽니다." if zi_ele.get(m_zi[0],'') == my_e else "현실적인 상황 분석과 결과 도출 능력이 탁월합니다."
        
        st.info(f"{p1}\n\n{p2}\n\n{p3}")

    else:
        st.warning("성함을 입력해 주세요.")
