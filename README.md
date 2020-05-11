<p align="center">
  <b>2017 Washington D.C. Gun Crime Analysis</b><br>
  <b>Eric Coholan</b><br>
  <b>4/30/2020</b><br>
</p>


#### Introduction
To determine if expansion of the ShotSpotter gunshot detection network is necessary, the project assessed gun crime rates and ShotSpotter shooting incident detection rates on a per-ward basis. Utilizing publicly available data sources, the number of gun crimes committed per 10,000 people and the number of shooting incidents detected by ShotSpotter per 10,000 people were calculated for each ward and visualized through QGIS 3.49 mapping tools. The calculation process was then automated with Python code, enabling future analyses to be performed on alternate data. Upon inspection of the data products, it is recommended that the ShotSpotter gunshot detection network be expanded into Ward 2.

#### Analysis
The three shapefiles used in the project are publicly available on [Open Data DC](http://opendata.dc.gov). The Ward_from_2012 shapefile is a polygon layer of Washington D.C.'s 2012 election wards and includes summary demographic attributes such as age and population for each ward. The Crime_Incidents_in_2017 shapefile is a point layer containing every crime committed in Washington D.C. during 2017, with attributes including latitude, longitude, and any associated weapon. The Shot_Spotter_Gun_Shot is a point layer describing the location of every ShotSpotter detected gunshot.
