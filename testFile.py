from models import NearEarthObject, CloseApproach

neo = NearEarthObject("433", False, name="Eros", diameter=2.5)

print(neo)

close_approach = CloseApproach("1900-Jan-01 00:11", 0.0921795123769547, 16.7523040362574, neo)

print(close_approach)