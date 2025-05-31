import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI  

load_dotenv()

llm = ChatOpenAI(
    model="mistralai/mixtral-8x7b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    temperature=0.7,
    max_tokens=700
)

prompt_template = PromptTemplate(
    input_variables=["text"],
    template="{text}"
)

llm_chain = LLMChain(prompt=prompt_template, llm=llm)

def ask_llm(prompt):
    result = llm_chain.invoke({"text": prompt})
    return result["text"]
