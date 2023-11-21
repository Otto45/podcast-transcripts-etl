from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from cli_chat_prompts import main as main_prompt
from databases.vector import get_vector_store

vector_store = get_vector_store()
retriever = vector_store.as_retriever()

model = ChatOpenAI(model='gpt-4-1106-preview')

chain = (
    {"transcripts": retriever, "question": RunnablePassthrough()}
    | main_prompt
    | model
    | StrOutputParser()
)

user_prompt = input("Question: ")

response = chain.invoke(user_prompt)

print(response)
