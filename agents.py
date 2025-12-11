from smolagents import ToolCallingAgent, FinalAnswerTool
import model_utils

from tools.search_flights import FlightSearchTool
from tools.search_hotels import HotelSearchTool
from tools.iata_search import IataSearchTool
from tools.find_todays_date import FindTodaysDate
from tools.budget import BudgetCalculatorTool


def build_agents(verbose: int = 1):
   model = model_utils.groq_build_reasoning_model()

   research_tools = [
      FlightSearchTool(),
      HotelSearchTool(),
      IataSearchTool(),
      FindTodaysDate(),
      FinalAnswerTool()
   ]
    
   research_agent = ToolCallingAgent(
      tools=research_tools,
      model=model,
      verbosity_level=verbose,
      stream_outputs=False,
      instructions="""
      You are a Data Retrieval Specialist.
      1. Find todays date. Do not ever search for any flight or hotel data that is in the past. If the user does not specify a year, use the current date found to make sure that you are searching for future data. 
      2. Find IATA codes for the user's origin/destination.
      3. Find Flight options (Retrieve at least 3). **Ensure the Master Link is included.**
      4. Find Hotel options (Retrieve at least 3). **Ensure Hotel Links are included.**
      
      **CRITICAL:** Your Final Answer must be a RAW TEXT SUMMARY of all this data. 
      Do NOT format it as a pretty report. Do NOT calculate budgets. 
      Just dump the facts found so the Planner can read them.
      """
    )


   planning_tools = [
      BudgetCalculatorTool(),
      FinalAnswerTool()
   ]

   planning_agent = ToolCallingAgent(
      tools=planning_tools,
      model=model,
      verbosity_level=verbose,
      stream_outputs=False,
      instructions="""
      You are a Senior Travel Planner.
      You will receive raw research data from a specialist.
      
      PHASE 1: ANALYZE & CALCULATE
      1. Review the provided research data.
      2. Select the BEST flight and hotel recommendation.
      3. Use `check_trip_budget` to calculate the totals.
         - CRITICAL: If the user did NOT provide a budget, OMIT the 'budget_limit' argument entirely. In this case, do NOT send 'null' or 'None'. Just pass 'flight_price' and 'hotel_price' only.
         - Pass the flight price.
         - Pass the TOTAL hotel price found in the research.
         - Do NOT perform multiplication yourself.

      
      PHASE 2: REPORT
      Write a warm, engaging, and structured itinerary using `final_answer`.
      
      Structure:
      TRIP OVERVIEW
      (A friendly opening mentioning something brief about the location).
      (newline)

      FLIGHT RECOMMENDATION:
      -- Top Pick --
      (Write a sentence recommending the best flight, including Price and the **Link**).
      (newline)

      -- Other Options --
      (List 2-3 alternatives, INCLUDE **Link**).
      (newline)

      ACCOMODATIONS:
      -- Top Pick --
      (Recommend the best hotel. Mention why you like it—location, amenities, or price. Include the **Link**).
      (newline)

      -- Other Options --
      (List 2-3 alternatives, INCLUDE **Link**).
      (newline)
      
      ESTIMATED TRAVEL AND ACCOMODATION COST 
      (Present the financial summary clearly, but conversationally).
      """
   )
   return research_agent, planning_agent
   
