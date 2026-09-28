import random

class Dados:
    dev_mode = False
    dev_sequence = [11, 3, 2, 5]

    @staticmethod
    def tirar_dados():
        if Dados.dev_mode:
            if len(Dados.dev_sequence) > 0:
                return Dados.dev_sequence.pop(0)

            return 1

        return random.randint(1, 6)