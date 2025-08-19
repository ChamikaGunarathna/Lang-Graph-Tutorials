# for graph
from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict): # state schema
    message :  str

def greeting_node(state: AgentState)->AgentState:
    '''Simple node that adds a greeting message to the state'''

    state['message'] = "Hey " + state["message"] + ", how is your day going?"

    return state


if __name__=='__main__':
    print("=============LangGraph Lesson 1==================")

    graph = StateGraph(AgentState)

    graph.add_node("greeter", greeting_node)

    graph.set_entry_point("greeter")
    graph.set_finish_point("greeter")

    app = graph.compile()

    # # show graph
    # image = app.get_graph().draw_mermaid_png()

    # with open('output.png', 'wb') as f:
    #     f.write(image)

    result = app.invoke({"message":"bob"})

    print(result["message"])