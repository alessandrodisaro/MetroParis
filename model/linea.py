from dataclasses import dataclass

@dataclass
class Linea:
    id_linea: int
    nome: str
    velocita: float
    intervallo: float
    colore: str

    def __hash__(self):
        return hash(self.id_linea)  # ma potrebbe non servire perche viene usata solo se siano nodi del nostro garfo


