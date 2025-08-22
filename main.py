import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

# .env 로드
load_dotenv()

# OpenAI 클라이언트 초기화 (환경변수 OPENAI_API_KEY 사용 권장)
client = OpenAI(api_key=os.getenv("API_KEY"))

# 입력 JSON (파이썬 dict)
temp = {
    "language": "Korean",
    "title": "과제 점수 왜 이따구냐?",
    "mail": "교수님, 안녕하세요. 이번 과제 점수가 너무 낮게 나온 것 같아서 이해가 안 갑니다. 솔직히 다른 새끼들보다 훨씬 열심히 했는데 점수가 시발 말이 됩니까? 혹시 채점 실수하신 건 아닌지 확인 부탁드립니다. 그리고 시험도 너무 어렵게 내셔서 학생들 다 힘들어했습니다. 다음 시험은 좀 쉽게 내주시면 좋겠습니다. 그리고 답장 좀 빨리 주세요.",
    "guide": "친근하게"
}

# Pydantic 출력 스키마
class ai_result(BaseModel):
    title: str
    mail: str

# --- 핵심 변경: JSON을 진짜 JSON으로 전달 ---
# 1) user content에 JSON 문자열을 그대로 넣음 (ensure_ascii=False로 한글 보존)
# 2) system 프롬프트는 role만 사용 (불필요한 "System:" 접두어 제거)

system_prompt = (
    "You are a supervisor responsible for managing email communications. "
    "Your goal is to proactively prevent any issues staff may encounter in emails. "
    "Your response should be a structured output: revise and improve both the 'title' and 'mail' fields "
    "in your structured output based on the input's title and mail content. "
    "If there is a guide provided in the input, reflect any guidance for revising both the title and the mail based on the guide. "
    "Modify the output language according to the input's specified language. "
    "Review and revise both the email's title and content to ensure there are no inappropriate expressions. "
    "After making revisions, briefly validate that both the email title and content are appropriate and clear, "
    "and proceed or self-correct if validation fails. Respond in the language specified by the input."
)

# 모델은 최신 SDK 예시와 호환되는 gpt-4o 계열 권장
# 참고: SDK README의 Responses API 예시들 (responses.create, input 사용법) :contentReference[oaicite:3]{index=3}
response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
        {"role": "system", "content": system_prompt},
        # JSON을 유효한 형태(쌍따옴표)로 직렬화해서 전달
        {"role": "user", "content": json.dumps(temp, ensure_ascii=False)}
    ],
    text_format=ai_result,
)

print(f"기존 메일 제목: {temp['title']}")
print(f"기존 메일 내용: {temp['mail']}")

try:
    res = response.output_parsed  # Pydantic으로 검증 완료된 객체
    print(f"수정된 메일 제목: {res.title}")
    print(f"수정된 메일 내용: {res.mail}")
except ValidationError as e:
    # 만약 모델이 스키마를 못 맞추면 에러 확인
    print("구조화 출력 검증 실패(Pydantic):", e)
