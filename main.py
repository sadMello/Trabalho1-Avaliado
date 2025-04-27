from PIL import Image
import numpy as np
import os

def salvar(imagem_obj, nome_saida):
    """
    Salva a imagem na pasta 'output'
    
    """
    os.makedirs("output", exist_ok=True)
    caminho_saida = os.path.join("output", nome_saida)
    imagem_obj.save(caminho_saida)
    print(f"Imagem salva em: {caminho_saida}")
    print(f"Matriz resultante: {imagem_obj.size}")

def reescalar_imagem_para_0_255(matriz):
    
    qtd_linhas, qtd_colunas = matriz.shape
    valor_minimo = np.min(matriz)
    valor_maximo = np.max(matriz)
    matriz_escalonada = np.zeros(matriz.shape, dtype=np.uint8)
    
    for i in range(qtd_linhas):
        for j in range(qtd_colunas):
            matriz_escalonada[i, j] = int(255 * (matriz[i, j] - valor_minimo) / (valor_maximo - valor_minimo))
        
    return matriz_escalonada
    
def soma(imagem1, imagem2):
    """
    Realiza a soma entre duas imagens.
    
    """
    if imagem1.size != imagem2.size:
        raise ValueError("As imagens devem ter o mesmo tamanho para serem processadas.")
    
    qtd_linhas, qtd_colunas = imagem1.size
    
    matriz_soma = np.zeros((qtd_linhas, qtd_colunas), dtype=np.uint16)
    for i in range(qtd_linhas):
        for j in range(qtd_colunas):
            matriz_soma[i, j] = imagem1.getpixel((i, j)) + imagem2.getpixel((i, j))
    
    matriz_soma = reescalar_imagem_para_0_255(matriz_soma)
    return matriz_soma
    
    
    
def subtracao(imagem1, imagem2):
    """Realiza a subtração de uma imagem por outra, retornando a matriz resultante escalada para 0-255.
    
    A função verifica se as imagens têm o mesmo tamanho e, em caso negativo, lança um ValueError.

    Args:
        imagem1 (_obj_): _a imagem a ser subtraida_
        imagem2 (_obj_): _segunda imagem_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if imagem1.size != imagem2.size:
        raise ValueError("As imagens devem ter o mesmo tamanho para serem processadas.")
    qtd_linhas, qtd_colunas = imagem1.size
    matriz_subtracao = np.zeros((qtd_linhas, qtd_colunas), dtype=np.int16)
    for i in range(qtd_linhas):
        for j in range(qtd_colunas):
            matriz_subtracao[i, j] = imagem1.getpixel((i, j)) - imagem2.getpixel((i, j)) 
    
    matriz_subtracao = reescalar_imagem_para_0_255(matriz_subtracao)
    return matriz_subtracao

    

def main():
    caminho_imagem = "imagem.jpg"  # Imagem deve estar na pasta do projeto
    try:
        imagem1 = Image.open(caminho_imagem).convert("L") # Converte para escala de cinza
    except Exception as erro:
        print("Erro ao carregar a imagem:", erro)
        return
    caminho_imagem = "imagem2.png"  # Imagem deve estar na pasta do projeto
    try:
        imagem2 = Image.open(caminho_imagem).convert("L") # Converte para escala de cinza
    except Exception as erro:
        print("Erro ao carregar a imagem:", erro)
        return
    
    # Realiza a soma das imagens
    matriz_soma = soma(imagem1, imagem1)
    img_soma = Image.fromarray(matriz_soma)
    salvar(img_soma, "imagem_soma.jpg")
    
    # Realiza a subtração das imagens
    matriz_subtracao = subtracao(imagem1, imagem2)
    img_subtracao = Image.fromarray(matriz_subtracao)
    salvar(img_subtracao, "imagem_subtracao.jpg")



if __name__ == "__main__":
    main()
