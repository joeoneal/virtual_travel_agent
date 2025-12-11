from smolagents import Tool
from tools.serp_client import SerpApiClient
import time

class FlightSearchTool(Tool):
    name = "search_flights"

    description = (
        "Searches for real-time flight options using Google Flights data. "
        "Returns a list of flight options with airlines, prices, and duration. "
        "If you want a round trip, you MUST provide a return_date."
    )
    inputs = {
        "origin": {
            "type": "string",
            "description": "3-letter IATA code for departure (example: 'SLC')."
        },
        "destination": {
            "type": "string",
            "description": "3-letter IATA code for arrival (example 'DEN')."
        },
        "departure_date": {
            "type": "string",
            "description": "Date in 'YYYY-MM-DD' format."
        },
        "return_date": {
            "type": "string",
            "description": "Date in 'YYYY-MM-DD' format. Optional. If omitted, searches one-way.",
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.client = SerpApiClient()

    def forward(self, origin: str, destination: str, departure_date: str, return_date: str = None) -> str:
        print('sleeping')
        time.sleep(0.5)
        print('done sleeping')

        flight_type = "2"
        
        if return_date:
            flight_type = "1"

        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": departure_date,
            "return_date": return_date, 
            "type": flight_type,        
            "currency": "USD",
            "hl": "en",
        }

        print(f"Searching SerpApi for {origin} -> {destination} ({'Round Trip' if return_date else 'One Way'})...")
        
        results = self.client.search(params)
        
        if "error" in results:
            error_msg = results["error"]
            print(f"SERPAPI ERROR: {error_msg}")
            return f"API Error: {error_msg}"
        
        link = results.get('search_metadata', {}).get("google_flights_url", "No link available")

        if "best_flights" not in results:
            return f"No flights found. \nYou are welcome to search for flights here: {link}"
        
        flights = []

        best_flights = results.get("best_flights", [])
        
        for flight in best_flights[:5]:
            price = flight.get("price", "N/A")
            airline = "Unknown Airline"
            if "flights" in flight and len(flight["flights"]) > 0:
                airline = flight["flights"][0].get("airline", "Unknown")
            
            flights.append(f"Flight: {airline}, Price: {price}, Link: {link}")

        return "\n".join(flights) + f'\n\nBooking Link: {link}'