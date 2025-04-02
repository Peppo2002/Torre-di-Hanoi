import sys
import time
from solver import RisolutoreHanoi

sys.setrecursionlimit(5000)

class RisolutoreDFS(RisolutoreHanoi):
    def __init__(self, num_dischi):
        super().__init__(num_dischi)
        self.tempo_inizio = None
        self.tempo_fine = None
        self.stati_esplorati = 0
    
    def risolvi(self):
        self.tempo_inizio = time.time()
        stato_iniziale = (tuple(range(self.num_dischi, 0, -1)), (), ())
        stato_obiettivo = ((), (), tuple(range(self.num_dischi, 0, -1)))
        self._dfs(stato_iniziale, [], stato_obiettivo)
        self.tempo_fine = time.time()
        self.stampa_statistiche()
    
    def _dfs(self, stato, percorso, stato_obiettivo):
        self.stati_esplorati += 1
        
        if stato == stato_obiettivo:
            self.soluzione = percorso
            return True
        
        self.stati_visitati.add(stato)
        
        for da_piolo in range(3):
            if not stato[da_piolo]:
                continue
            
            for a_piolo in range(3):
                if da_piolo == a_piolo:
                    continue
                
                if stato[a_piolo] and stato[da_piolo][-1] > stato[a_piolo][-1]:
                    continue
                
                nuovo_stato = self.muovi_disco(stato, da_piolo, a_piolo)
                if nuovo_stato not in self.stati_visitati:
                    if self._dfs(nuovo_stato, percorso + [(da_piolo, a_piolo)], stato_obiettivo):
                        return True
        return False

    def stampa_statistiche(self):
        tempo_impiegato = self.tempo_fine - self.tempo_inizio
        print(f"\n[Statistiche DFS]")
        print(f"- Mosse trovate: {len(self.soluzione)}")
        print(f"- Mosse ottimali: {2**self.num_dischi - 1}")
        print(f"- Stati esplorati: {self.stati_esplorati}")
        print(f"- Tempo di esecuzione: {tempo_impiegato:.4f} secondi")