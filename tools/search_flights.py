from smolagents import Tool
from tools.amadeus_client import AmadeusClient
import time

class SearchFlightsTool(Tool):
    name = "search_flights"

    description= "Searchs for available flights using Amadeus API. Returns a list of available flights with both prices and airline codes."

    inputs= {
        "origin":{
            "type": "string",
            "description": "3-letter IATA code for the flight departure city."
        },
        
        "destination": {
            "type": "string",
            "description": "3-letter IATA code for the flight arrival city."
        },

        "departure_date": {
            "type": "string",
            "description": "The date of departure in 'YYYY-MM-DD' format"
        },
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.amadeus = AmadeusClient().get_client()

    def forward(self, origin: str, destination: str, departure_date: str) -> str:
        print('sleeping')
        time.sleep(0.5)
        print('done sleeping')
        response = self.amadeus.shopping.flight_offers_search.get(
            originLocationCode = origin,
            destinationLocationCode = destination,
            departureDate = departure_date,
            adults=1,
            max =5
        )

        if not response.data:
            return("No flights found for the requested criteria.")
        
        ## time to parse

        results = []
        for flight in response.data:
            price = flight['price']['total']
            currency = 'USD'
            airline = flight['itineraries'][0]['segments'][0]['carrierCode']
            results.append(f'Flight: Airline {airline}, Price: {price} {currency}')

        print(results)
        return results




    