<p align="center">
  <b>2017 Washington D.C. Gun Crime Analysis</b><br>
  <b>Eric Coholan</b><br>
  <b>4/30/2020</b><br>
</p>


#### Introduction
To determine if expansion of the ShotSpotter gunshot detection network is necessary, the project assessed gun crime rates and ShotSpotter shooting incident detection rates on a per-ward basis. Utilizing publicly available data sources, the number of gun crimes committed per 10,000 people and the number of shooting incidents detected by ShotSpotter per 10,000 people were calculated for each ward and visualized through QGIS 3.49 mapping tools. The calculation process was then automated with Python code, enabling future analyses to be performed on alternate data. Upon inspection of the data products, it is recommended that the ShotSpotter gunshot detection network be expanded into Ward 2.

#### Analysis
The three shapefiles used in the project are publicly available on [Open Data DC](http://opendata.dc.gov). The 'Ward_from_2012' shapefile is a polygon layer of Washington D.C.'s 2012 election wards and includes summary demographic attributes such as age and population for each ward. The 'Crime_Incidents_in_2017' shapefile is a point layer containing every crime committed in Washington D.C. during 2017, with attributes including latitude, longitude, and any associated weapon. The 'Shot_Spotter_Gun_Shot' is a point layer describing the location of every ShotSpotter detected gunshot in Washington D.C. from 2014 until July 2019.

The thematic map displaying the number of gun crimes committed per 10,000 people in 2017 in each ward was produced in QGIS 3.49. Using Selection Expression, all gun crimes were selected from the 'Crime_Incidents_in_2017' shapefile, and converted into a new point shapefile called 'guncrimes'. The Point in Polygon function within QGIS vector analysis tools was then used to combine 'Ward_from_2012' and 'guncrimes', creating a new polygon shapefile identifying the number of gun crimes in each ward, called 'count'. Within the Field Calulator in 'count', the number of gun crimes in each ward (NUMPOINTS) was divided by the quotient of 2010 population (POP_2010) and 10,000, producing new field known as GC_per, which indicated the number of crimes committed per 10,000 people in 2017 in each ward. Ward labels and thematic colorization were added to the map using the Properties tab in 'count', and standard map elements were added through the Map Layout window.

<p align="center">
  <kbd>
    <img src="https://github.com/ecoholan/682_Final/blob/master/GC.jpg">
  </kbd>
</p>

The thematic map displaying the number of shotting incidents detected by ShotSpotter per 10,000 people in 2017 in each ward was produced in QGIS 3.49. Using Selection Expression, all shooting incidents from the year 2017 were selected from the 'Shot_Spotter_Gun_Shot' shapefile, and converted into a new point shapefile called 'SS_2017'. The Point in Polygon function within QGIS vector analysis tools was then used to combine 'Ward_from_2012' and 'SS_2017', creating a new polygon shapefile identifying the number of shooting incidents in each ward, called 'count2'. Within the Field Calulator in 'count2', the number of shooting incidents in each ward (NUMPOINTS) was divided by the quotient of 2010 population (POP_2010) and 10,000, producing new field known as SS_per, which indicated the number of shooting incidents per 10,000 people in 2017 in each ward. Ward labels and thematic colorization were added to the map using the Properties tab in 'count', and standard map elements were added through the Map Layout window.

<p align="center">
  <kbd>
    <img src="https://github.com/ecoholan/682_Final/blob/master/SS.jpg">
  </kbd>
</p>

Number of gun crimes committed per 10,000 people in 2017 in each ward:
- Ward 1: 15.31
- Ward 2: 7.05
- Ward 3: 2.66
- Ward 4: 16.63
- Ward 5: 36.07
- Ward 6: 21.25
- Ward 7: 57.84
- Ward 8: 57.70
