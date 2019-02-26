import FreeCAD, FreeCADGui, numpy
from FreeCAD import Gui
from PySide import QtGui, QtCore
from math import sqrt
#import Finestra

class ConfrontaOggettiInWidget():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  : str(FreeCAD.getHomePath() + "Mod/Measures/Resources/icons/ConfrontoFinestra.svg"), # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "My New Command",
                'ToolTip' : "Cerca informazioni sull'oggetto selezionato"}

    def Activated(self):
        "Do something here"
        FreeCAD.Console.PrintMessage("Premuto pulsante ConfrontaOggettiInWidget" + "\n")
		
        global WidgetAttivo, Widget
        WidgetAttivo = True
        
        Widget = QtGui.QDockWidget()     # create a new dockwidget
        Widget.setObjectName("widgetDiProva")
        
        centralwidget = FreeCADGui.PySideUic.loadUi(relazioniFinestraUI)
        InizializzaFinestra(centralwidget)
        Widget.setWidget(centralwidget)
        
        FCmw = FreeCADGui.getMainWindow()
        FCmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, Widget) # add the widget to the main window Right
		
        global s3

        s3 = SelObserver()
        FreeCADGui.Selection.addObserver(s3)
		
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return not WidgetAttivo

Gui.addCommand('ConfrontaOggettiInWidget', ConfrontaOggettiInWidget())

