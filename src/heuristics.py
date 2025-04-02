class EuristicheHanoi:
    @staticmethod
    def base(stato, num_dischi):
        piolo_obiettivo = 2
        h = 0
        for piolo in range(3):
            for disco in stato[piolo]:
                if piolo != piolo_obiettivo:
                    h += 1
                    if disco < num_dischi:
                        h += 0.5
        return h

    @staticmethod
    def mosse_minime(stato, num_dischi):
        piolo_obiettivo = 2
        h = 0
        for piolo in range(3):
            for disco in stato[piolo]:
                if piolo != piolo_obiettivo:
                    h += 2 ** (disco - 1) if disco > 1 else 1
        return h

    @staticmethod
    def livello_pila(stato, num_dischi):
        piolo_obiettivo = 2
        h = 0
        for piolo in range(3):
            altezza_pila = len(stato[piolo])
            for pos, disco in enumerate(stato[piolo]):
                if piolo != piolo_obiettivo:
                    h += (altezza_pila - pos) * disco
        return h

    @classmethod
    def ottieni(cls, nome):
        return {
            'base': cls.base,
            'mosse_minime': cls.mosse_minime,
            'livello_pila': cls.livello_pila
        }.get(nome, cls.base)