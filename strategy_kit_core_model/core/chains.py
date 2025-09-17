from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from strategy_kit_core_model.core.prompts import level_two_prompt

load_dotenv()
llm = ChatOpenAI(model="gpt-4.1", temperature=0, use_responses_api=True)


class Level2Summary(BaseModel):
    summary: str


async def return_level_two_summary(transcript):
    llmr = llm.with_structured_output(Level2Summary)
    chain = level_two_prompt | llmr
    input_data = {"report_detailed_summary": transcript}
    response = await chain.ainvoke(input=input_data)
    return response.summary
