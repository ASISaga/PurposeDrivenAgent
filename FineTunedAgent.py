# Create an AutoGen Agent using a domain-specific fine-tuned language model.
# Dependencies:
# - transformers: for loading the tokenizer and model
# - autogen_core: for base model client and user message handling
# - autogen_agentchat: for base chat agent and text message handling
# - autogen_ext: for OpenAI chat completion client

from transformers import AutoTokenizer, AutoModelForCausalLM
from autogen_core.models import BaseModelClient, UserMessage
from autogen_core.agents import BaseAgent

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

class CustomModelClient(BaseModelClient):
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)

    async def generate(self, prompt, max_length=50):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = await asyncio.to_thread(self.model.generate, inputs['input_ids'], max_length=max_length)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Load your fine-tuned model
model_path = "./final_model"
custom_model_client = CustomModelClient(model_path)

# Example usage
prompt = "Your domain-specific prompt goes here..."
response = custom_model_client.generate(prompt)
print(response)

# Integrate your custom model client with AutoGen 0.4

class CustomAgent(BaseAgent):
    def __init__(self, model_client):
        self._model_client = model_client

    async def handle_message(self, message: UserMessage):
        response = await self.model_client.generate(message.content)
        return response

# Create an instance of your custom agent
custom_agent = CustomAgent(custom_model_client)

# Example usage
import asyncio

async def main():
    user_message = UserMessage(content="Your domain-specific prompt goes here...", source="user")
    response = await custom_agent.handle_message(user_message)
    print(response)

asyncio.run(main())
