import os
import uvicorn
from fastapi import FastAPI
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import MongoDBChatMessageHistory, ConversationSummaryBufferMemory, ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from typing import List, Dict, Any
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient, errors

# load env vars
load_dotenv()

# load it after getting environment vars
from prompts.prompt import router


# create server instance
app = FastAPI(desc="Yoda AI")

# include the prompts routes
app.include_router(router)

# to start the server Programmatically
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
