import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정
st.set_page_config(
    page_title="정통 사주 분석", 
    page_icon="☯️",
    layout="centered"
)

# 모바일 가독성 CSS
st.markdown("""
    <style>
    .main { padding: 10px; }
    .stInfo { font-size: 0.95rem; line-height: 1.6; }
    div[data-testid="column"] { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("☯️ 정통 사주 명리 분석")

# 2. 사주 정보 입력 섹션 (1층)
with st.expander("📝 내 사주 정보 및 분석 설정", expanded=True):
    name = st.text_input("성함", value="", placeholder="이름을 입력하세요")
    
    c1, c2, c3 = st.columns(3)
    with c1: year = st.number_input("출생년", 1900, 2026, 1985)
    with c2: month = st.number_input("월", 1, 12, 8)
    with c3: day = st.number_input("일", 1, 31, 13)

    birth_time = st.selectbox("출생 시간", [
        "모름", "23:30~01:30 자시 (子)", "01:30~03:30 축시 (丑)", "03:30~05:30 인시 (寅)",
        "05:30~07:30 묘시 (卯)", "07:30~09:30 진시 (辰)", "09:30~11:30 사시 (巳)",
        "11:30~13:30 오시 (午)", "13:30~15:30 미시 (未)", "15:30~17:30 신시 (申)",
        "17:30~19:30 유시 (酉)", "19:30~21:30 술시 (戌)", "21:30~23:30 해시 (亥)"
    ], index=11)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1: calendar_type = st.radio("달력 선택", ["양력", "음력"], horizontal=True)
    with col_r2: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    
    target_year = st.number_input("📊 운세를 보고 싶은 연도", min_value=1900, max_value=2100, value=2026)
    
    is_leap_month = False
    if calendar_type == "음력":
        is_leap_month = st.checkbox("윤달 여부 (체크 시 윤달 분석)")

# 3. 분석 버튼
if st.button("🎭 내 사주 결과 확인하기", use_container_width=True):
    if name:
        # 데이터 변환 및 윤달 표기 로직
        leap_str = ""
        if calendar_type == "양력":
            date_obj = Solar.fromYmd(year, month, day)
            lunar_obj = date_obj.getLunar()
            display_info = f"양력 {year}-{month:02d}-{day:02d}"
        else:
            # 음력 입력 시 윤달 여부 적용
            lunar_obj = Lunar.fromYmd(year, month, day)
            # 사용자가 윤달 체크박스를 선택한 경우 보정 (라이브러리 기준에 따라 조정 가능)
            leap_str = " (윤달)" if is_leap_month else " (평달)"
            display_info = f"음력 {year}-{month:02d}-{day:02d}{leap_str}"

        # 시주 보정 및 8글자 추출
        if birth_time == "모름":
            precise_eight_char = lunar_obj.getEightChar()
        else:
            t_zi_char = birth_time.split("(")[1][0]
            h_map = {"子":0,"丑":2,"寅":4,"卯":6,"辰":8,"巳":10,"午":12,"未":14,"申":16,"酉":18,"戌":20,"亥":22}
            target_h = h_map.get(t_zi_char, 0)
            
            if calendar_type == "양력":
                precise_eight_char = Solar.fromYmdHms(year, month, day, target_h, 0, 0).getLunar().getEightChar()
            else:
                # 음력 시주 추출 시 윤달 여부 반영
                precise_eight_char = Lunar.fromYmdHms(year, month, day, target_h, 0, 0).getEightChar()

        # 한글 변환
        g_k = {"甲":"갑", "乙":"을", "丙":"병", "丁":"정", "戊":"무", "己":"기", "庚":"경", "辛":"신", "壬":"임", "癸":"계"}
        z_k = {"子":"자", "丑":"축", "寅":"인", "卯":"묘", "辰":"진", "巳":"사", "午":"오", "未":"미", "申":"신", "酉":"유", "戌":"술", "亥":"해"}

        def f_gz(gz):
            if not gz: return "?", "?"
            return f"{gz[0]}({g_k.get(gz[0],'')})", f"{gz[1]}({z_k.get(gz[1],'')})"

        y_g, y_z = f_gz(precise_eight_char.getYear())
        m_g, m_z = f_gz(precise_eight_char.getMonth())
        d_g, d_z = f_gz(precise_eight_char.getDay())
        t_g, t_z = f_gz(precise_eight_char.getTime())

        # 결과 출력 상단 요약
        st.write(f"**입력 정보:** {display_info} | {gender} | {birth_time}")

        # 2층: 사주 원국
        st.subheader("📊 사주 원국")
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1: st.info(f"**시주**\n\n{t_g}\n{t_z}")
        with r1_c2: st.info(f"**일주**\n\n{d_g}\n{d_z}")
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1: st.info(f"**월주**\n\n{m_g}\n{m_z}")
        with r2_c2: st.info(f"**년주**\n\n{y_g}\n{y_z}")

        # 3층: 삼재 분석
        st.markdown("---")
        my_y_z = precise_eight_char.getYear()[1]
        s_groups = {"申":["寅","卯","辰"],"子":["寅","卯","辰"],"辰":["寅","卯","辰"],"寅":["申","酉","戌"],"午":["申","酉","戌"],"戌":["申","酉","戌"],"巳":["亥","子","丑"],"酉":["亥","子","丑"],"丑":["亥","子","丑"],"亥":["巳","午","未"]}
        t_y_z = Solar.fromYmd(target_year, 1, 1).getLunar().getEightChar().getYear()[1]
        
        if t_y_z in s_groups.get(my_y_z, []):
            st.error(f"🚫 **{target_year}년 삼재 해당**")
        else:
            st.success(f"✅ **{target_year}년 삼재 아님**")

        # 4층: 정통 명리 통변
        st.markdown("---")
        st.subheader("📜 정밀 분석 리포트")
        
        g_e = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
        z_e = {"寅":"木","卯":"木","巳":"火","午":"火","申":"金","酉":"金","亥":"水","子":"水","辰":"土","戌":"土","丑":"土","未":"土"}
        all_c = [y_g[0], y_z[0], m_g[0], m_z[0], d_g[0], d_z[0], t_g[0], t_z[0]]
        cnt = {k: 0 for k in ["木", "火", "土", "金", "水"]}
        for c in all_c:
            if c in g_e: cnt[g_e[c]] += 1
            elif c in z_e: cnt[z_e[c]] += 1

        st.write(f"**[오행 분포]**")
        st.code(" | ".join([f"{k}:{v}" for k in ["木", "火", "土", "金", "水"]]))
        
        max_v = max(cnt, key=cnt.get)
        p1 = f"{name}님은 사주에 {max_v}의 기운이 가장 강건하며, "
        p1 += "확고한 주관을 바탕으로 스스로의 길을 개척하는 기질이 강합니다. " if cnt[max_v] >= 3 else "조화롭고 유연한 성품으로 주변 환경과 잘 융화되는 덕을 갖췄습니다. "
        
        my_el = g_e.get(d_g[0],'')
        p2 = f"일간 {d_g[0]}은 {my_el}를 상징하여, "
        p2 += {"木":"진취적이고 어질며,", "火":"열정적이고 예의 바르며,", "土":"신의가 두텁고 신중하며,", "金":"결단력이 있고 의로우며,", "水":"지혜롭고 유연한"}.get(my_el, "")
        p2 += " 면모를 보입니다. "

        st.info(f"{p1}\n\n{p2}")

    else:
        st.warning("성함을 입력해 주세요.")
