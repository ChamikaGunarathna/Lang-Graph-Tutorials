from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    number2: int
    operation: str
    finalNumber:int

def adder(state:AgentState) -> AgentState:
    state['finalNumber'] = state['number1']+ state['number2']
    return state

def substractor(state:AgentState) -> AgentState:
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def decide_next_node(state:AgentState) -> AgentState:
    if state['operation'] == "+":
        return "addition"  # edge map
    elif state['operation'] == "-":
        return "substraction"   # edge map
    
if __name__=="__main__":
    graph = StateGraph(AgentState)

    graph.add_node("add",adder)
    graph.add_node("sub",substractor)
    graph.add_node("router", lambda state:state)

    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        decide_next_node,
        {
            #Edge : Node
            "addition":"add",
            "substraction":"sub"
        }
    )

    graph.add_edge("add",END)
    graph.add_edge("sub",END)

    app = graph.compile()

    # # show graph
    # image = app.get_graph().draw_mermaid_png()

    # with open('output.png', 'wb') as f:
    #     f.write(image)

    initial_state_1 = AgentState(
        number1=10,
        number2=7,
        operation="-"
    )
    result = app.invoke(initial_state_1)

    print(result)