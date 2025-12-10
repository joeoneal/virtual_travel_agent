from smolagents import Tool
import pandas as pd
import os

class IataSearchTool(Tool):
    name = "lookup_city_code"
    description = (
        "Searches for IATA airport codes. Returns ONLY the 3-letter codes separated by commas. "
        "Example Output: 'JFK, LGA, EWR'"
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "City name (e.g. 'New York', 'Paris')."
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame()
        self._load_data()

    def _load_data(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, "..", "airports.csv")
            csv_path = os.path.abspath(csv_path)

            if not os.path.exists(csv_path):
                print(f"⚠️ Warning: {csv_path} not found")
                return

            self.df = pd.read_csv(csv_path, on_bad_lines='skip', dtype=str).fillna("")
            
            possible_cols = ['City', 'Country', 'Airport name', 'IATA']
            valid_cols = [c for c in possible_cols if c in self.df.columns]
            self.df['search_text'] = self.df[valid_cols].agg(' '.join, axis=1).str.lower()

        except Exception as e:
            print(f"error: {e}")
            self.df = pd.DataFrame() 

    def forward(self, query: str) -> str:
        if self.df.empty:
            return "error: Database not loaded."

        clean_query = query.lower().strip()
        
        ## exact
        if len(clean_query) == 3:
            match = self.df[self.df['IATA'].str.lower() == clean_query]
            if not match.empty:
                return match.iloc[0]['IATA']

        ## close
        results = self.df[self.df['search_text'].str.contains(clean_query, na=False)]

        if results.empty:
            return "No IATA code found."

      
        codes = results['IATA'].unique().tolist()
        return ", ".join(codes[:5])