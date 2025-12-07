from smolagents import Tool
from tools.amadeus_client import AmadeusClient
import time

class HotelSearchTool(Tool):
    name = "search_hotels"
    description = (
        "Searches for hotel offers in a specific city. "
        "Returns a list of hotels with available rooms and prices."
    )
    inputs = {
        "city_code": {
            "type": "string",
            "description": "The 3-letter IATA code for the city."
        },
        "check_in_date": {
            "type": "string",
            "description": "Check-in date in 'YYYY-MM-DD' format."
        },
        "check_out_date": {
            "type": "string",
            "description": "Check-out date in 'YYYY-MM-DD' format."
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.amadeus = AmadeusClient().get_client()

    def forward(self, city_code: str, check_in_date: str, check_out_date: str) -> str:
        print('sleeping')
        time.sleep(0.5)
        print('done sleeping')

        hotels_response = self.amadeus.reference_data.locations.hotels.by_city.get(
            cityCode=city_code
        )

        if not hotels_response.data:
            return "No hotels found in this city."

        hotel_ids = [hotel['hotelId'] for hotel in hotels_response.data[:5]]
        hotel_ids_str = ",".join(hotel_ids)

        response = self.amadeus.shopping.hotel_offers_search.get(
            hotelIds=hotel_ids_str,
            checkInDate=check_in_date,
            checkOutDate=check_out_date,
            adults=1,
            currency='USD',
            bestRateOnly=True
        )

        if not response.data:
            return "No hotel offers found for these dates."

        results = []
        for offer in response.data:
            hotel_name = offer['hotel'].get('name', 'Unknown Hotel')
            if 'offers' in offer and len(offer['offers']) > 0:
                price = offer['offers'][0]['price']['total']
                currency = offer['offers'][0]['price']['currency']
                results.append(f"Hotel: {hotel_name}, Total Price: {price} {currency}")

        print(results)
        return (results)