#Eric Coholan
#4/30/2020
#GEOG 682 Final 

import processing 

crimes = "S:/682/Spring20/ecoholan/Crime_Incidents_in_2017.shp"
gunshots = "S:/682/Spring20/ecoholan/Shot_Spotter_Gun_Shots.shp"
ward = "S:/682/Spring20/ecoholan/Ward_from_2012.shp"

iface.addVectorLayer(crimes, "crimes", "ogr")

crimes = iface.activeLayer()
crimes.selectByExpression(" 'METHOD' = 'GUN'")

print(crimes)





