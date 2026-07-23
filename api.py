"""
This file provides an API wrapper around the Black-Scholes pricing engine.

It exposes two HTTP POST endpoints: /price for option pricing and /greeks for Greek calculations.
The API uses FastAPI to convert Python functions into web-accessible endpoints, and Pydantic to validate incoming JSON requests. 

The structure follows four conceptual layers:
    1. Imports: FastAPI, Pydantic, and the pricing engine
    2. App Creation: Instantiating the FastAPI application
    3. Request Model: Defining the JSON schema for incoming requests
    4. Endpoints: Exposing pricing and Greek calculations over HTTP
"""

# Imports
from fastapi import FastAPI
from pydantic import BaseModel
from black_scholes import black_scholes_prices, black_scholes_greeks


# App creation
app = FastAPI()


# Request model using BaseModel class -> defining JSON schema
class OptionRequest(BaseModel):
    S: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: str    # "call" or "put"


# Endpoint definitions
@app.post("/price")
def price(req: OptionRequest):
    """ The purpose of this endpoint is to take the user inputs and price the option using the Black Scholes model."""
    result = black_scholes_prices(req.S, req.K, req.T, req.r, req.sigma, req.option_type)

    return {"Option Price": result}


@app.post("/greeks")
def greeks(req: OptionRequest):
    """ The purpose of this endpoint is to take the user inputs and calculate the specified option's Greeks."""
    result = black_scholes_greeks(req.S, req.K, req.T, req.r, req.sigma, req.option_type)

    return result

# Addition of GET request homepages
@app.get("/")
def root():
    return {
        "Service": "Options Pricing API",
        "Status": "Running...",
        "Endpoints": ["/price", "/greeks", "/docs"]
    }


@app.get("/price")
def price_get():
    return {"Message": "Use POST with JSON body to calculate option price."}


@app.get("/greeks")
def greeks_get():
    return {"Message": "Use POST with JSON body to calculate Greeks."}