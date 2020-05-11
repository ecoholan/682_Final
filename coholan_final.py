#Eric Coholan
#4/30/2020
#GEOG 682 Final 

import processing

crimes = "S:/682/Spring20/ecoholan/Crime_Incidents_in_2017.shp"
ward = "S:/682/Spring20/ecoholan/Ward_from_2012.shp"

iface.addVectorLayer(ward, "ward", "ogr")
iface.addVectorLayer(crimes, "crimes", "ogr")

crimes = iface.activeLayer()
crimes.selectByExpression("METHOD = 'GUN'")

fn = "S:/682/Spring20/ecoholan/guncrimes.shp"
writer = QgsVectorFileWriter.writeAsVectorFormat(crimes, fn, 'utf-8', \
driverName = 'ESRI Shapefile', onlySelected = True)
del(writer)

crimes.removeSelection()

gunshots = "S:/682/Spring20/ecoholan/Shot_Spotter_Gun_Shots.shp"
iface.addVectorLayer(gunshots, "gunshots", "ogr")
gunshots = iface.activeLayer()
gunshots.selectByExpression("year(DATETIME) = 2017")

fn2 = "S:/682/Spring20/ecoholan/SS_2017.shp"
writer = QgsVectorFileWriter.writeAsVectorFormat(gunshots, fn2, 'utf-8', \
driverName = 'ESRI Shapefile', onlySelected = True)
del(writer)

gunshots.removeSelection()

guncrimes = fn
iface.addVectorLayer(guncrimes, "guncrimes", "ogr")

processing.run("qgis:countpointsinpolygon", {'POLYGONS':ward, 'POINTS':fn, 'FIELD':"NUMPOINTS", 'OUTPUT':"S:/682/Spring20/ecoholan/count.shp"})

count = "S:/682/Spring20/ecoholan/count.shp"
iface.addVectorLayer(count, "count", "ogr")
count = iface.activeLayer()

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
        
fc = count.featureCount()

for i in range(0, fc):
    feat = count.getFeature(i)
    print(feat['NAME'], 'Gun Crimes per 10,000 people:', feat['GC_per'])

SS_2017 = fn2
iface.addVectorLayer(SS_2017, "SS_2017", "ogr")
    
processing.run("qgis:countpointsinpolygon", {'POLYGONS':ward, 'POINTS':SS_2017, 'FIELD':"NUMPOINTS", 'OUTPUT':"S:/682/Spring20/ecoholan/count2.shp"})

count2 = "S:/682/Spring20/ecoholan/count2.shp"
iface.addVectorLayer(count2, "count2", "ogr")
count2 = iface.activeLayer()

pv2 = count2.dataProvider()
pv2.addAttributes([QgsField('SS_per', QVariant.Double)])
count2.updateFields()

context2 = QgsExpressionContext()
context2.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(count2))

with edit(count2):
    for i in count2.getFeatures():
        context2.setFeature(i)
        i['SS_per'] = expression.evaluate(context2)
        count2.updateFeature(i)
        
fc2 = count2.featureCount()

for i in range(0, fc2):
    feat = count2.getFeature(i)
    print(feat['NAME'], 'ShotSpotter shooting incidents detected per 10,000 people:', feat['SS_per'])

QgsProject.instance().removeMapLayer(count2.id())

SS_2017 = iface.activeLayer()
QgsProject.instance().removeMapLayer(SS_2017.id())

count = iface.activeLayer()
QgsProject.instance().removeMapLayer(count.id())

guncrimes = iface.activeLayer()
QgsProject.instance().removeMapLayer(guncrimes.id())