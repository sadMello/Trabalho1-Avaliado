from PIL import Image
import numpy as np
import os

class Imagem:
    def __init__(self, imagem):
        self.matriz = imagem
        self.qtd_linhas, self.qtd_colunas = imagem.shape

    def verificar_tamanhos(self, outra_imagem: "Imagem"):
        if (self.qtd_linhas != outra_imagem.qtd_linhas or self.qtd_colunas != outra_imagem.qtd_colunas):
            raise ValueError("As imagens devem ter o mesmo tamanho para serem processadas.")
       
    def reescalar_imagem_para_0_255(self, matriz):

        valor_minimo = np.min(matriz)
        valor_maximo = np.max(matriz)
        matriz_escalonada = np.zeros(matriz.shape, dtype=np.uint8)
        
        for i in range(self.qtd_linhas):
            for j in range(self.qtd_colunas):
                matriz_escalonada[i, j] = int(255 * (matriz[i, j] - valor_minimo) / (valor_maximo - valor_minimo))
        
        return matriz_escalonada
    
            