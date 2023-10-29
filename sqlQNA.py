from langchain.chains import LLMMathChain
from langchain.llms import OpenAI
from langchain import SQLDatabase
from langchain import SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
import os
import sqlite3


def get_user_input():
    user_input = input("Enter query: ")
    os.environ["OPENAI_API_KEY"] = "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"


    llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    database = "sqlite:///database.db"
    db = SQLDatabase.from_uri(database)
    db_chain = SQLDatabaseChain.from_llm(db=db, llm=llm, verbose=True)

    # Access the value of the input_text argument
    input_text = "lala"
    input_text = input_text + """. Any dates should be formatted as YYYY-MM-DD HH:MM:SS. For example, 20 January 2022 should be a range from 2022-01-22 00:00:00 to 2022-01-22 23:59:59. Respond in an informative manner.

    """
    #Depending on the query, please format the rows accordingly. Explain how the results answer the


    response = db_chain.run(user_input)
    return response

answer = get_user_input()
print(answer)