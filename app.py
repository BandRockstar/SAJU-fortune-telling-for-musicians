import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(
    page_title="정통 사주 분석", 
    page_icon="☯️",
    layout="centered"
)

# 모바일 가독성 향상 CSS
st.markdown("""
    <style>
    .main { padding: 10px; }
    .stInfo { font-size: 0.95rem; line-height: 1.6; }
    div[data-testid="column"] { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("☯️ 정통 사주 명리 분석")

# 2. 사주 정보 입력 섹션 (1층 - 연도 입력창 복구)
with st.expander("📝 내 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="", placeholder="이름을 입력하세요")
    
    # 생년월일 입력
    c1, c2, c3 = st.columns(3)
    with c1: year = st.number_input("출생년", 1900, 2026, 1985)
    with c2: month = st.number_input("월", 1, 12, 8)
    with c3: day = st.number_input("일", 1, 31, 13)

    # 출생 시간 선택
    birth_time = st.selectbox("출생 시간", [
        "모름", "23:30~01:30 자시 (子)", "01:30~03:30 축시 (丑)", "03:30~05:30 인시 (寅)",
        "05:30~07:30 묘시 (卯)", "07:30~09:30 진시 (辰)", "09:30~11:30 사시 (巳)",
        "11:30~13:30 오시 (午)", "13:30~15:30 미시 (未)", "15:30~17:30 신시 (申)",
        "17:30~19:30 유시 (酉)", "19:30~21:30 술시 (戌)", "21:30~23:30 해시 (亥)"
    ], index=11)
    
    # 달력 및 성별
    col_r1, col_r2 = st.columns(2)
    with col_r1: calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    with col_r2: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    # [복구된 부분] 운세를 보고 싶은 연도 입력
    target_year = st.number_input("📊 운세를 보고 싶은 연도", min_value=1900, max_value=2100, value=2026)
    
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달")
    else:
        is_leap_month = False

# 3. 분석 버튼
if st.button("🎭 내 사주 결과 확인하기", use_container_width=True):
    if name:
        # 데이터 변환 로직
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_date = f"양력 {year}-{month:02d}-{day:02d}"
        else:
            lunar_obj = Lunar.fromYmd(year, month, day)
            display_date = f"음력 {year}-{month:02d}-{day:02d}" + (" (윤)" if is_leap_month else "")

        # 시주 보정 및 8글자 추출
        if birth_time == "모름":
            precise_eight_char = lunar_obj.getEightChar()
        else:
            t_zi_char = birth_time.split("(")[1][0]
            h_map = {"子":0,"丑":2,"寅":4,"卯":6,"辰":8,"巳":10,"午":12,"未":14,"申":16,"酉":18,"戌":20,"亥":22}
            target_h = h_map.get(t_zi_char, 0)
            precise_eight_char = (Solar.fromYmdHms(year, month, day, target_h, 0, 0) if calendar_type == "양력" else Lunar.fromYmdHms(year, month, day, target_h, 0, 0)).getEightChar()

        # 한글 변환 맵
        g_k = {"甲":"갑", "乙":"을", "丙":"병", "丁":"정", "戊":"무", "己":"기", "庚":"경", "辛":"신", "壬":"임", "癸":"계"}
        z_k = {"子":"자", "丑":"축", "寅":"인", "卯":"묘", "辰":"진", "巳":"사", "午":"오", "未":"미", "申":"신", "酉":"유", "戌":"술", "亥":"해"}

        def f_gz(gz):
            if not gz: return "?", "?"
            return f"{gz[0]}({g_k.get(gz[0],'')})", f"{gz[1]}({z_k.get(gz[1],'')})"

        y_g, y_z = f_gz(precise_eight_char.getYear())
        m_g, m_z = f_gz(precise_eight_char.getMonth())
        d_g, d_z = f_gz(precise_eight_char.getDay())
        t_g, t_z = f_gz(precise_eight_char.getTime())

        # 2층: 사주 원국 (모바일 최적화 2x2)
        st.subheader("📊 사주 원국")
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1: st.info(f"**시주**\n\n{t_g}\n{t_z}")
        with r1_c2: st.info(f"**일주**\n\n{d_g}\n{d_z}")
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1: st.info(f"**월주**\n\n{m_g}\n{m_z}")
        with r2_c2: st.info(f"**년주**\n\n{y_g}\n{y_z}")

        # 3층: 삼재 분석 (입력한 target_year 기준)
        st.markdown("---")
        my_y_z = precise_eight_char.getYear()[1]
        s_groups = {"申":["寅","卯","辰"],"子":["寅","卯","辰"],"辰":["寅","卯","辰"],"寅":["申","酉","戌"],"午":["申","酉","戌"],"戌":["申","酉","戌"],"巳":["亥","子","丑"],"酉":["亥","子","丑"],"丑":["亥","子","丑"],"亥":["巳","午","未"]}
        t_solar = Solar.fromYmd(target_year, 1, 1)
        t_y_z = t_solar.getLunar().getEightChar().getYear()[1]
        
        if t_y_z in s_groups.get(my_y_z, []):
            st.error(f"🚫 **{target_year}년 삼재 해당** (조심이 필요합니다)")
        else:
            st.success(f"✅ **{target_year}년 삼재 아님** (평온한 흐름입니다)")

        # 4층: 정통 명리 심층 통변
        st.markdown("---")
        st.subheader("📜 정밀 분석 리포트")
        
        g_e = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
        z_e = {"寅":"木","卯":"木","巳":"火","午":"火","申":"金","酉":"金","亥":"水","子":"水","辰":"土","戌":"土","丑":"土","未":"土"}
        all_c = [y_g[0], y_z[0], m_g[0], m_z[0], d_g[0], d_z[0], t_g[0], t_z[0]]
        cnt = {k: 0 for k in ["木", "火", "土", "金", "水"]}
        for c in all_c:
            if c in g_e: cnt[g_e[c]] += 1
            elif c in z_e: cnt[z_e[c]] += 1

        st.write(f"**[{name}님 오행 분포]**")
        st.code(" | ".join([f"{k}:{v}" for k in ["木", "火", "土", "金", "水"]]))
        
        max_v = max(cnt, key=cnt.get)
        p1 = f"{name}님은 현재 {max_v}의 기운이 {cnt[max_v]}개로 가장 강성합니다. "
        p1 += "주관이 뚜렷하고 신념을 관철하는 강인한 성정입니다. " if cnt[max_v] >= 3 else "매사에 원만하고 균형 감각이 뛰어난 성품입니다. "
        
        my_element = g_e.get(d_g[0],'')
        p2 = f"일간 {d_g[0]}은 {my_element}를 상징하며, "
        p2 += {"木":"어질고 진취적인 마음을,", "火":"열정적이고 명랑한 표현력을,", "土":"신중하고 두터운 신의를,", "金":"날카로운 결단력과 완벽함을,", "水":"유연하고 깊은 지혜를"}.get(my_element, "")
        p2 += " 갖춘 명조입니다. "

        p3 = "주체적인 환경에서 본인의 역량을 발휘할 때 가장 효율적입니다." if z_e.get(m_z[0],'') == my_element else "주어진 상황을 분석하여 실질적인 결과를 내는 능력이 탁월합니다."
        
        st.info(f"{p1}\n\n{p2}\n\n{p3}")

    else:
        st.warning("성함을 입력해 주세요.")
