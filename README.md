<p align="center">
  <b>2017 Washington D.C. Gun Crime Analysis</b><br>
  <b>Eric Coholan</b><br>
  <b>5/11/2020</b><br>
</p>


#### Introduction
To determine if expansion of the ShotSpotter gunshot detection network is necessary, the project assessed gun crime rates and ShotSpotter shooting incident detection rates on a per-ward basis. Utilizing publicly available data sources, the number of gun crimes committed per 10,000 people and the number of shooting incidents detected by ShotSpotter per 10,000 people were calculated for each ward and visualized through QGIS 3.49 mapping tools. The calculation process was then automated with Python code, enabling future analyses to be performed on alternate data. Upon inspection of the data products, it is recommended that the ShotSpotter gunshot detection network be expanded into Ward 2.

#### Analysis
The three shapefiles used in the project are publicly available on [Open Data DC](http://opendata.dc.gov). The 'Ward_from_2012' shapefile is a polygon layer of Washington D.C.'s 2012 election wards and includes summary demographic attributes such as age and population for each ward. The 'Crime_Incidents_in_2017' shapefile is a point layer containing every crime committed in Washington D.C. during 2017, with attributes including latitude, longitude, and any associated weapon. The 'Shot_Spotter_Gun_Shot' is a point layer describing the location of every ShotSpotter detected gunshot in Washington D.C. from 2014 until July 2019.

The thematic map displaying the number of gun crimes committed per 10,000 people in 2017 in each ward was produced in QGIS 3.49. Using Selection Expression, all gun crimes were selected from the 'Crime_Incidents_in_2017' shapefile, and converted into a new point shapefile called 'guncrimes'. The Point in Polygon function within QGIS vector analysis tools was then used to combine 'Ward_from_2012' and 'guncrimes', creating a new polygon shapefile identifying the number of gun crimes in each ward, called 'count'. Within the Field Calulator in 'count', the number of gun crimes in each ward (NUMPOINTS) was divided by the quotient of 2010 population (POP_2010) and 10,000, producing new field known as 'GC_per', which indicated the number of crimes committed per 10,000 people in 2017 in each ward. Ward labels and thematic colorization were added to the map using the Properties tab in 'count', and standard map elements were added through the Map Layout window.

<p align="center">
  <kbd>
    <img src="https://github.com/ecoholan/682_Final/blob/master/GC.jpg">
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

The thematic map displaying the number of shooting incidents detected by ShotSpotter per 10,000 people in 2017 in each ward was produced in QGIS 3.49. Using Selection Expression, all shooting incidents from the year 2017 were selected from the 'Shot_Spotter_Gun_Shot' shapefile, and converted into a new point shapefile called 'SS_2017'. The Point in Polygon function within QGIS vector analysis tools was then used to combine 'Ward_from_2012' and 'SS_2017', creating a new polygon shapefile identifying the number of shooting incidents in each ward, called 'count2'. Within the Field Calulator in 'count2', the number of shooting incidents in each ward (NUMPOINTS) was divided by the quotient of 2010 population (POP_2010) and 10,000, producing new field known as 'SS_per', which indicated the number of shooting incidents per 10,000 people in 2017 in each ward. Ward labels and thematic colorization were added to the map using the Properties tab in 'count', and standard map elements were added through the Map Layout window.

<p align="center">
  <kbd>
    <img src="https://github.com/ecoholan/682_Final/blob/master/SS.jpg">
  </kbd>
</p>

Number of shooting incidents detected by ShotSpotter per 10,000 people in 2017 in each ward:
- Ward 1: 16.52
- Ward 2: 0.26
- Ward 3: 0.00
- Ward 4: 20.85
- Ward 5: 56.52
- Ward 6: 37.12
- Ward 7: 232.20
- Ward 8: 289.02

#### Automation
After importing the processing package and displaying the three aforementioned shapefiles, the automated code can be described by three processes: the selection of features and subsequent creation of new layers from the selections, the use of the 'countpointsinpolygon' function, and the creation of a field specifying the number of either gun crimes or shooting incidents per 10,000 people in each ward.

After renaming 'Crime_Incidents_in_2017' to 'crimes', and specifying the shapefile as the active layer in the interface, the following snippet of code selects all gun crimes and reads them into the 'guncrimes' shapefile:

```ruby
crimes.selectByExpression("METHOD = 'GUN'")

fn = "S:/682/Spring20/ecoholan/guncrimes.shp"
writer = QgsVectorFileWriter.writeAsVectorFormat(crimes, fn, 'utf-8', \
driverName = 'ESRI Shapefile', onlySelected = True)
```

The 'selectByExpression' function enables all instances of the string 'GUN' be pulled from the METHOD field in 'crimes'. Following the selection, an empty 'guncrimes' shapefile is stored in the working directory and the 'writeAsVectorFormat' function is employed to transfer the contents of the selection into 'guncrimes'. A similar process was used to select all ShotSpotter detected shooting incidents from the year 2017, and read them into the 'SS_2017' point shapefile.

Following the creation of the selection layers the Point in Polygon vector analysis process was used to identify the number of selected features that appeared in each ward:

```ruby
processing.run("qgis:countpointsinpolygon", {'POLYGONS':ward, 'POINTS':fn, 'FIELD':"NUMPOINTS", 'OUTPUT':"S:/682/Spring20/ecoholan/count.shp"})
```

The code specifies the renamed 'Ward_from_2012' shapefile as the input polygon layer, with the 'guncrimes' layer (here characterized as 'fn') occupying the point layer input. The output field is named 'NUMPOINTS' to describe the number of points occurring in each ward, and the new polygon layer containing 'NUMPOINTS' is to be called 'count' and located in the working directory. Again the process is easily reproducible with ShotSpotter data.

Upon creation of the 'count' layer, the following loop structure generates a new field containing the number of gun crimes committed per 10,000 people in each ward:

```ruby
pv = count.dataProvider()
pv.addAttributes([QgsField('GC_per', QVariant.Double)])
count.updateFields()

expression = QgsExpression("NUMPOINTS/(POP_2010/10000)")

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(count))

with edit(count):
    for i in count.getFeatures():
        context.setFeature(i)
        i['GC_per'] = expression.evaluate(context)
        count.updateFeature(i)
```

The initial three lines of code create a new field in 'count' called 'GC_per" that is specified to be data type double. The 'QgsExpression' function then stores the requisite expression in variable 'expression'. The following two lines of code encapsulate the parameters for which 'expression' should be evaluated, and are stored in variable 'context'. Utilizing a looping structure, the expression is subsequently evaluated for every feature in the field 'GC_per', displaying the number of gun crimes committed per 10,000 people in each ward. Like all previous code, the preceding structure is also compatible with ShotSpotter data.

The functionality of the code is not exclusive to the three shapefiles obtained for the project. By simply changing the names of temporally different data to reflect the renamed shapefiles (wards, crimes, and gunshots), and possibly adjusting the selection parameters depending on the objective, this code could run the same analysis on other data inputs.

#### Results
Based on 2017 ShotSpotter data, the ShotSpotter gunshot detection network appears to be present in all but the second and third wards. Ward 2 showcased a rate of 7.05 gun crimes per 10,000 people and Ward 3 sported a rate of 2.66 gun crimes per 10,000 people. ShotSpotters stationed in adjacent wards detected multiple gunshots in Ward 2 while no gunshots were detected in Ward 3. For these reasons, it is recommended that the ShotSpotter gunshot detection network expand coverage into Ward 2 while also maintaining all current locations in Washington D.C.

The analysis was limited by time and data resolution. In regard to time, the project specified only the use of crime and ShotSpotter data from 2017, although similar crime datasets from different years exist on [Open Data DC](http://opendata.dc.gov). Given more time to complete the project, these datasets combined with the current ShotSpotter dataset (2014 - July 2019), could have been used to map trends in gun crime rate and shooting incident detection on a year-to-year basis, producing a more informed recommendation. The resolution of ward data also reduces the accuracy of the results. With spatial data compartmentalized into more specific sectors (census tracts, census blocks, etc.) it would be possible to view gun crime rates and ShotSpotter shooting incident detection rates at a neighborhood-by-neighborhood level. At this finer spatial resolution, city officials would have a higher degree of certainty about the location where ShotSpotters must be placed.
