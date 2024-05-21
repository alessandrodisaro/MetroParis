import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._fermataPartenza = None
        self._fermataArrivo = None

    def handleCreaGrafo(self,e):
        self._model.buildGraph()
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        #self._view.lst_results.clean()
        self._view.lst_result.controls.append(ft.Text(f"Il grafo e' stato creato correttamente"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {nEdges} archi"))

        self._view.lst_result.controls.append(ft.Text())
        self._view._btnCalcola.disabled = False # RIABILITO il bottono dopo aver creato il grafo
        self._view.update_page()

    def handleCreaGrafoPesato(self, e):
        self._model.buildGraphPesato()
        nNodes = self._model.getNumNodes()
        nEdges = self._model.getNumEdges()
        archiPesoMaggiore = self._model.getArchiPesoMaggiore()

        self._view.lst_result.clean()
        self._view.lst_result.controls.append(ft.Text("Grafo pesato correttamente creato"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi e {nEdges} archi"))
        for a in archiPesoMaggiore:
            self._view.lst_result.controls.append(ft.Text(a))
        self._view._btnCalcolaPercorso.disabled = False  # RIABILITO il bottono dopo aver creato il grafo
        self._view._btnCalcola.disabled = False
        self._view.update_page()





    def handleCercaRaggiungibili(self,e):

       # visited = self._model.getBSFNodes(self._fermataPartenza)
        visited = self._model.getDFSNodes(self._fermataPartenza)
        self._view.lst_result.clean()
        self._view.lst_result.controls.append(ft.Text(f"Da {self._fermataPartenza} posso raggiungere {len(visited)} satzioni: " ))
        for stazione in visited:
            self._view.lst_result.controls.append(ft.Text(stazione))
        self._view.update_page()


    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def handlePercorso(self, e):
        if self._fermataArrivo is None or self._fermataArrivo is None:
            self._view.lst_result.clean()
            self._view.lst_result.controls.append(ft.Text("Attenzione, selezionare le due fermate"))
            self._view.update_page()
        v0 = self._fermataPartenza
        v1 = self._fermataArrivo
        totTime, path = self._model.getBestPath(v0, v1)
        if path == []:
            self._view.lst_result.clean()
            self._view.lst_result.controls.append(ft.Text("Percorso no trovato"))
            self._view.update_page()
            return
        self._view.lst_result.clean()
        self._view.lst_result.controls.append(ft.Text("Percorso trovato"))
        self._view.lst_result.controls.append(ft.Text(f"Il cammino piu' breve fra "
                                                      f"{self._fermataPartenza} e"
                                                      f"{self._fermataArrivo} "
                                                      f"impiega {totTime} minuti"))
        for node in path:
            self._view.lst_result.controls.append(ft.Text(f"{node}"))
        self._view.update_page()


    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
