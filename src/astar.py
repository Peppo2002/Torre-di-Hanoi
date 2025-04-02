import heapq
import time
from solver import RisolutoreHanoi
from heuristics import EuristicheHanoi

class RisolutoreAStar(RisolutoreHanoi):
    def __init__(self, num_dischi, euristica='base'):
        super().__init__(num_dischi)
        self.stati_visitati = {}
        self.nome_euristica = euristica if euristica is not None else 'base'
        self.funzione_euristica = EuristicheHanoi.ottieni(self.nome_euristica)
        self.tempo_inizio = None
        self.tempo_fine = None
        self.stati_esplorati = 0

    def risolvi(self):
        self.tempo_inizio = time.time()
        stato_iniziale = (tuple(range(self.num_dischi, 0, -1)), (), ())
        stato_obiettivo = ((), (), tuple(range(self.num_dischi, 0, -1)))
        
        coda_priorita = []
        heapq.heappush(coda_priorita, (
            self.funzione_euristica(stato_iniziale, self.num_dischi),
            0,
            stato_iniziale,
            []
        ))
        self.stati_visitati[stato_iniziale] = 0
        
        while coda_priorita:
            self.stati_esplorati += 1
            _, costo, stato, percorso = heapq.heappop(coda_priorita)
            
            if stato == stato_obiettivo:
                self.soluzione = percorso
                self.tempo_fine = time.time()
                self.stampa_statistiche()
                return
            
            if costo > self.stati_visitati.get(stato, float('inf')):
                continue
                
            for da_piolo in range(3):
                if not stato[da_piolo]:
                    continue
                
                for a_piolo in range(3):
                    if da_piolo == a_piolo:
                        continue
                    
                    if stato[a_piolo] and stato[da_piolo][-1] > stato[a_piolo][-1]:
                        continue
                    
                    nuovo_stato = self.muovi_disco(stato, da_piolo, a_piolo)
                    nuovo_costo = costo + 1
                    
                    if nuovo_stato not in self.stati_visitati or nuovo_costo < self.stati_visitati[nuovo_stato]:
                        self.stati_visitati[nuovo_stato] = nuovo_costo
                        priorita = nuovo_costo + self.funzione_euristica(nuovo_stato, self.num_dischi)
                        heapq.heappush(coda_priorita, (priorita, nuovo_costo, nuovo_stato, percorso + [(da_piolo, a_piolo)]))

    def stampa_statistiche(self):
        tempo_impiegato = self.tempo_fine - self.tempo_inizio
        print(f"\n[Statistiche A*]")
        print(f"- Euristica usata: {self.nome_euristica}")
        print(f"- Mosse trovate: {len(self.soluzione)}")
        print(f"- Mosse ottimali: {2**self.num_dischi - 1}")
        print(f"- Stati esplorati: {self.stati_esplorati}")
        print(f"- Tempo di esecuzione: {tempo_impiegato:.4f} secondi")