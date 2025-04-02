from collections import deque
import time
from solver import RisolutoreHanoi

class RisolutoreBRFS(RisolutoreHanoi):
    def __init__(self, num_dischi):
        super().__init__(num_dischi)
        self.tempo_inizio = None
        self.tempo_fine = None
        self.stati_esplorati = 0

    def risolvi(self):
        self.tempo_inizio = time.time()
        stato_iniziale = (tuple(range(self.num_dischi, 0, -1)), (), ())
        stato_obiettivo = ((), (), tuple(range(self.num_dischi, 0, -1)))
        
        coda = deque()
        coda.append((stato_iniziale, []))
        self.stati_visitati.add(stato_iniziale)
        
        while coda:
            self.stati_esplorati += 1
            stato, percorso = coda.popleft()
            
            if stato == stato_obiettivo:
                self.soluzione = percorso
                self.tempo_fine = time.time()
                self.stampa_statistiche()
                return
            
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
                        self.stati_visitati.add(nuovo_stato)
                        coda.append((nuovo_stato, percorso + [(da_piolo, a_piolo)]))

    def stampa_statistiche(self):
        tempo_impiegato = self.tempo_fine - self.tempo_inizio
        print(f"\n[Statistiche BRFS]")
        print(f"- Mosse trovate: {len(self.soluzione)}")
        print(f"- Mosse ottimali: {2**self.num_dischi - 1}")
        print(f"- Stati esplorati: {self.stati_esplorati}")
        print(f"- Tempo di esecuzione: {tempo_impiegato:.4f} secondi")