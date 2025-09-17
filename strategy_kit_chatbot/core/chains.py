from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from strategy_kit_chatbot.core.prompts import chat_bot_prompt
from pydantic import BaseModel

load_dotenv()
llm = ChatOpenAI(model="gpt-4.1")


class ChatBotResponse(BaseModel):
    chatbot_response: str


async def chatbot_reply_chain(junk_data, ai_data, query, chat_history=[]):
    llmr = llm.with_structured_output(ChatBotResponse)
    input_data = {"junk_data": junk_data, "ai_data": ai_data, "query": query}
    chatbot_chain = chat_bot_prompt | llmr
    response = await chatbot_chain.ainvoke(input_data)
    return response.chatbot_response
