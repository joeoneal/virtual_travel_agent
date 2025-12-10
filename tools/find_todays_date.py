from smolagents import Tool
from datetime import datetime
import time

class FindTodaysDate(Tool):
    name = "find_todays_date"
    description = "Retrieves the current date in YYYY-MM-DD format. Useful for answering questions relative to the current day."
    inputs = {} 
    output_type = "string"

    def forward(self) -> str:
        print('sleeping')
        time.sleep(1)
        print('done sleeping')

        return datetime.today().strftime('%Y-%m-%d')