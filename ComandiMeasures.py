import FreeCAD, FreeCADGui
from FreeCAD import Gui
from PySide import QtGui, QtCore
#import Finestra

class SelezionaOggetto():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  : str(FreeCAD.getHomePath() + "Mod/Measures/Resources/icons/Confronto.svg"), # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "My New Command",
                'ToolTip' : "Cerca informazioni sull'oggetto selezionato"}

    def Activated(self):
        "Do something here"
        FreeCAD.Console.PrintMessage("Premuto pulsante Seleziona Oggetto" + "\n")
		
        global Pannello
        Pannello = PannelloSelezionaOggetto()
		
        InizializzaFinestra(Pannello.form)

        FreeCADGui.Control.showDialog(Pannello)

        global s1

        s1 = SelObserver()
        FreeCADGui.Selection.addObserver(s1)
		
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand('SelezionaOggetto', SelezionaOggetto()) 

class ConfrontaOggettiInFinestra():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  : str(FreeCAD.getHomePath() + "Mod/Measures/Resources/icons/ConfrontoFinestra.svg"), # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "My New Command",
                'ToolTip' : "Cerca informazioni sull'oggetto selezionato"}

    def Activated(self):
        "Do something here"
        FreeCAD.Console.PrintMessage("Premuto pulsante ConfrontaOggettiInFinestra" + "\n")
		
        global finestraAttiva, Finestra
        finestraAttiva = True
        
        Finestra = FreeCADGui.PySideUic.loadUi(relazioniFinestraUI)
        InizializzaFinestra(Finestra)
		
        Finestra.show()
		
        global s2

        s2 = SelObserver()
        FreeCADGui.Selection.addObserver(s2)
		
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return not finestraAttiva

Gui.addCommand('ConfrontaOggettiInFinestra', ConfrontaOggettiInFinestra())

class ChiudiConfrontaOggettiInFinestra():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  : str(FreeCAD.getHomePath() + "Mod/Measures/Resources/icons/ChiudiConfrontoFinestra.svg"), # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "My New Command",
                'ToolTip' : "Chiudi finestra confronta oggetti"}

    def Activated(self):
        "Do something here"
        FreeCAD.Console.PrintMessage("Premuto pulsante ChiudiConfrontaOggettiInFinestra" + "\n")
		
        global finestraAttiva, Finestra
        finestraAttiva = False
        
        Finestra.hide()
        
        FreeCADGui.Selection.removeObserver(s2)
		
        return

    def IsActive(self):
        """Here you can defin
		e if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return finestraAttiva

Gui.addCommand('ChiudiConfrontaOggettiInFinestra', ChiudiConfrontaOggettiInFinestra())

def AggiungiElemento(elemento, model):
	oggetto = QtGui.QStandardItem(elemento)
	model.clear()
	model.appendRow(oggetto)

def AnalizzaElemento(model):
    model.clear()
    try:
        SubElement = FreeCADGui.Selection.getSelectionEx()                                        # sub element name with getSelectionEx()
        subElementName = Gui.Selection.getSelectionEx()[0].SubElementNames[0]                     # sub element name with getSelectionEx()
        scritta = QtGui.QStandardItem("subElementName : " + str(subElementName))
        model.appendRow(scritta)
        
        subObjectLength = Gui.Selection.getSelectionEx()[0].SubObjects[0].Length                  # sub element Length
        scritta = QtGui.QStandardItem("subObjectLength: " + str(subObjectLength))
        model.appendRow(scritta)
		
        contatore = 0
        for vertice in Gui.Selection.getSelectionEx()[0].SubObjects[0].Vertexes:
            scritta = QtGui.QStandardItem("Punto " + str(contatore) + "   : " + str(vertice.Point))
            model.appendRow(scritta)
            contatore = contatore + 1

        subObjectBoundBox = Gui.Selection.getSelectionEx()[0].SubObjects[0].BoundBox              # sub element BoundBox coordinates
        scritta = QtGui.QStandardItem("subObjectBBox  : " + str(subObjectBoundBox))
        model.appendRow(scritta)

        subObjectBoundBoxCenter = Gui.Selection.getSelectionEx()[0].SubObjects[0].BoundBox.Center # sub element BoundBoxCenter
        scritta = QtGui.QStandardItem("subObjectBBoxCe: " + str(subObjectBoundBoxCenter))
        model.appendRow(scritta)

        surfaceFace = Gui.Selection.getSelectionEx()[0].SubObjects[0].Area                        # Area of the face selected
        scritta = QtGui.QStandardItem("surfaceFace    : " + str(surfaceFace))
        model.appendRow(scritta)
    except:
        scritta = QtGui.QStandardItem("errore nella selezione dell'oggetto")
        model.appendRow(scritta)
	
def InizializzaFinestra(finestra):
	global modelPrimo, modelSecondo, modelPropPrimo, modelPropSecondo, modelRelazioni

	modelPrimo = QtGui.QStandardItemModel()
	modelSecondo = QtGui.QStandardItemModel()
	modelPropPrimo = QtGui.QStandardItemModel()
	modelPropSecondo = QtGui.QStandardItemModel()
	modelRelazioni = QtGui.QStandardItemModel()
	
	finestra.listViewPrimoElemento.setModel(modelPrimo)
	finestra.listViewSecondoElemento.setModel(modelSecondo)
	finestra.listViewPropPrimoElemento.setModel(modelPropPrimo)
	finestra.listViewPropSecondoElemento.setModel(modelPropSecondo)
	finestra.listViewRelazioni.setModel(modelRelazioni)

class PannelloSelezionaOggetto:
    def __init__(self):
        # this will create a Qt widget from our ui file
        self.form = FreeCADGui.PySideUic.loadUi(relazioniFinestraUI)
        self.form.setObjectName("Nome di Prova")
        self.form.setWindowTitle("Sezionona 2 elementi")

    def accept(self):
        FreeCAD.Console.PrintMessage("Accettato" + "\n")
        FreeCADGui.Selection.removeObserver(s1)
        FreeCADGui.Control.closeDialog()
		
    def reject(self):
        FreeCAD.Console.PrintMessage("Rifiutato" + "\n")
        FreeCADGui.Selection.removeObserver(s1)
        FreeCADGui.Control.closeDialog()

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
			global modelPrimo, modelPropPrimo
			AggiungiElemento(str(obj), modelPrimo)
			AnalizzaElemento(modelPropPrimo)
			FreeCAD.Console.PrintMessage("Aggiunto elemento alla prima lista: " + str(sub) + "\n")
			self.numeroElemento = 1
		else:
			global modelSecondo,modelPropSecondo
			AggiungiElemento(str(obj), modelSecondo)
			AnalizzaElemento(modelPropSecondo)
			FreeCAD.Console.PrintMessage("Aggiunto elemento alla seconda lista: " + str(sub) + "\n")
			self.numeroElemento = 0
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

relazioniFinestraUI = str(FreeCAD.getHomePath() + "Mod/Measures/Resources/ui/relazioniFinestra.ui")
finestraAttiva = False