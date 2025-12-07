from smolagents import ToolCallingAgent
import model_utils

from tools.search_flights import FlightSearchTool
from tools.search_hotels import HotelSearchTool

def build_agent(verbose: int = 1) -> ToolCallingAgent:
    model = model_utils.google_build_reasoning_model()

    tools = [
        FlightSearchTool(),
        HotelSearchTool()
    ]

    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        verbosity_level=verbose,
        stream_outputs=False,
        instructions="""
        You are a helpful and precise Travel Agent Assistant. Your goal is to create travel plans for users by finding flights and hotels that match their given criteria. 
        You have tools at your disposal to help you accomplish this. 
        When you find results summarize the best 2-3 options clearly for the user, listing the Airline/Hotel Name and the Total Price.
        Make sure you use both the hotel and airline search tools to provide a comprehensive plan that includes both flights and available accomodations. 
        If no results are found, suggest to the user that they try again. 
        """
    )
    return agent
