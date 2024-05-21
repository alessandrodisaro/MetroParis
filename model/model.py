from geopy import distance

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        # aggiungo tutti i nodi (fermate al grafo)
        self._grafo.add_nodes_from(self._fermate)
        #  creo il dizionario per l id_fermate e un oggetto fermate vero e proprio
        self._id_map = {}
        # key = id_fermata ; value = oggetto Fermata
        for fermata in self._fermate:
            self._id_map[fermata.id_fermata] = fermata
        self._linee = DAO.getAllLinee()
        self._lineaMap = {}
        for l in self._linee:
            self._lineaMap[l.id_linea] = l
    def getBSFNodes(self, source):
        edges = nx.bfs_edges(self._grafo, source)  # breadth first = cerchi concentrici
        print(edges)
        visited = []
        for u, v in edges:
            visited.append(v)  # appendo i nodi target , che sonon tutti quelli visitati
        return visited

    def getDFSNodes(self, source):
        edges = nx.dfs_edges(self._grafo, source)  # depth first = come la ricorsione con backtracikng
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def addEdgesPesati(self):
        self._grafo.clear_edges()
        allConnesioni = DAO.getAllConnessioni()
        for c in allConnesioni:
            v0 = self._id_map[c.id_stazP]
            v1 = self._id_map[c.id_stazA]

            linea = self._lineaMap[c.id_linea]
            peso = self.getTraversalTime(v0, v1, linea)
            if self._grafo.has_edge(v0, v1):
                if self._grafo[v0][v1]["weight"] > peso:
                    self._grafo[v0][v1]["weight"] = peso
            else:
                self._grafo.add_edge(v0, v1, weight=peso)
        #     if self._grafo.has_edge(self._id_map[c.id_stazP], self._id_map[c.id_stazA]):
        #         self._grafo[self._id_map[c.id_stazP]][self._id_map[c.id_stazA]]["weight"] += 1
        #     else:
        #         self._grafo.add_edge(self._id_map[c.id_stazP], self._id_map[c.id_stazA], weight=1)

    def getEdgeWeight(self, v1, v2):
        # mi dice il peso dell arco tra due nodi
        return self._grafo[v1][v2]["weight"]

    def getArchiPesoMaggiore(self):
        if len(self._grafo.edges) == 0:
            print("Il grafo e' vuoto")
            return

        edges = self._grafo.edges
        result = []

        for u, v in edges:
            peso = (self._grafo[u][v]["weight"])
            if peso > 1:
                result.append((u, v, peso))

        return result

    def buildGraph(self):
        self._grafo.clear()

        # MODE 1 doppio loop su nodi e query per ogni arco
        # for nodo_part in self._fermate:
        #     for nodo_arr in self._fermate:
        #         result = DAO.getEdge(nodo_part, nodo_arr)
        #         if len(result) > 0:
        #             self._grafo.add_edge(nodo_part, nodo_arr)
        #             print(f"added edge tra {nodo_arr} e {nodo_arr}")

        # MODE 2 ciclo una voltaq sola su tutti i nodi e vedo tutti nodi connessi ad esso
        # for nodo_par in self._fermate:
        #     vicini = DAO.getEdegsVicini(nodo_par)
        #     for vicino in vicini:
        #         # prendo il valore dell' oggetto fermata di chiave _id_stazA
        #         vicino_nodo = self._id_map[vicino.id_stazA]
        #         self._grafo.add_edge(nodo_par, vicino_nodo)
        #         print(f"aggiunto arco tra {nodo_par} e {vicino_nodo}")

        # MODE 3 query che ritorna gia' tutte le connessioni
        allConnessioni = DAO.getAllConnessioni()
        for c in allConnessioni:
            p_nodo = self._id_map[c.id_stazP]
            a_nodo = self._id_map[c.id_stazA]
            self._grafo.add_edge(p_nodo, a_nodo)
            print(f"arco aggiunto tra {p_nodo} e {a_nodo}")

    @property
    def fermate(self):
        return self._fermate

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getTraversalTime(self, v0, v1, linea):
        vel = linea.velocita
        p0 = (v0.coordX, v0.coordY)
        p1 = (v1.coordX, v1.coordY)
        dist = distance.distance(p0, p1).km
        tempo = (dist / vel) * 60  # in minuti
        return tempo

    def getBestPath(self, v0, v1):
        costoTot, path = nx.single_source_dijkstra(self._grafo, v0, v1)
        return costoTot, path

