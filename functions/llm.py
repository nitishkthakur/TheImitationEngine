import ollama
from ollama import chat
from ollama import ChatResponse


class LLM:
    def __init__(self, system_instructions = ""):
        self.system_instructions = system_instructions
        self.messages = []
        self.messages.append({'role': 'system', 'content': self.system_instructions})
        
    def set_system_instructions(self, system_instructions):
        self.system_instructions = system_instructions
        # Update the system instructions in the message stream
        self.messages[0]['content'] = self.system_instructions
        
    def load_llm(self):
        print("Entering Chat Function")
        response_null = chat(
            model="llama3.2:1b",
            messages=[],         # empty list ⇒ just load, no generation
            keep_alive=-1        # keep loaded indefinitely
        )
        print(response_null)
        print("model loaded")

    def chat(self, user_prompt):
        # Update messages
        self.messages.append({'role': 'user', 'content': user_prompt})
        
        # Get back response
        response = chat(model='llama3.2:1b', messages=self.messages, keep_alive = -1)
        
        # Add back the response to the message stream
        self.messages.append({'role': 'assistant', 'content': response['message']['content']})
        return response['message']['content']

                        