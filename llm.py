from openai import OpenAI
import os
from dotenv import load_dotenv

from audio_functions import get_audio

class Assistant():
    def __init__(
        self,
        system_prompt="You are a personal assistant named Ariana that plans the day, manages appointments, and helps with diet and productivity goals. Respond very briefly, under 30 words.",
        model="gpt-4-1106-preview"
    ) -> None:
        
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model 
        
        self.conversation = []
        self.system_prompt = system_prompt
        self.conversation.append({"role": "system", "content": self.system_prompt})
    
    def get_completion(self, prompt):
        self.conversation.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
                model=self.model,
                max_tokens = 256,
                messages=self.conversation
        )

        completion = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": completion})

        print(completion)
        return completion 

if __name__ == '__main__':
    ariana = Assistant()
    user_prompt = input("Start a conversation with Ariana. \n")

    while True:
        response = ariana.get_completion(user_prompt)
        print(response)
        
        user_prompt = input()  # Continues the conversation without the repeated start prompt
        if user_prompt.lower() == 'quit':
            break 