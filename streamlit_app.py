import streamlit as st

# Streamlit 페이지 설정
st.set_page_config(
    page_title="교사 번아웃 체크!",
    page_icon="🍎",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- CSS 스타일링 (Tailwind CSS 대신 직접 스타일링) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 700;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
    h2 {
        color: #34495e;
        margin-top: 25px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 12px;
        padding: 10px 25px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        display: block;
        margin: 20px auto;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }
    .stSlider>div>div>div>div {
        background-color: #3498db;
    }
    .stSlider>div>div>div>div>div {
        background-color: #2980b9;
    }
    .result-box {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 30px;
        margin-top: 40px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        text-align: center;
    }
    .result-title {
        font-size: 2.2em;
        font-weight: bold;
        color: #27ae60; /* 기본 색상 */
        margin-bottom: 15px;
    }
    .result-animal {
        font-size: 1.8em;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .result-description {
        font-size: 1.1em;
        line-height: 1.6;
        color: #555;
    }
    .burnout-level-0 .result-title { color: #27ae60; } /* 활기찬 돌고래 */
    .burnout-level-1 .result-title { color: #2ecc71; } /* 평온한 코알라 */
    .burnout-level-2 .result-title { color: #f1c40f; } /* 고민하는 부엉이 */
    .burnout-level-3 .result-title { color: #e67e22; } /* 지친 나무늘보 */
    .burnout-level-4 .result-title { color: #e74c3c; } /* 쓰러진 낙타 */

    .resource-box {
        background-color: #ecf0f1;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .resource-box h3 {
        color: #34495e;
        margin-bottom: 10px;
    }
    .resource-box ul {
        list-style-type: disc;
        margin-left: 20px;
    }
    .resource-box li {
        margin-bottom: 8px;
        color: #555;
    }
    .resource-box a {
        color: #3498db;
        text-decoration: none;
    }
    .resource-box a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# --- 설문 문항 정의 ---
questions = [
    "최근 업무에 대한 열정이 줄어들고 무기력함을 느낍니다.",
    "학생들을 가르치는 일에 흥미를 잃고 형식적으로 느껴질 때가 많습니다.",
    "업무 스트레스로 인해 쉽게 짜증이 나거나 분노를 느낍니다.",
    "동료 교사나 학생, 학부모와의 관계에서 감정적으로 지쳐있다고 느낍니다.",
    "수면의 질이 나빠지거나 식욕 부진 등 신체적인 불편함을 겪고 있습니다.",
    "업무 외 활동이나 개인적인 취미 생활에 대한 의욕이 없습니다.",
    "교직에 대한 회의감이 들고 다른 직업을 고민하게 됩니다.",
    "작은 일에도 집중하기 어렵고, 기억력이 나빠진 것 같습니다.",
    "아침에 일어나는 것이 힘들고, 학교 가는 것이 부담스럽게 느껴집니다.",
    "내 노력이 학생들에게 아무런 영향을 주지 못하는 것 같습니다."
]

# --- 번아웃 등급 및 동물 비유 정의 ---
burnout_levels = [
    {
        "title": "번아웃 없음: 활기찬 돌고래 🐬",
        "animal": "활기찬 돌고래",
        "description": "당신은 현재 교직 생활에 대한 높은 만족도와 에너지를 가지고 있습니다. 긍정적인 태도로 업무에 임하고 있으며, 스트레스 관리도 잘하고 계십니다. 지금처럼 활기찬 모습을 유지하며 학생들에게 좋은 영향을 계속 주세요!"
    },
    {
        "title": "번아웃 낮음: 평온한 코알라 🐨",
        "animal": "평온한 코알라",
        "description": "약간의 스트레스는 있지만, 전반적으로 안정적인 상태입니다. 가끔 지치거나 힘든 순간이 있겠지만, 잘 극복하고 계십니다. 꾸준히 자기 관리를 하며 번아웃을 예방하는 것이 중요합니다."
    },
    {
        "title": "번아웃 중간: 고민하는 부엉이 🦉",
        "animal": "고민하는 부엉이",
        "description": "번아웃의 초기 징후가 나타나고 있습니다. 업무에 대한 부담감이나 피로가 쌓여 있을 수 있습니다. 잠시 멈춰 서서 자신의 상태를 돌아보고, 스트레스 해소를 위한 적극적인 노력이 필요합니다."
    },
    {
        "title": "번아웃 높음: 지친 나무늘보 🦥",
        "animal": "지친 나무늘보",
        "description": "상당한 수준의 번아웃을 겪고 계십니다. 업무에 대한 의욕 상실, 감정적 고갈, 신체적 피로가 심할 수 있습니다. 혼자 해결하기보다는 주변의 도움을 요청하거나 전문가의 상담을 고려하는 것이 시급합니다."
    },
    {
        "title": "번아웃 최상: 쓰러진 낙타 🐪",
        "animal": "쓰러진 낙타",
        "description": "매우 심각한 번아웃 상태입니다. 심각한 무기력감, 절망감, 신체적/정신적 고통을 겪고 있을 수 있습니다. 즉시 휴식을 취하고, 반드시 전문가의 도움(의사, 심리 상담사 등)을 받아야 합니다. 당신의 건강이 최우선입니다."
    }
]

# --- 자원 추천 정보 ---
resources = {
    "일반": [
        "**명상 및 마음챙김 앱:** Calm, Headspace 등을 통해 스트레스 완화",
        "**규칙적인 운동:** 걷기, 요가, 가벼운 스트레칭 등으로 신체 활력 증진",
        "**충분한 수면:** 하루 7-8시간의 질 좋은 수면 확보",
        "**균형 잡힌 식단:** 건강한 식습관으로 에너지 유지",
        "**취미 생활:** 업무 외 즐거움을 찾고 몰입할 수 있는 활동",
    ],
    "번아웃 낮음": [
        "**교사 연수 프로그램:** 스트레스 관리, 감정 조절 관련 연수 참여",
        "**동료 교사와의 소통:** 어려움을 공유하고 지지받기",
        "**업무 분담 및 위임:** 혼자 모든 것을 하려 하지 말고 도움 요청",
    ],
    "번아웃 중간": [
        "**심리 상담 센터 이용:** 전문 상담사와의 대화를 통해 문제 해결",
        "**휴식 시간 확보:** 짧은 휴가나 주말을 활용하여 재충전",
        "**업무 우선순위 재설정:** 중요하지 않은 업무는 과감히 줄이기",
    ],
    "번아웃 높음": [
        "**정신건강의학과 방문:** 필요시 약물 치료 및 전문적인 진단",
        "**장기 휴가 고려:** 충분한 휴식을 통해 회복에 집중",
        "**가족 및 친구에게 도움 요청:** 정서적 지지 얻기",
    ],
    "번아웃 최상": [
        "**즉각적인 의료 및 심리 전문가의 도움:** 가장 중요합니다. 혼자 감당하려 하지 마세요.",
        "**업무 중단 및 충분한 휴식:** 회복을 위한 절대적인 시간 확보",
        "**안전한 환경 조성:** 자신을 지지해 줄 수 있는 사람들과 함께하기",
    ]
}

# --- 메인 애플리케이션 로직 ---
st.title("교사 번아웃 자가 진단 웹사이트 🍎")
st.markdown("---")
st.write("""
안녕하세요, 선생님! 👨‍🏫👩‍🏫
이 웹사이트는 선생님의 번아웃 수준을 객관적으로 파악하고,
이에 맞는 맞춤형 자원과 정보를 제공하여 선생님의 건강한 교직 생활을 돕기 위해 만들어졌습니다.
아래 10가지 질문에 솔직하게 답변해 주세요.
""")
st.markdown("---")

# 설문 응답 저장
responses = {}
total_score = 0

# 각 질문에 대한 슬라이더 생성
st.subheader("번아웃 자가 진단 설문 (1점: 전혀 그렇지 않다 ~ 5점: 항상 그렇다)")
for i, question in enumerate(questions):
    st.markdown(f"**{i+1}. {question}**")
    # 슬라이더를 사용하여 1점에서 5점까지 응답 받기
    responses[f"q{i+1}"] = st.slider(
        f"선택해주세요:",
        min_value=1,
        max_value=5,
        value=3, # 기본값
        key=f"slider_{i}"
    )
    total_score += responses[f"q{i+1}"]
    st.markdown("---")

# 결과 보기 버튼
if st.button("내 번아웃 결과 확인하기"):
    st.subheader("진단 결과")

    # 번아웃 레벨 계산 (총점 10점 ~ 50점)
    # 10-18: 레벨 0 (활기찬 돌고래)
    # 19-26: 레벨 1 (평온한 코알라)
    # 27-34: 레벨 2 (고민하는 부엉이)
    # 35-42: 레벨 3 (지친 나무늘보)
    # 43-50: 레벨 4 (쓰러진 낙타)
    
    burnout_level_index = 0
    if total_score >= 43:
        burnout_level_index = 4
    elif total_score >= 35:
        burnout_level_index = 3
    elif total_score >= 27:
        burnout_level_index = 2
    elif total_score >= 19:
        burnout_level_index = 1
    else:
        burnout_level_index = 0

    current_level = burnout_levels[burnout_level_index]

    st.markdown(f"""
    <div class="result-box burnout-level-{burnout_level_index}">
        <div class="result-title">{current_level['title']}</div>
        <div class="result-animal">당신은 마치 '{current_level['animal']}' 같아요!</div>
        <div class="result-description">{current_level['description']}</div>
        <br>
        <p><strong>총 점수: {total_score}점</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("선생님을 위한 맞춤형 자원 추천")

    st.markdown(f"""
    <div class="resource-box">
        <h3>일반적인 번아웃 관리 팁</h3>
        <ul>
            {"".join([f"<li>{item}</li>" for item in resources['일반']])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # 현재 번아웃 레벨에 따른 추가 자원 추천
    if burnout_level_index == 1: # 평온한 코알라
        st.markdown(f"""
        <div class="resource-box">
            <h3>'평온한 코알라'를 위한 추가 팁</h3>
            <ul>
                {"".join([f"<li>{item}</li>" for item in resources['번아웃 낮음']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif burnout_level_index == 2: # 고민하는 부엉이
        st.markdown(f"""
        <div class="resource-box">
            <h3>'고민하는 부엉이'를 위한 추가 팁</h3>
            <ul>
                {"".join([f"<li>{item}</li>" for item in resources['번아웃 중간']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif burnout_level_index == 3: # 지친 나무늘보
        st.markdown(f"""
        <div class="resource-box">
            <h3>'지친 나무늘보'를 위한 추가 팁</h3>
            <ul>
                {"".join([f"<li>{item}</li>" for item in resources['번아웃 높음']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif burnout_level_index == 4: # 쓰러진 낙타
        st.markdown(f"""
        <div class="resource-box">
            <h3>'쓰러진 낙타'를 위한 긴급 지원</h3>
            <ul>
                {"".join([f"<li>{item}</li>" for item in resources['번아웃 최상']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("이 진단은 참고용이며, 정확한 진단은 전문가와 상담하시기 바랍니다.")

