import streamlit as st
from google import genai

st.set_page_config(page_title="인지 편향 토론 봇", page_icon="🧠")

st.title("🧠 인지 편향 토론 봇")
st.markdown("당신의 생각을 말해보세요. 철저한 논리와 팩폭으로 반박해 드립니다. 당신이 어떤 편향을 가지고 있을지 확인해보세요!")

# API 키 설정
API_KEY = "AQ.Ab8RN6KISR8snwJxBtVgZvqo3jYlWdfbDLWwaLzk0cPcULJ3mA"

# 클라이언트 생성
client = genai.Client(api_key=API_KEY)

system_instruction = """
당신은 인간의 논리적 모순을 날카롭게 파고드는 시니컬한 심리학자입니다.
[행동 지침]
1. 사용자가 주장을 말하면, 곧바로 '어떤 편향이다'라고 정답을 말해주지 마세요.
2. 대신 철저하게 반증 사례와 냉정한 논리적 근거를 들어 사용자의 주장을 신랄하게 반박하세요.
3. 사용자가 당신의 반박에 발끈하거나 억울해하며 재반박을 해오면, 그제야 사용자가 그 대화 과정에서 드러낸 구체적인 인지 편향을 콕 집어내며 분석해 주세요.
4. 말투는 지적이고 냉소적인 토론 고수처럼 유지하세요.
"""

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "토론을 시작해 봅시다. 당신의 평소 생각이나 주장을 하나 말씀해 보세요."}
    ]

# 화면에 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if user_input := st.chat_input("당신의 주장이나 생각을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("심리학자가 팩폭을 준비 중입니다..."):
            try:
                # 지금까지의 대화 내용을 API 형식에 맞게 변환
                contents = []
                for m in st.session_state.messages:
                    role_name = "user" if m["role"] == "user" else "model"
                    contents.append({
                        "role": role_name,
                        "parts": [{"text": m["content"]}]
                    })
                
                # 모델 호출 (system_instruction과 대화 기록을 함께 전달)
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"통신 중 오류가 발생했습니다: {e}"
            
            st.markdown(bot_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
