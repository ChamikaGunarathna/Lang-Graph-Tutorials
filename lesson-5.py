from langgraph.graph import StateGraph, START, END
import random
from typing import Dict, TypedDict, List


class AgentState(TypedDict):
    name:str
    number: List[int]
    counter:int

def greeting_node(state:AgentState) -> AgentState:
    state['name'] = f"Hi there, {state['name']}"
    state['counter'] = 0
    return state

def random_node(state:AgentState)->AgentState:
    state['number'].append(random.randint(0,10))
    state['counter'] += 1
    return state

def should_continue(state:AgentState)->AgentState:
    if state['counter'] < 5:
        print(f"Entering loop. Count : {state['counter']}")
        return "loop"
    else:
        return "exit"


if __name__=='__main__':
    graph = StateGraph(AgentState)

    graph.add_node("greeting",greeting_node)
    graph.add_node("random", random_node)
    
    graph.add_edge(START,"greeting")
    graph.add_edge("greeting", "random")
    graph.add_conditional_edges(
        "random",
        should_continue,
        {
            "loop": "random",
            "exit": END
        }
    )

    app = graph.compile()

    # # show graph
    # image = app.get_graph().draw_mermaid_png()

    # with open('output.png', 'wb') as f:
    #     f.write(image)

    result = app.invoke(
        {
            'name':'Bob',
            'number':[],
            'counter':-1
        }
    )

    print(result)
