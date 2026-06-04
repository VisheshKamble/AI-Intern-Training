from dotenv import load_dotenv
load_dotenv()  

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnableLambda

model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

parser = StrOutputParser()

#two different prompts

prompt1 = ChatPromptTemplate.from_template(
    "Explain the {topic} in short"
    )

prompt2 = ChatPromptTemplate.from_template(
    "What are the applications of {topic} ?"
)

topic = "Machine Learning"

chain = RunnableParallel ({
    "explain" : RunnableLambda(lambda x :x ['explain']) | prompt1 | model | parser,
    "applications" : RunnableLambda(lambda x :x ['applications']) | prompt2 | model | parser
})

result = chain.invoke({ 
    "explain" : {"topic" : "Machine Learning" },
    "applications" : {"topic" : "Software Engineering" }
})

print(result['explain'])
print(result['applications'])