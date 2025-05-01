# test_openai_api.py
import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


def test_openai_api():
    client = OpenAI(
        api_key="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"
    )

    messages: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": "Diga olá em português"}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=messages,
    )
    print("✅ OpenAI API funcionou:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    test_openai_api()
