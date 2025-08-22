import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("API_KEY"))

# GPT API 호출 예제
response = client.chat.completions.create(
    model="gpt-4o-mini",  # 원하는 모델 지정
    messages=[
        {"role": "system", "content": "You are a supervisor responsible for managing email communications. Your goal is to proactively prevent any issues staff may encounter in emails. For each email provided, respond only with the email content. Review and revise the email's content to ensure there are no inappropriate expressions. After making revisions, briefly validate that the email is appropriate and clear, and proceed or self-correct if validation fails. Respond in the language specified by the prompt."},
        {"role": "user", "content": "제목: 과제 점수 왜 이렇게 주셨어요?\
\
교수님,\
\
안녕하세요. 이번 과제 점수가 너무 낮게 나온 것 같아서 이해가 안 갑니다.\
솔직히 다른 새끼들보다 훨씬 열심히 했는데 점수가 시발 말이 됩니까?\
혹시 채점 실수하신 건 아닌지 확인 부탁드립니다.\
\
그리고 시험도 너무 어렵게 내셔서 학생들 다 힘들어했습니다.\
다음 시험은 좀 쉽게 내주시면 좋겠습니다.\
\
그리고 답장 좀 빨리 주세요."}
    ],
)

print(response.choices[0].message.content)
