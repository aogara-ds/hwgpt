from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")

def load_search_agent():
    llm = OpenAI(temperature=0)
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search"
        )
    ]

    search_agent = initialize_agent(tools, llm, agent="self-ask-with-search", verbose=True)

    return search_agent

def answer_questions(infile, outfile, search_agent):
    search_agent = load_search_agent()

    # Read questions from infile
    read_questions = open(infile, "r")
    questions = read_questions.read().split("\n")

    for q in questions:
        output = search_agent.run(q)
        print(output)

        # Write output to outfile
        with open(outfile, "a") as f:
            f.write("Question: " + question + "\n" + "Answer: " + output + "\n\n")

def fix_file():
    read_questions = open("geol/exam2qs.txt", "r")
    questions = read_questions.read().split("\n")
    read_answers = open("geol/studyguide.txt", "r")
    answers = read_answers.read().split("\n")

    for q, a in zip(questions, answers):
        with open("studyguide.txt", "a") as f:
            f.write("Question: " + q + "\n" + "Answer: " + a + "\n\n")

if __name__=="__main__":
    # search_agent = load_search_agent()
    # answer_questions("questions.txt", "answers.txt", search_agent)
    fix_file()
