from decimal import Decimal

from app.services import withdraw

result= withdraw("W004", Decimal("100"))

print(result)