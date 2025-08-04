from models import NearEarthObject, CloseApproach
from extract import load_neos, load_approaches

# neo = NearEarthObject("433", False, name="Eros", diameter=2.5)
#
# print(neo)
#
# close_approach = CloseApproach("1900-Jan-01 00:11", 0.0921795123769547, 16.7523040362574, neo)
#
# print(close_approach)

# print(load_neos(r'C:\Users\E3000185\PycharmProjects\NEO-Program\data\neos.csv'))

print(load_approaches(r'C:\Users\E3000185\PycharmProjects\NEO-Program\data\cad.json'))
