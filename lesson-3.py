from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state:AgentState) -> AgentState:

    state['final'] = f"Hi {state['name']}!"
    return state

def second_node(state:AgentState)-> AgentState:
    state["final"] = f"{state['final']}\nYou are {state["age"]} years old!"
    return state

if __name__=="__main__":
    graph = StateGraph(AgentState)

    graph.add_node("first",first_node)
    graph.add_node("second",second_node)

    graph.set_entry_point("first")
    graph.add_edge("first","second")
    graph.set_finish_point("second")

    app = graph.compile()

    # show graph
    image = app.get_graph().draw_mermaid_png()

    with open('output.png', 'wb') as f:
        f.write(image)

    result = app.invoke(
        {
            "name": "Chris",
            "age": 30
        }
    )

    print(result)