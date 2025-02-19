from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """Abstract base class for discounts."""
    
    @abstractmethod
    def apply_discount(self, original_price):
        pass

class PercentageDiscount(DiscountStrategy):
    """Discount based on a percentage off the price."""
    
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, original_price):
        discount_amount = (self.percentage / 100) * original_price
        return max(0, original_price - discount_amount)

class FixedAmountDiscount(DiscountStrategy):
    """Discount based on a fixed amount off the price."""
    
    def __init__(self, amount):
        self.amount = amount

    def apply_discount(self, original_price):
        return max(0, original_price - self.amount)
