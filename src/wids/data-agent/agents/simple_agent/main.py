from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Literal, Any


# Define the agent state simply
class SimpleAgentState(TypedDict):
    question: str
    research_plan: str
    findings: List[str]
    summary: str
    next_step: Literal["plan", "research", "summarize", "end"]


def create_plan(state: SimpleAgentState, plan_chain: Any) -> SimpleAgentState:
    research_plan = plan_chain.invoke({"question": state["question"]})
    return {**state, "research_plan": research_plan.content, "next_step": "research"}


def conduct_research(state: SimpleAgentState, research_chain: Any) -> SimpleAgentState:
    findings = research_chain.invoke(
        {"question": state["question"], "research_plan": state["research_plan"]}
    )
    return {
        **state,
        "findings": state.get("findings", []) + [findings.content],
        "next_step": "summarize",
    }


def create_summary(state: SimpleAgentState, summary_chain: Any) -> SimpleAgentState:
    summary = summary_chain.invoke(
        {"question": state["question"], "findings": "\n".join(state["findings"])}
    )
    return {**state, "summary": summary.content, "next_step": "end"}


def main():
    # Initialize the model
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # Create the prompt template
    planner_prompt = ChatPromptTemplate.from_template(
        """
You are a research assistant. Given a question, create a brief research plan.
Question: {question}
Research Plan:
"""
    )
    plan_chain = planner_prompt | llm

    resarch_prompt = ChatPromptTemplate.from_template(
        """
You are a research assistant. Given a question and research plan, 
conduct research and provide your findings.
Question: {question}
Research Plan: {research_plan}
Findings:
"""
    )
    research_chain = resarch_prompt | llm

    summarize_prompt = ChatPromptTemplate.from_template(
        (
            """You are a research assistant. Summarize the following findings into a 
comprehensive answer to the original question.
Question: {question}
Findings: {findings}
Summary:"""
        )
    )
    summarize_chain = summarize_prompt | llm

    # Define the graph
    graph = StateGraph(SimpleAgentState)
