from __future__ import annotations
from langgraph.graph import END, START, StateGraph
from pipeline.nodes.aggregator_node import aggregator_node
from pipeline.agent.discharge_agent import discharge_agent
from pipeline.agent.id_agent import id_agent
from pipeline.agent.itemized_bill_agent import bill_agent
from pipeline.agent.segregator_agent import segregator_agent
from pipeline.state import State

def workflow_graph():
    graph = StateGraph(State)
    
    graph.add_node("segregator", segregator_agent)
    graph.add_node("id_agent", id_agent)
    graph.add_node("discharge_agent", discharge_agent)
    graph.add_node("bill_agent", bill_agent)
    graph.add_node("aggregator", aggregator_node)
    
    graph.add_edge(START, "segregator")
    graph.add_edge("segregator", "id_agent")
    graph.add_edge("segregator", "discharge_agent")
    graph.add_edge("segregator", "bill_agent")
    
    graph.add_edge("id_agent", "aggregator")
    graph.add_edge("discharge_agent", "aggregator")
    graph.add_edge("bill_agent", "aggregator")
    graph.add_edge("aggregator", END)
    
    return graph.compile()

claim_pipeline = workflow_graph()
    