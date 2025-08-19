from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    number2: int
    number3: int
    operation1: str
    operation2: str
    finalNumber:int
    finalNumber2:int

def adder1(state:AgentState) -> AgentState:
    state['finalNumber'] = state['number1']+ state['number2']
    return state

def substractor1(state:AgentState) -> AgentState:
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def adder2(state:AgentState) -> AgentState:
    state['finalNumber2'] = state['finalNumber']+ state['number3']
    return state

def substractor2(state:AgentState) -> AgentState:
    state['finalNumber2'] = state['finalNumber'] - state['number3']
    return state


def decide_next_node1(state:AgentState) -> AgentState:
    if state['operation1'] == "+":
        return "addition"  # edge map
    elif state['operation1'] == "-":
        return "substraction"   # edge map
    
def decide_next_node2(state:AgentState) -> AgentState:
    if state['operation2'] == "+":
        return "addition"  # edge map
    elif state['operation2'] == "-":
        return "substraction"   # edge map
    
if __name__=="__main__":
    graph = StateGraph(AgentState)

    graph.add_node("add1",adder1)
    graph.add_node("sub1",substractor1)
    graph.add_node("router1", lambda state:state)

    graph.add_node("add2",adder2)
    graph.add_node("sub2",substractor2)
    graph.add_node("router2", lambda state:state)

    graph.add_edge(START, "router1")
    graph.add_conditional_edges(
        "router1",
        decide_next_node1,
        {
            #Edge : Node
            "addition":"add1",
            "substraction":"sub1"
        }
    )
    graph.add_edge("add1","router2")
    graph.add_edge("sub1","router2")

    graph.add_conditional_edges(
        "router2",
        decide_next_node2,
        {
            #Edge : Node
            "addition":"add2",
            "substraction":"sub2"
        }
    )
    graph.add_edge("add2", END)
    graph.add_edge("sub2", END)

    app = graph.compile()

    # # show graph
    # image = app.get_graph().draw_mermaid_png()

    # with open('output.png', 'wb') as f:
    #     f.write(image)

    initial_state_1 = AgentState(
        number1=10,
        number2=7,
        number3=8,
        operation1="-",
        operation2="+"
    )
    result = app.invoke(initial_state_1)

    print(result)