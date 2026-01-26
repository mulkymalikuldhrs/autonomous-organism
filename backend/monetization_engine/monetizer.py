from enum import Enum

class MonetizationModel(Enum):
    AFFILIATE = "affiliate"
    SUBSCRIPTION = "subscription"
    LEAD_SALES = "lead_sales"
    DONATION = "donation"

def determine_pricing(idea: str):
    """
    Determines the best pricing model for an idea.
    """
    # Placeholder for now - will use a more sophisticated model in the future
    return MonetizationModel.SUBSCRIPTION

def create_packages():
    """
    Creates pricing packages.
    """
    # Placeholder for now
    return [
        {"name": "Basic", "price": 9.99},
        {"name": "Pro", "price": 29.99},
    ]
