import argparse
from gui import InterfacciaHanoi

def main():
    parser = argparse.ArgumentParser(description="Gioco della Torre di Hanoi")
    parser.add_argument('-d', '--dischi', type=int, default=5,
                       help="Numero di dischi (default: 5)")
    parser.add_argument('-a', '--algoritmo', choices=['brfs', 'astar', 'dfs', 'bfs'], 
                       help="Algoritmo di risoluzione")
    parser.add_argument('-e', '--euristica', choices=['base', 'mosse_minime', 'livello_pila'],
                       help="Tipo di euristica per A*")
    
    args = parser.parse_args()
    
    gioco = InterfacciaHanoi(
        num_dischi=args.dischi,
        algoritmo=args.algoritmo,
        euristica=args.euristica if args.algoritmo in ['astar', 'bfs'] else 'base' 
    )
    gioco.esegui()

if __name__ == "__main__":
    main()