from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import math
import google.generativeai as genai
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()


EMAIL = os.getenv("Official_Email")
API_KEY = os.getenv("Gemini_Api_Key")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


class InputData(BaseModel):
    fibonacci: int = None
    prime: List[int] = None
    lcm: List[int] = None
    hcf: List[int] = None
    AI: str = None

def get_fibonacci(n: int):
    if n < 0:
        raise HTTPException(status_code=422, detail="Invalid fibonacci input")
    
    a = 0
    b = 1

    result = []

    for i in range(n):
        result.append(a)
        a, b = b, a + b

    return result


def get_primes(arr: List[int]):
    result = []

    for num in arr:
        if num < 2:
            continue

        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break

        if is_prime:
            result.append(num)

    return result


def get_lcm(arr: List[int]):
    lcm_val = arr[0]

    for num in arr[1:]:
        lcm_val = abs(lcm_val * num) // math.gcd(lcm_val, num)

    return lcm_val


def get_hcf(arr: List[int]):
    hcf_val = arr[0]

    for num in arr[1:]:
        hcf_val = math.gcd(hcf_val, num)

    return hcf_val

def get_ai_answer(question: str):
    if not question.strip():
        raise HTTPException(status_code=422, detail="Empty AI question")

    prompt = f"""
    Answer the question using ONLY ONE WORD.
    Do not add explanations or punctuation.

    Question: {question}
    """

    response = model.generate_content(prompt)
    return response.text.strip()



@app.post("/bfhl")
def bfhl(data: InputData):
    try:
        payload = data.dict(exclude_none=True)

        if not payload:
            raise HTTPException(status_code=400, detail="No input provided")

        results = {}

        for key, value in payload.items():

            if key == "fibonacci":
                results["fibonacci"] = get_fibonacci(value)

            elif key == "prime":
                results["prime"] = get_primes(value)

            elif key == "lcm":
                results["lcm"] = get_lcm(value)

            elif key == "hcf":
                results["hcf"] = get_hcf(value)

            elif key == "AI":
                results["AI"] = get_ai_answer(value)

            else:
                raise HTTPException(status_code=400, detail=f"Invalid input key: {key}")

        return {
            "is_success": True,
            "official_email": EMAIL,
            "data": results
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.get("/health")
def health():
    return {
        "is_success": True,
        "official_email": EMAIL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

