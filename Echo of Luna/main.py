from fases import *
from telas import *

if __name__ == "__main__":
    while True:
        tela_inicial()     
        pontuacao = Fase1() 
        Game_over(pontuacao)