import postcodes_uk
from postcodes_uk import Postcode


# Create a Postcode object
p = Postcode.from_string('AB10 1XG')

# Print the postcode area
print(p.area)
print(p.district)
print(p.sector)
print(p.unit)