"""
These calculations are made for equilateral prism, with refractive index 1.475,
assuming the incident ray entered at 30deg from the normal of the face.
Assuming n_air = 1.

Negative exit point height means that the rays won't leave from that face.
Simulation link: https://phydemo.app/ray-optics/simulator/#XQAAAALfAwAAAAAAAABFqcrGU8hqLFnpmVEV4ih8ZyjFwnhZ3kdCyD8WxTXvqXpu-r8uwPK_yEbzUTBoU_j0R0Ep7K5zbbFlgq8uRecqSz6-fNRxv8hHARTc0C0h3eD3V_BmcgcQNFjzXOyrPKsQAvqJ42lWlCZGQr1jkXd9gKGdmNIk9cIHYJoIxfgHfj-M86VIUoMcFlkyxxXMsC4UlOyGZhQPmeGZ7ld4hzj3i8fQH-26TPq1W5ELnWBrC8_3ZT_rIYPHvI04htQUdQ7KsOFFShJCtp0rPMY-qO3p9l1WzkecVx_aiteyG151CPh2cs7ZjsfnbICTBmMiVv1N3hE4nfCIGaJNWqiaBVR1vKoeS6Cb9wDdxZAqfQWn0U-Xuu4Zp_q4_zPmOtwn5RCBreddD21lJB3RbKoTDkomYpLn9m-Zmk7zecRGignn29rmyd2yLuY0HEe_Ogu9HzYHMaybEGgThivppLNAF_BY633Q0SV8k5j7V_Kh0B_XFO9iWr_qge8XFhmPKe5q7FuwhOSxV8vqs3v2mVVuTcUehnGL5toVpYXW-lpYGJC5bWWIsV_p23jI4jxXx5JkyFqqoT04zbtWOmE-Ps5rZmtVS4v-OspcfmOJ6L8zt3ZY7mOn79-O2TPaafsnV49cbnQXFLGWBOsFW8oPse_ItLZrFoyKAXeNB3wMEq35MpSEYNCBcsAAZf9LICt7OOiPN9Z5nJ1WwKaOXoNGolWTpr039bW9bC5SW8lHQ-fZ1Icd-1_Twy49d_QnDpKVF1IYjVQhdebvXdNbK34mmNqH77pWJXpg5MGXDgcqXzYIwtiRnO64C7KFIpfXARpcwxYo4AGnXA9iLX7hOoNR__KelNQ
In the simulation, there is 19.39x zoom, so convert dimensions before using.
"""

from math import *

AB = BC = AC = 16.5  # Hardcoding for my prism
n_prism = 1.475
angle_incident_1 = 30
angle_refraction_1 = degrees(asin(sin(radians(30)) / n_prism))
angle_refraction_from_horizontal = 30 - angle_refraction_1


h1 = float(input("Enter the h1:"))
AE = E1C = h1 / sin(radians(60))
EB = EE1 = BE1 = AB - AE

BH3 = BE1 / 2
EH3 = EB * sin(radians(60))
H3O = tan(radians(30 + angle_refraction_from_horizontal)) * EH3
OC = BC - BH3 - H3O
h2 = sin(radians(60)) * OC

print(f"Exit point height from base is {h2}")

AH1 = AE / 2
CH2 = OC / 2
H1H2 = AC - AH1 - CH2

print(f"Entry point depth along the horizontal axis: {AH1}")
print(f"Horizontal distance between the entry and exit points: {H1H2}")
print(f"Exit point depth along the horizontal axis: {CH2}")