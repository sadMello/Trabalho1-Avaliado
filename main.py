from PIL import Image
import numpy as np
import os

#funções auxiliares para manipulação de imagens
def salvar(imagem_obj, nome_saida):
    """
    Salva a imagem na pasta 'output'
    
    Args:
        imagem_obj (PIL.Image): Objeto de imagem a ser salvo
        nome_saida (str): Nome do arquivo de saída
    """
    os.makedirs("output", exist_ok=True)
    caminho_saida = os.path.join("output", nome_saida)
    imagem_obj.save(caminho_saida)
    print(f"Imagem salva em: {caminho_saida}")
    print(f"Matriz resultante: {imagem_obj.size}")

def imagem_para_matriz(caminho_imagem):
    """
    Converte uma imagem em uma matriz numpy.
    
    Args:
        caminho_imagem (str): Caminho da imagem
        
    Returns:
        numpy.ndarray: Matriz de pixels em escala de cinza
    """
    try:
        imagem = Image.open(caminho_imagem).convert("L")
        matriz = np.array(imagem)
        return matriz
    except Exception as erro:
        print("Erro ao carregar a imagem:", erro)
        return None

def reescalar_imagem_para_0_255(matriz):
    """
    Normaliza os valores da matriz para o intervalo 0-255.
    
    Args:
        matriz (numpy.ndarray): Matriz de entrada
        
    Returns:
        numpy.ndarray: Matriz normalizada
    """
    valor_minimo = np.min(matriz)
    valor_maximo = np.max(matriz)
    
    if valor_maximo == valor_minimo:
        return np.zeros(matriz.shape, dtype=np.uint8)
    
    matriz_escalonada = 255 * (matriz - valor_minimo) / (valor_maximo - valor_minimo)
    return matriz_escalonada.astype(np.uint8)


#funções de operações aritméticas em imagens

def soma(matriz1, matriz2):
    """
    Realiza a soma entre duas imagens e retorna a matriz resultante.
    
    Args:
        matriz1 (numpy.ndarray): Primeira matriz de pixels
        matriz2 (numpy.ndarray): Segunda matriz de pixels
    
    Returns:
        numpy.ndarray: Matriz resultante da soma
    """
    if matriz1.shape != matriz2.shape:
        raise ValueError("As imagens devem ter o mesmo tamanho.")
    
    qtd_linhas, qtd_colunas = matriz1.shape
    matriz_soma = np.zeros((qtd_linhas, qtd_colunas), dtype=np.uint8)

    for i in range(qtd_linhas):
        for j in range(qtd_colunas):
            pixel1 = int(matriz1[i, j])
            pixel2 = int(matriz2[i, j])
            matriz_soma[i, j] = int((pixel1 + pixel2)/2)
            
    return matriz_soma

def subtracao(matriz_minuendo, matriz_subtraendo):
    """
    Realiza a subtração entre duas imagens e retorna a matriz resultante.
    
    Args:
        matriz_minuendo (numpy.ndarray): Matriz minuendo
        matriz_subtraendo (numpy.ndarray): Matriz subtraendo
    
    Returns:
        numpy.ndarray: Matriz resultante da subtração
    """
    if matriz_minuendo.shape != matriz_subtraendo.shape:
        raise ValueError("As imagens devem ter o mesmo tamanho.")
    
    qtd_linhas, qtd_colunas = matriz_minuendo.shape
    matriz_diferenca = np.zeros((qtd_linhas, qtd_colunas), dtype=np.int16)
    
    for i in range(qtd_linhas):
        for j in range(qtd_colunas):
            pixel1 = int(matriz_minuendo[i, j])
            pixel2 = int(matriz_subtraendo[i, j])
            matriz_diferenca[i, j] = pixel1 - pixel2
    
    matriz_diferenca = reescalar_imagem_para_0_255(matriz_diferenca)
    return matriz_diferenca.astype(np.uint8)

#função de operação geométrica 

def escalar_vizinho_proximo(imagem, escala_x, escala_y):
    """
    Escala uma imagem usando mapeamento inverso e interpolação por vizinho mais próximo.
    
    Args:
        imagem (numpy.ndarray): Matriz da imagem original
        escala_x (float): Fator de escala no eixo X
        escala_y (float): Fator de escala no eixo Y
    
    Returns:
        numpy.ndarray: Imagem escalonada
    """
    if escala_x <= 0 or escala_y <= 0:
        raise ValueError("Os fatores de escala devem ser positivos.")
    
    qtd_linhas, qtd_colunas = imagem.shape
    nova_largura = int(qtd_colunas * escala_x)
    nova_altura = int(qtd_linhas * escala_y)
    
    imagem_escalada = np.zeros((nova_altura, nova_largura), dtype=np.uint8)
    
    for linha in range(nova_altura):
        for coluna in range(nova_largura):
            x_origem = coluna / escala_x
            y_origem = linha / escala_y
            
            coluna_arredondada = int(round(x_origem))
            linha_arredondada = int(round(y_origem))
            
            if 0 <= coluna_arredondada < qtd_colunas and 0 <= linha_arredondada < qtd_linhas:
                imagem_escalada[linha, coluna] = imagem[linha_arredondada, coluna_arredondada]
    
    return imagem_escalada


def main():
    caminho_imagem = "imagem.jpg"
    matriz_imagem1 = imagem_para_matriz(caminho_imagem)

    matriz_soma = soma(matriz_imagem1, matriz_imagem1)
    imagem_soma = Image.fromarray(matriz_soma, mode="L")
    salvar(imagem_soma, "soma.jpg")
    
    matriz_subtracao = subtracao(matriz_imagem1, matriz_imagem1)
    imagem_subtracao = Image.fromarray(matriz_subtracao, mode="L")
    salvar(imagem_subtracao, "subtracao.jpg")

    matriz_escalada = escalar_vizinho_proximo(matriz_imagem1, 0.3, 1.2)
    imagem_escalada = Image.fromarray(matriz_escalada, mode="L")
    salvar(imagem_escalada, "escalada.jpg")

if __name__ == "__main__":
    main()