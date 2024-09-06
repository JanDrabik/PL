import os
from datetime import datetime
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import Tool
from langchain.chains import LLMMathChain, LLMChain
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class PlanAndSolveAgent:
    def __init__(self, api_key: str, model: str, temperature: float = 0.2):
        self.api_key = api_key
        self.model_name = model
        self.temperature = temperature
        self.search = DuckDuckGoSearchAPIWrapper()
        if self.model_name == Models.CHATGPT_4_TURBO:
            self.llm = ChatOpenAI(temperature=self.temperature, model=self.model_name, api_key=self.api_key)
        else:
            self.llm = ChatGroq(temperature=self.temperature, model=self.model_name, api_key=self.api_key)
        self.llm_math_chain = LLMMathChain.from_llm(llm=self.llm, verbose=True)

        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()

    def _initialize_tools(self):
        return [
            Tool(
                name="Search",
                func=self.search.run,
                description="useful for when you need to answer questions about current events",
            ),
            Tool(
                name="Calculator",
                func=self.llm_math_chain.run,
                description="useful for when you need to do math",
            ),
        ]

    def _initialize_agent(self):
        planner = load_chat_planner(self.llm)
        executor = load_agent_executor(self.llm, self.tools, verbose=True)
        return PlanAndExecute(planner=planner, executor=executor)

    def invoke(self, input_text):
        return self.agent.invoke({"input": input_text})


def save_string_to_file(content):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"output_{formatted_date}.txt"
    output_path = os.path.join("./outputs", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as file:
        file.write(content)
    print(f"Content saved to {output_path}")


class Models:
    LLAMA3_8B_8192 = "llama3-8b-8192"
    LLAMA3_70B_8192 = "llama3-70b-8192"
    CHATGPT_4_TURBO = 'gpt-4-turbo'


def main():
    groq_key = "groq_key"
    openai_key = "openai_key"
    model_name = Models.CHATGPT_4_TURBO
    agent = PlanAndSolveAgent(api_key=openai_key, model=model_name, temperature=0.2)
    plan_and_solve_result = agent.invoke(
        "How much does it cost on average to rent an apartment in Poland in 2024? List data for 10 biggest cities. "
        "Make sure there is data for each city. Currency should be only in PLN. Compare prices for 1 and 3 bedroom "
        "flats."
    )


    plotter_llm = ChatOpenAI(api_key=openai_key, model_name=model_name, temperature=0.2)
    # plotter_llm = ChatGroq(api_key=openai_key, model_name=model_name, temperature=0.2)
    plotter_prompt = PromptTemplate(
        input_variables=["input_data"],
        template="""
        Transform given data to a format, that can be easily plotted, such as a pandas DataFrame.
        Do not provide any comments, summary or any unnecessary text. Your output should be code only.

        Data:
        {input_data}
        """
    )

    plotter_chain = plotter_prompt | plotter_llm | StrOutputParser()
    plotter_result = plotter_chain.invoke({"input_data": plan_and_solve_result["output"]})

    save_string_to_file(f'{plan_and_solve_result["output"]}\n\n{plotter_result}')


if __name__ == '__main__':
    main()
