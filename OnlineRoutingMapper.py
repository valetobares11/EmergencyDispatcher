# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OnlineRoutingMapper
                                 A QGIS plugin
 Generate routes by using online services (Google Directions, Here, MapBox, YourNavigation, OSRM etc.)
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-10-01
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Mehmet Selim BILGIN
        email                : mselimbilgin@yahoo.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QAction, QMessageBox

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .OnlineRoutingMapper_dialog import OnlineRoutingMapperDialog, OnlineRoutingMapperDialogAgPedido, OnlineRoutingMapperDialogModMapa
import os.path
from urllib.request import urlopen

from .routeprovider import RouteProvider
from .db import createTablePoints, insertarPoints, seleccionarPoints, borrarPoint, seleccionarPoint
from .util import geocode_address, agregar_texto_con_saltos_de_linea
from qgis.gui import *
from qgis.core import *

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import platform

from .config import *
from qgis.PyQt.QtWidgets import QTableWidgetItem,QPushButton 


class OnlineRoutingMapper:
    

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'OnlineRoutingMapper_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Online Routing Mapper')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'OnlineRoutingMapper')
        self.toolbar.setObjectName(u'OnlineRoutingMapper')
        self.dlg_back = None
        self.listPointsExclution = []
        self.tipoAutomovil = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('OnlineRoutingMapper', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/OnlineRoutingMapper/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Online Routing Mapper'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def clickHandler(self, pointXY):
        if self.no == 0:
            startPointXY = QgsPointXY(pointXY)
            # self.startRubberBand.removeLastPoint()
            # self.startRubberBand.removeLastPoint()
            self.startRubberBand.addPoint(startPointXY)
            self.dlg.startTxt.setText(str(pointXY.x()) + ',' + str(pointXY.y()))
        else:
            stopPointXY = QgsPointXY(pointXY)
            # self.stopRubberBand.removeLastPoint()
            # self.stopRubberBand.removeLastPoint()
            self.stopRubberBand.addPoint(stopPointXY)
            self.dlg.stopTxt.setText(str(pointXY.x()) + ',' + str(pointXY.y()))
        self.dlg.showNormal()

        # free them
        self.canvas.unsetMapTool(self.clickTool)
        self.clickTool.canvasClicked.disconnect(self.clickHandler)

    def toolActivator(self, no):
        self.no = no
        self.dlg.showMinimized()
        self.clickTool.canvasClicked.connect(self.clickHandler)
        self.canvas.setMapTool(self.clickTool)  # clickTool is activated

    def crsTransform(self, pointXY):
        sourceCRS = self.canvas.mapSettings().destinationCrs()  # getting the project CRS
        destinationCRS = QgsCoordinateReferenceSystem(4326)  # google uses this CRS
        transformer = QgsCoordinateTransform(sourceCRS, destinationCRS,
                                             QgsProject.instance())  # defining a CRS transformer

        outputQgsPoint = transformer.transform(pointXY, QgsCoordinateTransform.ForwardTransform)

        return str(outputQgsPoint.y()) + ',' + str(outputQgsPoint.x())

    def checkNetConnection(self):
        try:
            urlopen('http://www.google.com', timeout=10)
            return True
        except Exception as err:
            pass
        return False

    def routeMaker(self, wktLineString):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(wktLineString))
        vectorLayer = QgsVectorLayer('LineString?crs=epsg:4326', 'Routing Result', 'memory')
        layerProvider = vectorLayer.dataProvider()
        vectorLayer.startEditing()
        layerProvider.addFeatures([feature])
        vectorLayer.commitChanges()
        vectorLayer.updateExtents()
        vectorLayer.loadNamedStyle(self.plugin_dir + os.sep + 'OnlineRoutingMapper.qml')
        QgsProject.instance().addMapLayer(vectorLayer)
        destinationCRS = self.canvas.mapSettings().destinationCrs()  # getting the project CRS
        sourceCRS = QgsCoordinateReferenceSystem(4326)
        transformer = QgsCoordinateTransform(sourceCRS, destinationCRS, QgsProject.instance())
        extentForZoom = transformer.transform(vectorLayer.extent(), QgsCoordinateTransform.ForwardTransform)
        self.canvas.setExtent(extentForZoom)
        self.canvas.zoomScale(self.canvas.scale() * 1.03)  # zoom out a little bit.
        QMessageBox.information(self.dlg, 'Information', 'The analysis result was added to the canvas.')

    def runAnalysis(self):
        # if len(self.dlg.startTxt.text()) > 0 and len(self.dlg.stopTxt.text()) > 0:
        if self.startPointXY is not None and self.stopPointXY is not None:
            if self.checkNetConnection():              
                startPoint = self.crsTransform(self.startPointXY)
                stopPoint = self.crsTransform(self.stopPointXY)
                # index = self.dlg.serviceCombo.currentIndex()
                try:
                    service = self.services[list(self.services)[0]]
                    self.cargar_puntos_lista()
                    wkt, url = service(startPoint, stopPoint, self.listPointsExclution, self.tipoAutomovil)
                    self.routeMaker(wkt)
                    # clear rubberbands
                    # self.startRubberBand.removeLastPoint()
                    # self.stopRubberBand.removeLastPoint()
                    # self.startRubberBand.removeLastPoint()
                    # self.stopRubberBand.removeLastPoint()
                    self.listPointsExclution=[]
                except Exception as err:
                    QgsMessageLog.logMessage(str(err))
                    QMessageBox.warning(self.dlg, 'Analysis Error',
                                        "Cannot calculate the route between the start and stop locations that you entered. Please use other Service APIs.")
            else:
                QMessageBox.warning(self.dlg, 'Network Error!', 'There is no internet connection.')
        else:
            QMessageBox.information(self.dlg, 'Warning', 'Please choose Start Location and Stop Location.')
    
    def calculate_points(self):
        punto_part = PUNTO_PARTIDA.split(',')
        self.startPointXY = QgsPointXY(float(punto_part[0]), float(punto_part[1]))
        if (self.dlg.lineEdit.text() != None):
            address = self.dlg.lineEdit.text()+ " " + CIUDAD
            x, y = geocode_address(address)
            self.stopPointXY = QgsPointXY(x,y)
        else:
            self.dlg.stopBtn.clicked.connect(lambda: self.toolActivator(1))
        log = canvas.Canvas(PATH_REPORTE, pagesize=letter)
        message= "Descripcion:  {}\npunto comienzo: {}\n punto final: {}\n ".format(self.dlg.descripcion.text(), self.startPointXY, self.stopPointXY)
        agregar_texto_con_saltos_de_linea(log,100, 750, message)
        log.save()


    def changeScreenAgPedido(self):
        self.dlg = OnlineRoutingMapperDialogAgPedido()
        self.dlg.setFixedSize(self.dlg.size())
        self.dlg.show()
        
        opciones = [CAMIONETA, CAMION_LIGERO, CAMION_PESADO]
        self.dlg.comboBox.addItems(opciones)

        self.dlg.volver.clicked.connect(lambda: self.backScreen())
        self.dlg.aceptar.clicked.connect(lambda: self.savePoints())
    
    def add_table_item(self, row, column, text):
        # Método para agregar un elemento a la tabla
        item = QTableWidgetItem(text)
        self.dlg.tableWidget.setItem(row, column, item)
    
    def borrar_todos_los_puntos(self):
        # Itera sobre todos los puntos y los elimina uno por uno
        while self.stopRubberBand.numberOfVertices() > 0:
            self.stopRubberBand.removeLastPoint()
        
        while self.startRubberBand.numberOfVertices() > 0:
            self.startRubberBand.removeLastPoint()

    def remove_points(self, id, tupla):
        # Borrar en la tabla interface
        i=0
        while i < self.dlg.tableWidget.rowCount():
            if int(self.dlg.tableWidget.item(i,0).text()) == id:
                self.dlg.tableWidget.removeRow(i)
            i += 1

        # Borrar en la BD
        borrarPoint(id)
        borrarPoint(id-1)

    def add_point(self, id, descripcion, tupla):
        rowPosition = self.dlg.tableWidget.rowCount()
        self.dlg.tableWidget.insertRow(rowPosition)
        self.dlg.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(id)))
        self.dlg.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(descripcion))
        delete_button = QPushButton("delete")
        delete_button.clicked.connect(lambda: self.remove_points(id, tupla))
        self.dlg.tableWidget.setCellWidget(rowPosition, 2, delete_button)

    def changeScreenModMapa(self):
        self.dlg = OnlineRoutingMapperDialogModMapa()
        self.dlg.setFixedSize(self.dlg.size())
        self.dlg.show()
        self.dlg.tableWidget.setColumnCount(3)
        self.dlg.tableWidget.setHorizontalHeaderLabels(["ID", "Descripcion", "Acción"])
        registros = seleccionarPoints()
        i=1
        for tupla in registros:
            if i % 2 == 0:
                self.add_point(tupla[0], tupla[3], (tupla[1], tupla[2]))
            i+=1
        
        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        self.dlg.startBtn.clicked.connect(lambda: self.toolActivator(0))
        self.dlg.stopBtn.clicked.connect(lambda: self.toolActivator(1))
        self.dlg.volver.clicked.connect(lambda: self.backScreen())
        self.dlg.aceptar.clicked.connect(lambda: self.savePointsExclution())
    
    def cargar_puntos_lista(self):
        registros = seleccionarPoints()
        i=1
        if (len(registros) > 0) :
            for tupla in registros:
                if i % 2 == 0:
                    # stop
                    stopPointExclution = tupla[2]+','+tupla[1]
                else:
                    # start
                    startPointExclution = tupla[2]+','+tupla[1]
                i+=1
            self.listPointsExclution.append((startPointExclution, stopPointExclution))
        

    def savePointsExclution(self):
        if len(self.dlg.startTxt.text()) > 0 and len(self.dlg.stopTxt.text()) > 0:
            if platform.system() == 'Windows':
                startPointExclution = self.dlg.startTxt.text()
                stopPointExclution = self.dlg.stopTxt.text()
            else:
                pointsStart = self.dlg.startTxt.text().split(',')
                startPointExclution = pointsStart[1]+','+pointsStart[0]
                pointsStop = self.dlg.stopTxt.text().split(',')
                stopPointExclution = pointsStop[1]+','+pointsStop[0]
            
            #Inserta los puntos en la BD 
            startPoint = startPointExclution.split(',')
            stopPoint = stopPointExclution.split(',')
            insertarPoints(startPoint[1], startPoint[0], self.dlg.descripcionTxt.text())
            insertarPoints(stopPoint[1], stopPoint[0], self.dlg.descripcionTxt.text())

        self.agregar_actualizar_puntos_iniciales()
        self.dlg = self.dlg_back
        self.dlg.show()

    def savePoints(self):
        self.calculate_points()
        self.tipoAutomovil = self.dlg.comboBox.currentText()
        self.dlg = self.dlg_back
        self.dlg.show()

    def backScreen(self):
        self.dlg = self.dlg_back
        self.dlg.show()

    def agregar_actualizar_puntos_iniciales(self):
        self.borrar_todos_los_puntos()
        registros = seleccionarPoints()
        i=1
        for tupla in registros:
            if i % 2 == 0:
                self.stopRubberBand.addPoint(QgsPointXY(float(tupla[1]), float(tupla[2])))
            else:
                self.startRubberBand.addPoint(QgsPointXY(float(tupla[1]), float(tupla[2])))
            i+=1

    def run(self):
        self.no = 0
        self.startPointXY = None
        self.stopPointXY = None
        createTablePoints()
        self.dlg = OnlineRoutingMapperDialog()
        
        self.dlg.setFixedSize(self.dlg.size())

        self.services = RouteProvider().services()
        # self.dlg.serviceCombo.addItems(list(self.services))

        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)  # clicktool instance generated in here.
        # self.dlg.startBtn.clicked.connect(lambda: self.toolActivator(0))
        # self.dlg.stopBtn.clicked.connect(lambda: self.toolActivator(1))
        self.dlg.runBtn.clicked.connect(self.runAnalysis)
        
        self.dlg_back = self.dlg
        self.dlg.btnAgPedido.clicked.connect(lambda: self.changeScreenAgPedido())
        self.dlg.btnModMapa.clicked.connect(lambda: self.changeScreenModMapa())
        
        self.startRubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.startRubberBand.setColor(QColor("#000000"))
        self.startRubberBand.setIconSize(10)
        self.startRubberBand.setIcon(QgsRubberBand.ICON_FULL_BOX)
        self.stopRubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.stopRubberBand.setColor(QColor("#000000"))
        self.stopRubberBand.setIconSize(10)
        self.stopRubberBand.setIcon(QgsRubberBand.ICON_FULL_BOX)
        self.agregar_actualizar_puntos_iniciales()

        self.dlg.show()
        self.dlg.closeEvent = self.close

    def close(self, event):
        #clear the rubberbands
        self.canvas.scene().removeItem(self.startRubberBand)
        self.canvas.scene().removeItem(self.stopRubberBand)


