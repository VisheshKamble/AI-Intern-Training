from dotenv import load_dotenv
load_dotenv()  

from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#Prompt template

prompt = ChatPromptTemplate.from_template(
  "Explain the {topic} in brief"
)

#model

model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

#output parser

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"topic": "Machie Learning"})

print(result)