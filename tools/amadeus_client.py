import os
import dotenv
from amadeus import Client

dotenv.load_dotenv()

class AmadeusClient:
    def __init__(self):
        self.key = os.getenv("AMADEUS_API_KEY")
        self.secret = os.getenv("AMADEUS_API_SECRET")

        if not self.key or not self.secret:
            print('no api keys founds, check .env file')
            return
        
        self.client = Client(client_id = self.key, client_secret = self.secret)
        
    def get_client(self):
        return self.client
    

if __name__ == '__main__':
    print('testing amadeus connection')
    
    client = AmadeusClient()
    client = client.get_client()

    response = client.reference_data.locations.get(
        keyword='PAR',
        subType='CITY'
    )

    print(response.data)