import os
from langchain.chains import LLMMathChain
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

def get_user_input():
    user_input = input("Enter query: ")

    os.environ["OPENAI_API_KEY"] = "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"


    llm = OpenAI(temperature=0.1, openai_api_key=os.getenv("OPENAI_API_KEY"))

    def greeting_tool(input: str) -> str:
        greetings = ["hi", "hello", "good morning", "good afternoon"]
        if input.lower() in greetings:
            return "Hello there!"
        else:
            return "I don't understand your greeting."
        
    def explanation_tool(input: str) -> str:
        query = ["who are you", "what are you", "what do you do", "what is your use"]
        if input.lower() in query:
            return "I am ChatVM, your assistant in understanding the large volume of surveillance and customer traffic data! Feel free to ask queries on what has happened within your establishment."
        else:
            return "I am ChatVM, your assistant in understanding the large volume of surveillance and customer traffic data! Feel free to ask queries on what has happened within your establishment."

    llm_math_chain = LLMMathChain.from_llm(llm=llm)

    database = "sqlite:///database.db"
    db = SQLDatabase.from_uri(database)
    db_chain = SQLDatabaseChain.from_llm(db=db, llm=llm)


    tools = [
        Tool(
            name="Greeting", 
            func=greeting_tool,
            description="Responds to common greetings",
        ),
        Tool(
            name="Introduction", 
            func=explanation_tool,
            description="Responds to queries on the agent's usage",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        ),
        Tool(
            name="SQLQuery",
            func=db_chain.run,
            description="""useful for when you need to answer questions about traffic in a certain area that is under surveillance. 
            Input should be in the form of a question containing full context. The values in person_id indicates a unique person. 
            The person_id may appear more than once, in a different x_pos and y_pos to show their coordinates. 
            Counting the person_id column would mean to count the number of appearances of people, NOT the number of unique people. 
            The area that is under surveillance can be partitioned into different sectors, as specified in the sections column. 
            Any dates should be formatted as YYYY-MM-DD HH:MM:SS. For example, 20 January 22 should be a range from 2022-01-22 00:00:00 to 2022-01-22 23:59:59. 
            When responding to questions on how many people/person, format your response with 'appearance of people/person' rather than just 'people/person|'.
            """,
        ),
    ]

    chatVM = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    response = chatVM.run(user_input)

    return response

answer = get_user_input()
print(answer)