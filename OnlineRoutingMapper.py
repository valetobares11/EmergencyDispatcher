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
from qgis.PyQt.QtCore import Qt

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .OnlineRoutingMapper_dialog import OnlineRoutingMapperDialog, OnlineRoutingMapperDialogAgPedido, OnlineRoutingMapperDialogModMapa, OnlineRoutingMapperDialogModBombas, OnlineRoutingMapperDialogVerPedidos
import os.path
from urllib.request import urlopen

from .routeprovider import RouteProvider
from .db import *
from .util import *
from qgis.gui import *
from qgis.core import *

import platform
from .config import *
from .apikey import *
from qgis.PyQt.QtWidgets import QTableWidgetItem,QPushButton,QFileDialog
import pygame



#variable necesaria para saber si calcular rutas a bombas de incendio
is_incendio = False

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
        self.path_planilla_carga = None

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
        self.dlg_back.showMinimized()
        self.clickTool.canvasClicked.connect(self.clickHandler)
        self.canvas.setMapTool(self.clickTool)  # clickTool is activated

    def clickHandlerStart(self, pointXY):
        self.stopPointXY = QgsPointXY(pointXY)
        self.stopRubberBand.addPoint(self.stopPointXY)
        self.canvas.unsetMapTool(self.clickTool)
        # self.clickTool.canvasClicked.disconnect(self.clickHandler)

    def toolActivatorStartPoints(self):
        self.dlg.showMinimized()
        self.dlg_back.showMinimized()
        self.clickTool.canvasClicked.connect(self.clickHandlerStart)
        self.canvas.setMapTool(self.clickTool)  # clickTool is activated

    def clickHandlerBombas(self, pointXY):
        pointXY = QgsPointXY(pointXY)
        self.startRubberBand.addPoint(pointXY)
        self.dlg.bombaTxt.setText(str(pointXY.x()) + ',' + str(pointXY.y()))
        
        if (self.dlg.close()):
            self.dlg.showNormal()

        # free them
        self.canvas.unsetMapTool(self.clickTool)
        self.clickTool.canvasClicked.disconnect(self.clickHandlerBombas)

    def toolActivatorBombas(self):
        self.dlg.showMinimized()
        self.dlg_back.showMinimized()
        self.clickTool.canvasClicked.connect(self.clickHandlerBombas)
        self.canvas.setMapTool(self.clickTool)  # clickTool is activatedr)


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
            polygon = QgsProject.instance().mapLayersByName('Jurisdicción')[0]
            if not polygon.getFeature(1).geometry().contains(self.stopPointXY):
                QMessageBox.warning(self.dlg, 'Calculate routes bombas',"El punto esta fuera de la juridiccion")
            if self.checkNetConnection():              
                startPoint = self.crsTransform(self.startPointXY)
                stopPoint = self.crsTransform(self.stopPointXY)
                # index = self.dlg.serviceCombo.currentIndex()
                try:
                    service = self.services[list(self.services)[0]]
                    self.cargar_puntos_lista()
                    wkt, url = service(startPoint, stopPoint, self.listPointsExclution, self.tipoAutomovil)
                    report(url)
                    self.calculate_routes_a_bombas(stopPoint)
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
    
    def calculate_routes_a_bombas(self, startPoint):
        try:
            bombas = select('bomba')
            if (len(bombas)):
                service = self.services[list(self.services)[0]]
                distances = []
                for tupla in bombas:
                    if (tupla[4] == 'A'):
                        wkt, url = service(startPoint, self.crsTransform(QgsPointXY(float(tupla[1]), float(tupla[2]))))
                        response = urlopen(url).read().decode("utf-8")
                        diccionario = json.loads(response)
                        d = int(diccionario['response']['route'][0]['summary']['distance'])
                        distances.append([d,tupla[3]])

                list_distances = sorted(distances, key=lambda x: x[0])
                f = open (PATH_REPORTE,'a')
                f.write('\nLas Bombas de agua más cercanas de menor a mayor:\n')
                for tupla in list_distances:
                    f.write(str(tupla[1])+ ", distancia :"+ str(tupla[0])+'\n')
                f.close()
        except Exception as err:
            QgsMessageLog.logMessage(str(err))
            QMessageBox.warning(self.dlg, 'Calculate routes bombas',"Hubo un error al calcular las bombas mas cercanas")

    def calculate_points(self):
        punto_part = PUNTO_PARTIDA.split(',')
        self.startPointXY = QgsPointXY(float(punto_part[0]), float(punto_part[1]))
        if (self.dlg.form_direccion.text() != None):
            if (self.stopPointXY is None):
                address = self.dlg.form_direccion.text()+ " " + CIUDAD + " " + PROVINCIA
                try:
                    x, y = obtener_coordenada(address)
                    self.stopPointXY = QgsPointXY(x,y)
                    f = open (PATH_REPORTE ,'w')
                    f.write('Descripcion Emergencia: '+self.dlg.form_descripcion.text())
                    f.write('\n\nDireccion: '+address)
                    f.write('\n\nSolicitante: '+self.dlg.form_solicitante.text())
                    f.write('\n\nTelefono: '+self.dlg.form_telefono.text()+'\n\n')
                    f.close()
                except Exception as e:
                    QgsMessageLog.logMessage(str(e))
                    QMessageBox.warning(self.dlg, 'calculate_points', "No se pudo encontrar esa direccion pruebe seleccionando un punto con el buscar punto")
            else:
                try:
                    address = obtener_direccion(self.stopPointXY.x(),self.stopPointXY.y())
                    f = open (PATH_REPORTE ,'w')
                    f.write('Descripcion Emergencia: '+self.dlg.form_descripcion.text())
                    f.write('\n\nDireccion: '+self.dlg.form_direccion.text())
                    f.write('\n\nSolicitante: '+self.dlg.form_solicitante.text())
                    f.write('\n\nTelefono: '+self.dlg.form_telefono.text()+'\n\n')
                    f.close()
                except Exception as e:
                    QgsMessageLog.logMessage(str(e))
                    QMessageBox.warning(self.dlg, 'calculate_points', "No se pudo encontrar este punto")
    
    
    def call_sound(self, path_sound, fire = False):
        if (fire):
            is_incendio = True

        pygame.init()

        # Configura el sistema de sonido
        pygame.mixer.init()

        # Carga el archivo de sonido
        sonido = pygame.mixer.Sound(path_sound)

        # Reproduce el sonido
        sonido.play()


    def changeScreenAgPedido(self):
        self.dlg = OnlineRoutingMapperDialogAgPedido()
        self.dlg.setFixedSize(self.dlg.size())
        self.dlg.show()
        
        opciones = [CAMIONETA, CAMION_LIGERO, CAMION_PESADO]
        self.dlg.comboBox.addItems(opciones)

        self.dlg.buttonIncendioForestal.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_INCENDIO_FORESTAL, True))
        self.dlg.buttonIncendioRural.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_INCENDIO_RURAL, True))
        self.dlg.buttonIncendioVehicular.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_INCENDIO_VEHICULAR, True))
        self.dlg.buttonIncendioEstructura.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_RESCATE_ESTRUCTURA, True))
        self.dlg.buttonAccidenteVehicular.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_ACCIDENTE_VEHICULAR))
        self.dlg.buttonAccidenteMatPel.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_ACCIDENTE_MAT_PEL))
        self.dlg.buttonEmergVarias.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_EMERGENCIAS_VARIAS))
        self.dlg.buttonRescateDeAltura.clicked.connect(lambda: self.call_sound(SONIDO_ALARMA_RESCATE_DE_ALTURA))

        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        self.dlg.buscarPunto.clicked.connect(lambda: self.toolActivatorStartPoints())
        self.dlg.volver.clicked.connect(lambda: self.backScreen())
        self.dlg.aceptar.clicked.connect(lambda: self.press_btn_acept())


    def press_btn_acept(self):
        self.savePoints()
        self.runAnalysis()

         

        
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

        self.vectorRubberBand.reset()
    ####
    def remove_bomba(self, id):
        # Borrar en la tabla interface
        i=0
        while i < self.dlg.tableWidget.rowCount():
            if int(self.dlg.tableWidget.item(i,0).text()) == id:
                self.dlg.tableWidget.removeRow(i)
            i += 1

        # Borrar en la BD
        delete('bomba', id)

    def update_bomba(self, id):
        try:
            i=0
            found = False
            while i < self.dlg.tableWidget.rowCount() and not found:
                if int(self.dlg.tableWidget.item(i,0).text()) == id:
                    found = True
                i += 1

            i = i-1
            if found:
                # Actualizar en la BD
                descripcion = self.dlg.tableWidget.item(i,1).text()
                estado = self.dlg.tableWidget.item(i,2).text()
                seters = " description = '{}', estado = '{}'".format(descripcion, estado)
                update('bomba', seters, id)
                QMessageBox.information(self.dlg, 'actualizar_bomba', "Actualizacion exitosa")
        except Exception as e:
            QgsMessageLog.logMessage(str(e))
            QMessageBox.warning(self.dlg, 'actualizar_bomba', "No se puede modificar el valor")

    def add_bombas(self, id, descripcion, estado):
        rowPosition = self.dlg.tableWidget.rowCount()
        self.dlg.tableWidget.insertRow(rowPosition)
        self.dlg.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(id)))
        self.dlg.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(descripcion))
        self.dlg.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(estado))
        delete_button = QPushButton("delete")
        delete_button.clicked.connect(lambda: self.remove_bomba(id))
        self.dlg.tableWidget.setCellWidget(rowPosition, 3, delete_button)
        update_bomba = QPushButton("update")
        update_bomba.clicked.connect(lambda: self.update_bomba(id))
        self.dlg.tableWidget.setCellWidget(rowPosition, 4, update_bomba)

    def changeScreenModBombas(self):
        self.dlg = OnlineRoutingMapperDialogModBombas()
        self.dlg.setFixedSize(self.dlg.size())
        self.dlg.show()
        self.dlg.tableWidget.setColumnCount(5)
        self.dlg.tableWidget.setHorizontalHeaderLabels(["ID", "Descripcion", "Estado", "Borrar", "Modificar"])
        registros = select('bomba')
        for tupla in registros:
            self.add_bombas(tupla[0], tupla[3], tupla[4])
        
        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        self.dlg.startBtn.clicked.connect(lambda: self.toolActivatorBombas())
        self.dlg.volver.clicked.connect(lambda: self.backScreen())
        self.dlg.aceptar.clicked.connect(lambda: self.saveBomba())

    def saveBomba(self):
        if len(self.dlg.bombaTxt.text()) > 0:
            if platform.system() == 'Windows':
                point = self.dlg.bombaTxt.text()
            else:
                pointsStart = self.dlg.bombaTxt.text().split(',')
                point = pointsStart[1]+','+pointsStart[0]
                
            #Inserta los puntos en la BD 
            startPoint = point.split(',')
            valores = "{}, {}, '{}'".format(startPoint[1], startPoint[0], self.dlg.descripcionTxt.text())
            insert('bomba', 'startPoint, stopPoint, description', valores)
        self.dlg = self.dlg_back
        self.dlg.show()
        if (self.dlg.close()):
            self.dlg.showNormal()
        self.agregar_actualizar_puntos_iniciales()


    #tupla esta de mas?
    def remove_points(self, id):
        # Borrar en la tabla interface
        i=0
        while i < self.dlg.tableWidget.rowCount():
            if int(self.dlg.tableWidget.item(i,0).text()) == id:
                self.dlg.tableWidget.removeRow(i)
            i += 1

        # Borrar en la BD
        delete('points', id)
        delete('points', id-1)
        self.agregar_actualizar_puntos_iniciales()

    def add_point(self, id, descripcion):
        rowPosition = self.dlg.tableWidget.rowCount()
        self.dlg.tableWidget.insertRow(rowPosition)
        self.dlg.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(id)))
        self.dlg.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(descripcion))
        delete_button = QPushButton("delete")
        delete_button.clicked.connect(lambda: self.remove_points(id))
        self.dlg.tableWidget.setCellWidget(rowPosition, 2, delete_button)

    def changeScreenModMapa(self):
        self.dlg = OnlineRoutingMapperDialogModMapa()
        self.dlg.setFixedSize(self.dlg.size())
        self.dlg.show()
        self.dlg.tableWidget.setColumnCount(3)
        self.dlg.tableWidget.setHorizontalHeaderLabels(["ID", "Descripcion", "Acción"])
        registros = select('points')
        i=1
        for tupla in registros:
            if i % 2 == 0:
                self.add_point(tupla[0], tupla[3])
            i+=1
        
        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        self.dlg.startBtn.clicked.connect(lambda: self.toolActivator(0))
        self.dlg.stopBtn.clicked.connect(lambda: self.toolActivator(1))
        self.dlg.volver.clicked.connect(lambda: self.backScreen())
        self.dlg.aceptar.clicked.connect(lambda: self.savePointsExclution())
        self.dlg.closeEvent = self.closeUpdate
    
    def update_pedido(self, id):
        try:
            i=0
            found = False
            while i < self.dlg.tableWidget.rowCount() and not found:
                if int(self.dlg.tableWidget.item(i,0).text()) == id:
                    found = True
                i += 1

            i = i-1
            if found:
                # Actualizar en la BD
                direccion = self.dlg.tableWidget.item(i,1).text()
                solicitante = self.dlg.tableWidget.item(i,2).text()
                telefono = self.dlg.tableWidget.item(i,3).text()
                operador = self.dlg.tableWidget.item(i,4).text()
                startPoint = self.dlg.tableWidget.item(i,5).text()
                stopPoint = self.dlg.tableWidget.item(i,6).text()
                descripcion = self.dlg.tableWidget.item(i,7).text()

                seters = "direccion = '{}', solicitante = '{}', telefono = '{}', operador = '{}', startPoint = '{}', stopPoint = '{}', description = '{}'".format(direccion, solicitante, telefono, operador, startPoint, stopPoint ,descripcion)
            
                update('pedido', seters, id)
        except Exception as e:
            QgsMessageLog.logMessage(str(e))
            QMessageBox.warning(self.dlg, 'actualizar_pedido', "No se puede modificar el valor por exceder de caracteres o tipo incorrecto")

    def add_pedido(self, id, direccion, solicitante, telefono, operador, coordenada_partida, coordenada_lugar, descripcion):
        rowPosition = self.dlg.tableWidget.rowCount()
        self.dlg.tableWidget.insertRow(rowPosition)
        item = QTableWidgetItem(str(id))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.dlg.tableWidget.setItem(rowPosition, 0, item)
        self.dlg.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(direccion)))
        self.dlg.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(str(solicitante)))
        self.dlg.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(str(telefono)))
        self.dlg.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(str(operador)))
        self.dlg.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(coordenada_partida))
        self.dlg.tableWidget.setItem(rowPosition, 6, QTableWidgetItem(str(coordenada_lugar)))
        self.dlg.tableWidget.setItem(rowPosition, 7, QTableWidgetItem(descripcion))
        update_button = QPushButton("Modificar")
        update_button.clicked.connect(lambda: self.update_pedido(id))
        self.dlg.tableWidget.setCellWidget(rowPosition, 8, update_button)
        

    def changeScreenVerPedidos(self):
        self.dlg = OnlineRoutingMapperDialogVerPedidos()
        self.dlg.setFixedSize(self.dlg.size())
        self.dlg.show()
        self.dlg.tableWidget.setColumnCount(9)
        self.dlg.tableWidget.setHorizontalHeaderLabels(["Numero ID", "Direccion", "Solicitante", "Telefono", "Operador", "Coordenada de partida", "Coordenada del lugar", "Descripcion", "Modificar"])
        #self.dlg.tableWidget.sortItems(0)
        
        self.cargar_pedidos_tabla()
        
        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        #self.dlg.buscarPunto.clicked.connect(lambda: self.toolActivatorStartPoints())

        self.dlg.volver.clicked.connect(lambda: self.backScreen())
        self.dlg.aceptar.clicked.connect(lambda: self.backScreen())
        self.dlg.cargar_planilla.clicked.connect(lambda: self.seleccionar_pedidos())
        self.dlg.cargar.clicked.connect(lambda: self.cargar_pedidos())
    
    def cargar_pedidos_tabla(self):
        registros = select("pedido")
        for tupla in registros:
            self.add_pedido(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7])

    def seleccionar_pedidos(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Archivos ODS (*.ods)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            selected_file_path = file_paths[0]
            self.dlg.cargar_planilla.setText(selected_file_path)
            self.path_planilla_carga = selected_file_path
            
            
    def cargar_pedidos(self):
        if self.path_planilla_carga is not None:
            cargar_pedidos(self.path_planilla_carga)
            self.cargar_pedidos_tabla()
            self.path_planilla_carga = None
            self.dlg.cargar_planilla.setText("Seleccionar archivo")


    def cargar_puntos_lista(self):
        registros = select('points')
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

            insertar_punto(startPoint[1], startPoint[0], self.dlg.descripcionTxt.text())
            insertar_punto(stopPoint[1], stopPoint[0], self.dlg.descripcionTxt.text())

        self.agregar_actualizar_puntos_iniciales()
        self.dlg = self.dlg_back
        self.dlg.show()

    def savePoints(self):
        try:
            descripcion = self.dlg.form_descripcion.text()
            direccion = self.dlg.form_direccion.text()
            solicitante = self.dlg.form_solicitante.text()
            telefono = self.dlg.form_telefono.text()
            #inserta los pedidos en la DB
            valores = "'{}', '{}', '{}', '{}', '{}', '{}', '{}'".format(direccion, solicitante, telefono, "Pedro", " ", " ", descripcion)
            insert('pedido', 'direccion, solicitante, telefono, operador, startpoint, stoppoint, description ', valores)
        
            self.calculate_points()
            self.tipoAutomovil = self.dlg.comboBox.currentText()
            self.dlg = self.dlg_back
            self.dlg.show()
            if(self.dlg.close()):
                self.dlg.showNormal()
        except Exception as e:
            QgsMessageLog.logMessage(str(e))
            QMessageBox.warning(self.dlg, 'actualizar_pedido', "No se puede modificar el valor por exceder de caracteres o tipo incorrecto")

    def backScreen(self):
        self.dlg = self.dlg_back
        self.dlg.show()
        if (self.dlg.close()):
            self.dlg.showNormal()
        self.agregar_actualizar_puntos_iniciales()

    def agregar_actualizar_puntos_iniciales(self):
        self.borrar_todos_los_puntos()
        registros = select('points')
        i=1
        points = []
        for tupla in registros:
            points.append(QgsPointXY(float(tupla[1]), float(tupla[2])))
            if i % 2 == 0:
                self.vectorRubberBand.addGeometry(QgsGeometry.fromPolygonXY([points]), None)
                points = []
                self.stopRubberBand.addPoint(QgsPointXY(float(tupla[1]), float(tupla[2])))
            else:
                self.startRubberBand.addPoint(QgsPointXY(float(tupla[1]), float(tupla[2])))
            i+=1

    def run(self):
        self.no = 0
        self.startPointXY = None
        self.stopPointXY = None
        createTablePoints()
        createTableBomba()
        createTablePedido()
        self.dlg = OnlineRoutingMapperDialog()
        
        self.dlg.setFixedSize(self.dlg.size())

        self.services = RouteProvider().services()
        # self.dlg.serviceCombo.addItems(list(self.services))

        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)  # clicktool instance generated in here.
        # self.dlg.startBtn.clicked.connect(lambda: self.toolActivator(0))
        # self.dlg.stopBtn.clicked.connect(lambda: self.toolActivator(1))
       
        
        self.dlg_back = self.dlg
        self.dlg.btnAgPedido.clicked.connect(lambda: self.changeScreenAgPedido())
        self.dlg.btnModMapa.clicked.connect(lambda: self.changeScreenModMapa())
        self.dlg.btnModBombas.clicked.connect(lambda: self.changeScreenModBombas())
        self.dlg.btn_ver_pedidos.clicked.connect(lambda: self.changeScreenVerPedidos())

        self.vectorRubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.vectorRubberBand.setColor(QColor("#000000"))
        self.vectorRubberBand.setWidth(4)

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
        self.canvas.scene().removeItem(self.vectorRubberBand)

    def closeUpdate(self, event):
        self.dlg_back.closeEvent = self.close
        self.agregar_actualizar_puntos_iniciales()