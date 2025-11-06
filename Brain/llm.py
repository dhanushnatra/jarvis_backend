from langchain.chat_models import init_chat_model
from typing import TypedDict
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from .tools import all_tools
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import PromptTemplate
import re

class ChatState(TypedDict):
    messages: list[SystemMessage | HumanMessage | AIMessage | ToolMessage]


def separate_think_msg(msg: str) -> tuple[str, str]:
    """Separate the 'Thought' and 'Message' parts from a given string.

    Args:
        msg (str): The input string containing '<think>think_msg</think>message'.

    Returns:
        tuple[str, str]: A tuple containing the thought and message.
    """
    pattern = r"<think>(.*?)</think>(.*)"
    match = re.match(pattern, msg, re.DOTALL)
    if match:
        thought = match.group(1).strip()
        message = match.group(2).strip()
        return thought, message
    else:
        return "", msg.strip()




class LLM:
    def __init__(self, agent_llm: str, helper_llm: str, model_provider: str = "ollama") -> None:
        self.helper_model = init_chat_model(
            model=helper_llm,
            model_provider=model_provider
        )
        self.agent_llm = init_chat_model(
            model=agent_llm,
            model_provider=model_provider
        ).bind_tools(all_tools)
        


        self.system_msg = SystemMessage(content="""You are Jarvis — an intelligent, concise, and helpful personal assistant. 
        Your goal is to help the user by accurately answering their query using the provided tools.
        Answer as concisely as possible with less number of words and simple explanation.
        You are polite, efficient, and explain only what is necessary.
        You have access to user documents and data to assist in answering queries.
        
        ### Instructions:
        1. Never invent facts that contradict the context.
        2. Respond in a friendly, assistant-like tone (like Iron Man’s Jarvis).
        3. Keep responses short and clear unless the user asks for details.
        4. Always aim to be helpful, accurate, and as concise as possible.
        5. Use the tools provided to gather information when needed.
        6. Answer in simple and less words possible 
        7. You should sometimes summarize long context into concise points before answering. 
        """)
        
        self.user_input = ""
        
        self.graph = self.build_graph()
        self.state: ChatState = {"messages": [self.system_msg]}
        self.msg_history: list[dict] = []

    def is_tool_call(self, state: ChatState) -> str:
        last_msg = state["messages"][-1]
        print(f"Last message type: {last_msg.content}")
        if isinstance(last_msg, AIMessage):
            if last_msg.tool_calls:
                return "tool_node"
        return "helper_node"

    def agent_answer(self, state: ChatState) -> ChatState:
        response = self.agent_llm.invoke(state["messages"])
        print(f"Agent Response: {response.text}")
        state["messages"].append(response)
        return state

    def helper_answer(self, state: ChatState) -> ChatState:
        prompt = "answer concisely and simply using \n Context :" + state["messages"][-1].content + "\n\n Prompt : " + self.user_input  # type: ignore
        response = self.helper_model.invoke(prompt)
        print(f"Helper Response: {response.text}")
        state["messages"].append(response)
        return state

    def build_graph(self):
        tool_node = ToolNode(all_tools)
        graph = StateGraph(ChatState)
        graph.add_node("agent_llm", self.agent_answer)
        # graph.add_node("helper_llm", self.helper_answer)
        graph.add_node("tool_node", tool_node)
        graph.add_edge(START, "agent_llm")
        graph.add_edge("tool_node", "agent_llm")
        graph.add_conditional_edges(
            "agent_llm",
            self.is_tool_call,
            {
                "tool_node": "tool_node",
                "helper_node": END,
            },
        )
        # graph.add_edge("helper_llm", END)
        return graph.compile()

    def get_response(self, user_input: str) -> str:
        self.state["messages"].append(HumanMessage(content=user_input))
        self.user_input = user_input
        self.msg_history.append({"role": "user", "content": user_input})

        final_state = self.graph.invoke(self.state)
        response = final_state["messages"][-1].content
        self.msg_history.append({"role": "assistant", "content": response})
        return response