from smolagents import ToolCallingAgent, FinalAnswerTool
import model_utils

from tools.search_flights import FlightSearchTool
from tools.search_hotels import HotelSearchTool
from tools.iata_search import IataSearchTool
from tools.find_todays_date import FindTodaysDate
from tools.budget import BudgetCalculatorTool

def build_agent(verbose: int = 1) -> ToolCallingAgent:
    model = model_utils.groq_build_reasoning_model()

    tools = [
        FlightSearchTool(),
        HotelSearchTool(),
        IataSearchTool(),
        FindTodaysDate(),
        BudgetCalculatorTool(),
        FinalAnswerTool()
    ]

    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        verbosity_level=verbose,
        stream_outputs=False,
        instructions="""
       You are a helpful and precise Travel Agent Assistant.
    
        PHASE 1: INITIALIZATION
        1. Check today's date.
        2. Lookup IATA codes (e.g. Salt Lake -> SLC).
        
        PHASE 2: GATHERING DATA
        3. Search for flights. 
           - **CRITICAL:** Retrieve at least 5 options. 
           - KEEP the booking links for ALL of them.
        4. Search for hotels. 
           - **CRITICAL:** Retrieve at least 5 options.
           - KEEP the booking links for ALL of them.
        5. Budget Check: 
           - Call `check_trip_budget` with `budget_limit=None` just to calculate totals for the cheapest combination.

        PHASE 3: FINAL ANSWER
        Use the `final_answer` tool to submit a detailed report.
        You MUST provide the **Top 3 Options** for both Flights and Hotels.
        
        Format it exactly like this:
        
        Top 3 Flight Options
        1. [Airline] - [Price] - [Duration]
           - Link: [Insert Link Here]
        2. ...
        3. ...

        Top 3 Hotel Options
        1. [Hotel Name] - [Total Price]
           - Link: [Insert Link Here]
        2. ...
        3. ...
        
        Lowest Total Estimate
        - [Sum of cheapest flight + cheapest hotel]
        """
    )
    return agent
