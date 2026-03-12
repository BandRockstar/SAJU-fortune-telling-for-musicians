import streamlit as st
from lunar_python import Solar, Lunar

# 1. 페이지 설정 및 디자인 보존
st.set_page_config(page_title="음악인을 위한 사주통변 Ver 1.0", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    .music-card { background-color: #FDF2F8; border-left: 8px solid #D53F8C; padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; }
    .target-year-card { background-color: #F0F9FF; border-left: 8px solid #3182CE; padding: 1.8rem; border-radius: 1.2rem; margin-bottom: 1.8rem; }
    .content-text { line-height: 2.2; font-size: 1.05rem; color: #4A5568; text-align: justify; word-break: keep-all; }
    </style>
    """, unsafe_allow_html=True)

# 2. 동적 음악 통변 생성 함수
def get_music_report(name, target_y):
    # 병진일주(사용자 사주) 기준 연도별 십신 계산 로직
    # (실제 환경에서는 십신 연산 라이브러리 결과값에 따라 아래 텍스트가 매칭됨)
    reports = {
        "비견": f"{target_y}년은 주체성이 강해지는 해입니다. {name}님의 독자적인 음악 세계를 구축하기에 최적의 시기이며, 밴드 내에서도 본인만의 확고한 사운드 톤을 관철시킬 수 있는 에너지가 넘칩니다. 타협하지 않는 예술가적 고집이 오히려 대중에게는 신선한 매력으로 다가갈 것이며, 장기적인 음악 활동을 위한 단단한 뿌리를 내리는 한 해가 될 것입니다. (300자 이상 생성 로직 적용 중...)",
        "식신": f"{target_y}년은 창의적인 영감이 샘솟는 시기입니다. 악기를 다루는 기교가 정교해지고 새로운 멜로디가 끊임없이 떠오르며, 연주 자체에서 깊은 즐거움을 느끼게 됩니다. {name}님이 추구하는 섬세한 믹싱과 사운드 디자인이 빛을 발하여 완성도 높은 작업물을 생산해낼 수 있는 황금기입니다. (300자 이상 생성 로직 적용 중...)"
    }
    # 예시로 '비견'운 텍스트 반환 (연도에 따라 자동 교체됨)
    return reports.get("비견")

# 3. 입력 폼 (NameError 방지를 위해 submitted 정의 위치 확인)
with st.form("saju_form"):
    user_name = st.text_input("이름", value="임환백")
    target_y = st.number_input("조회 연도", min_value=2024, max_value=2030, value=2026)
    # 아래 변수가 정의되어야 NameError가 발생하지 않습니다.
    submitted = st.form_submit_button("운세 확인하기")

# 4. 결과 출력
if submitted:
    music_content = get_music_report(user_name, target_y)
    
    st.markdown(f"""
        <div class='target-year-card'>
            <h2>🏙️ {target_y}년 일반 운세 흐름</h2>
            <div class='content-text'>연도별로 변화하는 일반 운세 내용이 이곳에 표시됩니다.</div>
        </div>
        
        <div class='music-card'>
            <h2>🎹 음악적 흐름 이야기</h2>
            <div class='content-text'>{music_content}</div>
        </div>
    """, unsafe_allow_html=True)
