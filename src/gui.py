import pygame
from brfs import RisolutoreBRFS
from astar import RisolutoreAStar
from dfs import RisolutoreDFS
from bfs import RisolutoreBFS

class InterfacciaHanoi:
    def __init__(self, num_dischi=5, algoritmo='astar', euristica='base'):
        self.num_dischi = num_dischi
        self.algoritmo = algoritmo
        self.euristica = euristica if algoritmo in ['astar', 'bfs'] else None
        self.risolutore = None
        self.inizializza_pygame()
        self.reimposta_gioco()
        
    def inizializza_pygame(self):
        pygame.init()
        self.larghezza, self.altezza = 1000, 700
        self.schermo = pygame.display.set_mode((self.larghezza, self.altezza))
        pygame.display.set_caption(f"Torre di Hanoi - {self.num_dischi} Dischi ({self.algoritmo.upper()})")
        self.orologio = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Colori e dimensioni
        self.colore_pioli = (139, 69, 19)
        self.colori_dischi = [
            (255, 50, 50), (255, 120, 0), (255, 200, 0),
            (200, 220, 0), (100, 200, 50), (0, 180, 120),
            (0, 150, 200), (0, 80, 220), (120, 0, 200),
            (180, 0, 160)
        ]
        self.colore_sfondo = (240, 240, 240)
        self.colore_testo = (0, 0, 0)
        self.altezza_disco = 15
        self.altezza_base = 20
        self.larghezza_piolo = 20
    
    def reimposta_gioco(self):
        self.pioli = [self.crea_piolo(i) for i in range(3)]
        self.piolo_selezionato = None
        self.mosse = 0
        self.gioco_terminato = False
        self.risoluzione_automatica = False
        self.mosse_soluzione = []
        self.indice_mossa = 0
        
        # Inizializza dischi sul primo piolo
        for i in range(self.num_dischi, 0, -1):
            self.pioli[0]['dischi'].append(self.crea_disco(i))
    
    def crea_piolo(self, indice):
        fattore_spaziatura = max(4, 3 + 0.1 * self.num_dischi)
        pos_x = (indice + 1) * self.larghezza / fattore_spaziatura
        return {
            'x': pos_x,
            'dischi': [],
            'rettangolo': pygame.Rect(
                pos_x - self.larghezza_piolo//2, 
                self.altezza//2, 
                self.larghezza_piolo, 
                self.altezza//2 - self.altezza_base
            )
        }
    
    def crea_disco(self, dimensione):
        larghezza_max = self.larghezza / 4
        larghezza_min = 40
        larghezza = larghezza_min + (larghezza_max - larghezza_min) * (dimensione / self.num_dischi)**0.7
        return {
            'dimensione': dimensione,
            'larghezza': larghezza,
            'colore': self.colori_dischi[dimensione % len(self.colori_dischi)]
        }
    
    def esegui(self):
        esecuzione = True
        while esecuzione:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esecuzione = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1 and not self.risoluzione_automatica:
                        self.gestisci_click(evento.pos)
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        self.reimposta_gioco()
                    elif evento.key == pygame.K_s and not self.risoluzione_automatica:
                        self.avvia_risoluzione_automatica()
            
            if self.risoluzione_automatica:
                self.passo_risoluzione_automatica()
            
            self.disegna()
            pygame.display.flip()
            self.orologio.tick(60)
        
        pygame.quit()
    
    def gestisci_click(self, pos):
        for i, piolo in enumerate(self.pioli):
            if abs(pos[0] - piolo['x']) < 100 and pos[1] < self.altezza - self.altezza_base:
                if self.piolo_selezionato is None:
                    if piolo['dischi']:
                        self.piolo_selezionato = i
                else:
                    if self.piolo_selezionato != i:
                        self.muovi_disco(self.piolo_selezionato, i)
                    self.piolo_selezionato = None
    
    def muovi_disco(self, da_piolo, a_piolo):
        piolo_partenza = self.pioli[da_piolo]
        piolo_arrivo = self.pioli[a_piolo]
        
        if piolo_partenza['dischi']:
            if not piolo_arrivo['dischi'] or piolo_partenza['dischi'][-1]['dimensione'] < piolo_arrivo['dischi'][-1]['dimensione']:
                disco = piolo_partenza['dischi'].pop()
                piolo_arrivo['dischi'].append(disco)
                self.mosse += 1
                
                if len(self.pioli[2]['dischi']) == self.num_dischi:
                    self.gioco_terminato = True
    
    def avvia_risoluzione_automatica(self):
        self.risolutore = self.ottieni_risolutore()
        self.risolutore.risolvi()
        self.mosse_soluzione = self.risolutore.ottieni_mosse()
        self.risoluzione_automatica = True
        self.indice_mossa = 0
    
    def ottieni_risolutore(self):
        if self.algoritmo == 'brfs':
            return RisolutoreBRFS(self.num_dischi)
        elif self.algoritmo == 'astar':
            return RisolutoreAStar(self.num_dischi, euristica=self.euristica if self.euristica is not None else 'base')
        elif self.algoritmo == 'dfs':
            return RisolutoreDFS(self.num_dischi)
        elif self.algoritmo == 'bfs':
            return RisolutoreBFS(self.num_dischi, euristica=self.euristica if self.euristica else 'base')
        else:
            return RisolutoreAStar(self.num_dischi)
    
    def passo_risoluzione_automatica(self):
        if self.indice_mossa < len(self.mosse_soluzione):
            da_piolo, a_piolo = self.mosse_soluzione[self.indice_mossa]
            self.muovi_disco(da_piolo, a_piolo)
            self.indice_mossa += 1
        else:
            self.risoluzione_automatica = False
    
    def disegna(self):
        self.schermo.fill(self.colore_sfondo)
        
        # Disegna titolo e informazioni
        titolo = self.font.render(
            f"Torre di Hanoi - {self.num_dischi} Dischi ({self.algoritmo.upper()})", 
            True, self.colore_testo
        )
        self.schermo.blit(titolo, (self.larghezza//2 - titolo.get_width()//2, 20))
        
        testo_mosse = self.font.render(
            f"Mosse: {self.mosse} (Ottimali: {2**self.num_dischi-1})", 
            True, self.colore_testo
        )
        self.schermo.blit(testo_mosse, (self.larghezza//2 - testo_mosse.get_width()//2, 50))
        
        if hasattr(self, 'risolutore') and self.risolutore:
            testo_stati = self.font.render(
                f"Stati esplorati: {self.risolutore.stati_esplorati}", 
                True, self.colore_testo
            )
            self.schermo.blit(testo_stati, (self.larghezza//2 - testo_stati.get_width()//2, 80))
        
        # Disegna istruzioni
        istruzioni = [
            "Clicca sui pioli per muovere i dischi",
            "Premi R per resettare",
            "Premi S per risoluzione automatica"
        ]
        
        for i, testo in enumerate(istruzioni):
            superficie_testo = self.font.render(testo, True, self.colore_testo)
            self.schermo.blit(superficie_testo, (20, 120 + i * 30))
        
        # Disegna pioli e dischi
        for piolo in self.pioli:
            self.disegna_piolo(piolo)
        
        # Evidenzia piolo selezionato
        if self.piolo_selezionato is not None:
            piolo = self.pioli[self.piolo_selezionato]
            pygame.draw.rect(
                self.schermo, (0, 255, 0), 
                (piolo['x'] - 100, 150, 200, self.altezza - 150 - self.altezza_base), 
                2
            )
        
        # Messaggio fine gioco
        if self.gioco_terminato:
            testo_fine = self.font.render(
                "Complimenti! Puzzle risolto!", True, (0, 128, 0)
            )
            self.schermo.blit(
                testo_fine, 
                (self.larghezza//2 - testo_fine.get_width()//2, 110)
            )
    
    def disegna_piolo(self, piolo):
        # Disegna asta del piolo
        pygame.draw.rect(self.schermo, self.colore_pioli, piolo['rettangolo'])
        
        # Disegna base
        pygame.draw.rect(
            self.schermo, self.colore_pioli,
            (piolo['x'] - 100, self.altezza - self.altezza_base, 200, self.altezza_base)
        )
        
        # Disegna dischi
        for i, disco in enumerate(piolo['dischi']):
            rettangolo_disco = pygame.Rect(
                piolo['x'] - disco['larghezza']//2,
                self.altezza - self.altezza_base - (i+1) * self.altezza_disco,
                disco['larghezza'],
                self.altezza_disco
            )
            pygame.draw.rect(self.schermo, disco['colore'], rettangolo_disco, border_radius=5)
            pygame.draw.rect(self.schermo, (0, 0, 0), rettangolo_disco, 1, border_radius=5)