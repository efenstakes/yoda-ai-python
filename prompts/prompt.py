import os
from fastapi import APIRouter
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import MongoDBChatMessageHistory, ConversationSummaryBufferMemory, ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from typing import List, Dict, Any
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient, errors

router = APIRouter()


# connect to mongo
client = MongoClient(os.getenv("MongoURI"))

# check the loaded env vars
all_values = dotenv_values(".env")
print(all_values)


llm = OpenAI(streaming=False, temperature=0.5)


@router.post("/prompt")
def prompt(prompt: str, session: str):
    message_history = MongoDBChatMessageHistory(
        connection_string=os.getenv("MongoURI"),
        session_id=session
    )

    memories = ConversationBufferMemory(k=3)

    if len(message_history.messages):
        memories.save_context(
            { "input": message_history.messages[0].content },
            { "output": message_history.messages[1].content },
        )
        conversation = ConversationChain(
            llm=llm,
            verbose=True,
            memory=memories
        )

        prompt_reply = conversation.predict(input=prompt)
        message_history.add_user_message(prompt)
        message_history.add_ai_message(prompt_reply)

        return {
            "reply": prompt_reply,
            "prompt": prompt,
            "memories": memories
        }
    
    else:
        conversation = ConversationChain(
            llm=llm,
            verbose=True,
            memory=memories
        )

        prompt_reply = conversation.predict(input=prompt)
        message_history.add_user_message(prompt)
        message_history.add_ai_message(prompt_reply)

        return {
            "reply": prompt_reply,
            "prompt": prompt,
            "memories": memories
        }


