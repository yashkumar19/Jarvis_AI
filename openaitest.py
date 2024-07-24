import Openai
from config import apikey

Openai.api_key = apikey

def get_openai_response(user_text):
    try:
        response = Openai.ChatCompletion.create(
            model="davinci-002",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_text}
            ],
            prompt="write a email for urgent leave",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response['choices'][0]['message']['content']
        return response_text
    except Exception as e:
        print(f"Failed to get response from OpenAI: {e}")
        return "Sorry, I could not process your request."

if __name__ == '__main__':
    user_prompt = "Write an email to my boss for resignation?"
    response = get_openai_response(user_prompt)
    print(response)
