#Eric Coholan
#4/30/2020
#GEOG 682 Final 

import processing

crimes = "S:/682/Spring20/ecoholan/Crime_Incidents_in_2017.shp"
gunshots = "S:/682/Spring20/ecoholan/Shot_Spotter_Gun_Shots.shp"
ward = "S:/682/Spring20/ecoholan/Ward_from_2012.shp"

iface.addVectorLayer(ward, "ward", "ogr")
iface.addVectorLayer(gunshots, "gunshots", "ogr")
iface.addVectorLayer(crimes, "crimes", "ogr")

crimes = iface.activeLayer()
crimes.selectByExpression("METHOD = 'GUN'")

fn = "S:/682/Spring20/ecoholan/guncrimes.shp"
writer = QgsVectorFileWriter.writeAsVectorFormat(crimes, fn, 'utf-8', \
driverName = 'ESRI Shapefile', onlySelected = True)
del(writer)

processing.run("qgis:joinbylocationsummary", {'INPUT':ward,'JOIN':"S:/682/Spring20/ecoholan/guncrimes.shp",'PREDICATE':1, \
'SUMMARIES':0,'OUTPUT':"S:/682/Spring20/ecoholan/gunjoin.shp"})

processing.run("qgis:intersection", {'INPUT':gunshots, 'OVERLAY':ward,\
'OUTPUT':"S:682/Spring20/ecoholan/intersect.shp"})

processing.run("qgis:joinbylocationsummary", {'INPUT':"S:/682/Spring20/ecoholan/gunjoin.shp",'JOIN':"S:682/Spring20/ecoholan/intersect.shp",'PREDICATE':1, \
'SUMMARIES':0,'OUTPUT':"S:/682/Spring20/ecoholan/gunfinal.shp"})

gunfinal = "S:/682/Spring20/ecoholan/gunfinal.shp"
gunfinal = iface.activeLayer()

pv = gunfinal.dataProvider()
pv.addAttributes([QgsField('GC_per_10000', QVariant.Double), QgsField('SS_per_10000', QVariant.Double)])
gunfinal.updateFields()

expression1 = QgsExpression("'CCN_count'/('POP_2010'/10000)")
expression2 = QgsExpression("'ID_count'/('POP_2010'/10000)")

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(gunfinal))

with edit(gunfinal):
    for i in gunfinal.getFeatures():
        context.setFeature(i)
        i['GC_per_10000'] = expression1.evaluate(context)
        gunfinal.updateFeature(i)
        
with edit(gunfinal):
    for i in gunfinal.getFeatures():
        context.setFeature(i)
        i['SS_per_10000'] = expression2.evaluate(context)
        gunfinal.updateFeature(i)
        
