from dotenv import load_dotenv
load_dotenv() 

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct") 
parser = StrOutputParser()

code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code generator. Output ONLY the code, no conversational text."),
    ("human", "{topic}")
])

explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who explains code in simple terms"),
    ("human", "Explain the following code in simple words:\n{code}")
])

seq1 = code_prompt | llm | parser

seq2 = RunnableParallel({
    "code": RunnablePassthrough(),
    "explanation": {"code": RunnablePassthrough()} | explain_prompt | llm | parser
})


chain = seq1 | seq2

result = chain.invoke({"topic": "Write a code in java to check if a number is prime or not"})

print("Generated Code:\n", result['code'])
print("\nExplanation:\n", result['explanation'])