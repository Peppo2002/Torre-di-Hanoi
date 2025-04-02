class RisolutoreHanoi:
    def __init__(self, num_dischi):
        self.num_dischi = num_dischi
        self.stati_visitati = set()
        self.soluzione = []
    
    def risolvi(self):
        raise NotImplementedError("Le sottoclassi devono implementare risolvi()")
    
    def ottieni_mosse(self):
        return self.soluzione
    
    @staticmethod
    def stato_a_tupla(stato):
        return tuple(tuple(piolo) for piolo in stato)
    
    @staticmethod
    def muovi_disco(stato, da_piolo, a_piolo):
        nuovo_stato = [list(piolo) for piolo in stato]
        disco = nuovo_stato[da_piolo].pop()
        nuovo_stato[a_piolo].append(disco)
        return tuple(tuple(piolo) for piolo in nuovo_stato)