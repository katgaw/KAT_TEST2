from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.tools import StructuredTool
import yfinance as yf
from typing import List
from datetime import datetime,timedelta
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

def data_analyst_tools():
    def get_crypto_price(cryptocurrencyticker: str) -> str:
        current_data=cg.get_price(ids=cryptocurrencyticker, vs_currencies='usd',include_market_cap='true', include_24hr_vol='true',include_last_updated_at='true')
        return str(current_data)

    class CryptoPriceCheckInput(BaseModel):
        """Input for Crypto price check."""
        Cryptoticker: str = Field(..., description="Ticker symbol for Crypto or index")

    class CryptoPriceTool(BaseTool):
        name = "get_crypto_price"
        description = "Useful for when you need to find out the price of Cryptocurrency. You should input the Crypto ticker used on the Coingecko API"
        """Input for Cryptocurrency price check."""
        Cryptoticker: str = Field(..., description="Ticker symbol for Crypto or index")
        def _run(self, Cryptoticker: str):
            # print("i'm running")
            price_response = get_crypto_price(Cryptoticker)

            return str(price_response)

        def _arun(self, Cryptoticker: str):
            raise NotImplementedError("This tool does not support async")
        args_schema: Optional[Type[BaseModel]] = CryptoPriceCheckInput


    tools_data_analyst = [StructuredTool.from_function(
            func=CryptoPriceTool,
            args_schema=CryptoPriceCheckInput,
            description="Function to get current Crypto prices.",
        ),
    ]
    return tools_data_analyst