class ChiudiConfrontaOggettiInWidget():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  : str(FreeCAD.getHomePath() + "Mod/Measures/Resources/icons/ChiudiConfrontoFinestra.svg"), # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "My New Command",
                'ToolTip' : "Chiudi Widget confronta oggetti"}

    def Activated(self):
        "Do something here"
        FreeCAD.Console.PrintMessage("Premuto pulsante ChiudiConfrontaOggettiInWidget" + "\n")
		
        global WidgetAttivo, Widget
        WidgetAttivo = False
        
        Widget.hide()
        
        FreeCADGui.Selection.removeObserver(s3)
		
        return

    def IsActive(self):
        """Here you can defin
		e if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return WidgetAttivo

Gui.addCommand('ChiudiConfrontaOggettiInWidget', ChiudiConfrontaOggettiInWidget())

def DefinisciElemento():
    surfaceFace = Gui.Selection.getSelectionEx()[0].SubObjects[0].Area
    subObjectLength = Gui.Selection.getSelectionEx()[0].SubObjects[0].Length
    if (surfaceFace == 0):
        if (subObjectLength == 0):
            scritta = "Punto"
        else:
            scritta = "Linea"
    else:
        scritta = "Superficie"
    
    return scritta
        
def AnalizzaRelazioni(model):
    global primoElemento, secondoElemento, tipoPrimoElemento, tipoSecondoElemento
    model.clear()
    
    scritta = QtGui.QStandardItem("Relazioni tra: " + str(tipoPrimoElemento) + " e " + str(tipoSecondoElemento))
    
    model.appendRow(scritta)
    
    if (tipoPrimoElemento == "Punto") and (tipoSecondoElemento == "Punto"):
        scritta = QtGui.QStandardItem("Distanza = " + str(primoElemento.SubObjects[0].Vertexes[0].Point.distanceToPoint(secondoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)
    
    elif (tipoPrimoElemento == "Punto") and (tipoSecondoElemento == "Linea"):
        scritta = QtGui.QStandardItem("Distanza = " + str(DistanzaPuntoRetta(secondoElemento.SubObjects[0].Vertexes[0].Point, secondoElemento.SubObjects[0].Vertexes[1].Point, primoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)
	
    elif (tipoPrimoElemento == "Linea") and (tipoSecondoElemento == "Punto"):
        scritta = QtGui.QStandardItem("Distanza = " + str(DistanzaPuntoRetta(primoElemento.SubObjects[0].Vertexes[0].Point, primoElemento.SubObjects[0].Vertexes[1].Point, secondoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)
	
    elif (tipoPrimoElemento == "Linea") and (tipoSecondoElemento == "Linea"):
        scritta = QtGui.QStandardItem("Distanza = " + str(Distanza2RetteNelloSpazio(primoElemento.SubObjects[0].Vertexes[0].Point, primoElemento.SubObjects[0].Vertexes[1].Point, secondoElemento.SubObjects[0].Vertexes[0].Point, secondoElemento.SubObjects[0].Vertexes[1].Point)))
        model.appendRow(scritta)
        diff1 = primoElemento.SubObjects[0].Vertexes[0].Point - primoElemento.SubObjects[0].Vertexes[1].Point
        diff2 = secondoElemento.SubObjects[0].Vertexes[0].Point - secondoElemento.SubObjects[0].Vertexes[1].Point
        scritta = QtGui.QStandardItem("Angolo = " + str(AngoloTra2VettoriNelloSpazio(diff1, diff2)))
        model.appendRow(scritta)
        
    elif (tipoPrimoElemento == "Superficie") and (tipoSecondoElemento == "Punto"):
        scritta = QtGui.QStandardItem("Distanza = " + str(DistanzaPuntoPiano(primoElemento.SubObjects[0].Faces[0].normalAt(0,0), primoElemento.SubObjects[0].Vertexes[0].Point, secondoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)
    
    elif (tipoPrimoElemento == "Punto") and (tipoSecondoElemento == "Superficie"):
        scritta = QtGui.QStandardItem("Distanza = " + str(DistanzaPuntoPiano(secondoElemento.SubObjects[0].Faces[0].normalAt(0,0), secondoElemento.SubObjects[0].Vertexes[0].Point, primoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)

    elif (tipoPrimoElemento == "Superficie") and (tipoSecondoElemento == "Superficie"):
        scritta = QtGui.QStandardItem("Distanza = " + str(DistanzaPianoPiano(primoElemento.SubObjects[0].Faces[0].normalAt(0,0), primoElemento.SubObjects[0].Vertexes[0].Point, secondoElemento.SubObjects[0].Faces[0].normalAt(0,0), secondoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)
        scritta = QtGui.QStandardItem("Angolo = " + str(AngoloTra2VettoriNelloSpazio(primoElemento.SubObjects[0].Faces[0].normalAt(0,0), secondoElemento.SubObjects[0].Faces[0].normalAt(0,0))))
        model.appendRow(scritta)
        
    elif (tipoPrimoElemento == "Linea") and (tipoSecondoElemento == "Superficie"):
        scritta = QtGui.QStandardItem("Distanza = " + str(DistanzaRettaPiano(primoElemento.SubObjects[0].Vertexes[0].Point, primoElemento.SubObjects[0].Vertexes[1].Point, secondoElemento.SubObjects[0].Faces[0].normalAt(0,0), secondoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)
        scritta = QtGui.QStandardItem("Angolo = " + str(90 - AngoloTra2VettoriNelloSpazio(primoElemento.SubObjects[0].Vertexes[0].Point - primoElemento.SubObjects[0].Vertexes[1].Point, secondoElemento.SubObjects[0].Faces[0].normalAt(0,0))))
        model.appendRow(scritta)
        
    elif (tipoPrimoElemento == "Superficie") and (tipoSecondoElemento == "Linea"):
        scritta = QtGui.QStandardItem("Distanza = " + str(DistanzaRettaPiano(secondoElemento.SubObjects[0].Vertexes[0].Point, secondoElemento.SubObjects[0].Vertexes[1].Point, primoElemento.SubObjects[0].Faces[0].normalAt(0,0), primoElemento.SubObjects[0].Vertexes[0].Point)))
        model.appendRow(scritta)
        scritta = QtGui.QStandardItem("Angolo = " + str(90 - AngoloTra2VettoriNelloSpazio(secondoElemento.SubObjects[0].Vertexes[0].Point - secondoElemento.SubObjects[0].Vertexes[1].Point, primoElemento.SubObjects[0].Faces[0].normalAt(0,0))))
        model.appendRow(scritta)


def DistanzaPuntoRetta(A, B, P):
    "Distanza tra una retta passante per i punti A e B un il punto P"
    "Fonte: https://math.stackexchange.com/questions/1905533/find-perpendicular-distance-from-point-to-line-in-3d"
    d = numpy.linalg.norm(numpy.cross(B - P, B - A)) / numpy.linalg.norm(B - A)
    return d

def DistanzaPuntoPiano(V, A, P):
    "V = vettore normale del piano, A = punto appartenente al piano, P = punto su cui calcolare la distanza"
    "Distanza tra un piano di vettore V passante per A e un punto P"
    "Fonte: http://mathworld.wolfram.com/Point-PlaneDistance.html"
    d = numpy.dot(V, P-A) / numpy.linalg.norm(V)
    return d

def Distanza2RetteNelloSpazio(A0, A1, B0, B1):
    "A0, A1 = punti appartenenti alla prima retta, B0, B1 = punti appartenenti alla seconda retta"
    if (numpy.linalg.norm(numpy.cross(A1 - A0, B1 - B0)) != 0):
        d =  numpy.dot(B0 - A0, numpy.cross(A1 - A0, B1 - B0)) / numpy.linalg.norm(numpy.cross(A1 - A0, B1 - B0))
    else:
        d = DistanzaPuntoRetta(A0, A1, B0)
    return d

def AngoloTra2VettoriNelloSpazio(V1, V2):
    "restituisce l'angolo formato da due vettori. Fonte algoritmo: https://www.youmath.it/lezioni/algebra-lineare/matrici-e-vettori/882-norma-e-prodotto-scalare.html"
    
    ProdottoVettoriale = numpy.vdot(V1, V2)
    normV1 = numpy.linalg.norm(V1)
    normV2 = numpy.linalg.norm(V2)
    
    cosenoAngolo = ProdottoVettoriale / (normV1 * normV2)
    
    AngoloRadianti = (numpy.pi/2) - numpy.arcsin(cosenoAngolo)
    
    AngoloGradi = AngoloRadianti *180/numpy.pi
    
    return numpy.round(AngoloGradi, 3)

def DistanzaPianoPiano(V1, A1, V2, A2):
    "V1 = vettore normale del primo piano, A1 = punto appartenente al primo piano, V2 = vettore normale del secondo piano, A2 = punto appartenente al secondo piano,"
    if (numpy.linalg.norm(numpy.cross(V1, V2)) != 0): # Se i vettori non sono paralleli
        d =  0
    else:
        d = DistanzaPuntoPiano(V1, A1, A2)
    return d

def DistanzaRettaPiano(A0, A1, V, P):
    if (numpy.dot(A1 - A0, V) != 0): # Se i vettori non sono paralleli
        d =  0
    else:
        d = DistanzaPuntoPiano(V, P, A0)
    return d

def InizializzaFinestra(finestra):
	global modelRelazioni

	modelRelazioni = QtGui.QStandardItemModel()
	
	finestra.listViewRelazioni.setModel(modelRelazioni)

class WidgetSelezionaOggetto:
    def __init__(self):
        # this will create a Qt widget from our ui file
        self.form = FreeCADGui.PySideUic.loadUi(relazioniFinestraUI)
        self.form.setObjectName("Nome di Prova")
        self.form.setWindowTitle("Seleziona 2 elementi")

    def setupUi(self): 
        self.centralWidget = QtGui.QWidget(self.form)
        self.centralWidget.setObjectName("centralWidget")

class SelObserver:
	def __init__(self):
		self.numeroElemento = 0

	def setPreselection(self,doc,obj,sub):                # Preselection object
		#App.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
		pass

	def addSelection(self,doc,obj,sub,pnt):
		# Selection object
		#App.Console.PrintMessage("addSelection"+ "\n")
		#App.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
		#FreeCAD.Console.PrintMessage("Aggiunto elemento: " + str(obj) + "\n")
		if (self.numeroElemento == 0):
			global primoElemento, tipoPrimoElemento
			primoElemento = FreeCADGui.Selection.getSelectionEx()[0]
			tipoPrimoElemento = DefinisciElemento()
			FreeCAD.Console.PrintMessage("Aggiunto elemento alla prima lista: " + str(sub) + "\n")
			self.numeroElemento = 1
		else:
			global secondoElemento, tipoSecondoElemento
			secondoElemento = FreeCADGui.Selection.getSelectionEx()[0]
			tipoSecondoElemento = DefinisciElemento()
			FreeCAD.Console.PrintMessage("Aggiunto elemento alla seconda lista: " + str(sub) + "\n")
			self.numeroElemento = 0
        
		global modelRelazioni
		AnalizzaRelazioni(modelRelazioni)
		#App.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
		#App.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object
		#App.Console.PrintMessage("______"+ "\n")

	def removeSelection(self,doc,obj,sub):                # Delete the selected object
		#App.Console.PrintMessage("removeSelection"+ "\n")
		pass
	
	def setSelection(self,doc):                           # Selection in ComboView
		#App.Console.PrintMessage("setSelection"+ "\n")
		pass
	
	def clearSelection(self,doc):                         # If click on the screen, clear the selection
		#App.Console.PrintMessage("clearSelection"+ "\n")  # If click on another object, clear the previous object
		pass

relazioniFinestraUI = str(FreeCAD.getHomePath() + "Mod/Measures/Resources/ui/relazioniFinestrav2.ui")
WidgetAttivo = False
primoElemento = None
secondoElemento = None
tipoPrimoElemento = None
tipoSecondoElemento = None
