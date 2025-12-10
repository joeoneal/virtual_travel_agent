from smolagents import Tool
import time

class BudgetCalculatorTool(Tool):
    name = "check_trip_budget"
    description = (
        "Calculates the total cost of the trip. If a budget_limit is provided, "
        "it also checks if the trip fits within that budget."
    )
    inputs = {
        "flight_price": {
            "type": "number",
            "description": "The price of the flight in USD (e.g., 350.50)."
        },
        "hotel_price": {
            "type": "number",
            "description": "The total price of the hotel in USD (e.g., 400.00)."
        },
        "budget_limit": {
            "type": "number",
            "description": "The user's maximum budget in USD. Optional.",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, flight_price: float, hotel_price: float, budget_limit: float = None) -> str:
        print('sleeping')
        time.sleep(1)
        print('done sleeping')

        total_cost = flight_price + hotel_price
        
        if budget_limit is None:
             return (
                f"TOTAL CALCULATED.\n"
                f"Total Cost: ${total_cost:.2f}\n"
                f"(No budget limit was specified by the user)."
            )

        remaining = budget_limit - total_cost
        
        if remaining >= 0:
            return (
                f"WITHIN BUDGET.\n"
                f"Total Cost: ${total_cost:.2f}\n"
                f"Budget: ${budget_limit:.2f}\n"
                f"Remaining: ${remaining:.2f}"
            )
        else:
            return (
                f"OVER BUDGET.\n"
                f"Total Cost: ${total_cost:.2f}\n"
                f"Budget: ${budget_limit:.2f}\n"
                f"Over by: ${abs(remaining):.2f}"
            )