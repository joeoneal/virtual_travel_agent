from smolagents import Tool
from tools.serp_client import SerpApiClient
import time

class HotelSearchTool(Tool):
    name = "search_hotels"
    description = (
        "Searches for hotel prices and availability in a specific city. "
        "Returns a list of top hotels with prices, totals, and booking links."
    )
    inputs = {
        "city_name": {
            "type": "string",
            "description": "The city name (e.g., 'Denver', 'New York')."
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
        self.client = SerpApiClient()

    def forward(self, city_name: str, check_in_date: str, check_out_date: str) -> str:
        print('sleeping')
        time.sleep(1)
        print('done sleeping')

        params = {
            "engine": "google_hotels",
            "q": f"Hotels in {city_name}",
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "currency": "USD",
            "hl": "en"
        }

        results = self.client.search(params)
        
        search_link = results.get('search_metadata', {}).get("google_hotels_url", "No link available")

        if "properties" not in results:
                return f"No hotels found. Try searching here: {search_link}"

        hotel_options = []
        for hotel in results["properties"][:5]:
            name = hotel.get("name", "Unknown Hotel")
            price = hotel.get("rate_per_night", {}).get("lowest", "N/A")
            total = hotel.get("total_rate", {}).get("lowest", "N/A")
            
            link = hotel.get("link", search_link)
            
            hotel_options.append(f"Hotel: {name}, Nightly: {price}, Total: {total}, Link: {link}")

        return "\n\n".join(hotel_options)