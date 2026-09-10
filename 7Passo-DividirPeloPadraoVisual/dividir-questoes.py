"""
Propósito: Dividir as questões por padrão visual vertical de 5 faixas.
Autor: Alexandre Nassar de Peder
Atualização: Ajustado para padrão customizado de 5 faixas.
"""

from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None

def cor_combinam(pixel, cor_alvo, tolerancia=15):
    """Verifica se a cor de um pixel combina com a cor alvo dentro da tolerância."""
    r, g, b = pixel[:3]
    return (abs(r - cor_alvo[0]) <= tolerancia and 
            abs(g - cor_alvo[1]) <= tolerancia and 
            abs(b - cor_alvo[2]) <= tolerancia)

def encontrar_padrao_questoes(imagem, tolerancia_cor=15):
    """
    Procura no último pixel da direita pelo padrão de 5 faixas verticais:
    1. 9px (35, 31, 32)   [margem 6-12px]
    2. 4px (255, 255, 255) [margem 1-7px]
    3. 5px (35, 31, 32)   [margem 2-8px]
    4. 4px (255, 255, 255) [margem 1-7px]
    5. 9px (35, 31, 32)   [margem 6-12px]
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Definindo as cores e alturas esperadas com a margem de erro de +-3px
    c_escura = (35, 31, 32)
    c_branca = (255, 255, 255)
    
    faixas_especificacao = [
        {'cor': c_escura, 'min': 6, 'max': 12},  # 9px +- 3
        {'cor': c_branca, 'min': 1, 'max': 7},   # 4px +- 3
        {'cor': c_escura, 'min': 2, 'max': 8},   # 5px +- 3
        {'cor': c_branca, 'min': 1, 'max': 7},   # 4px +- 3
        {'cor': c_escura, 'min': 6, 'max': 12}   # 9px +- 3
    ]
    
    posicoes_corte = []
    x = largura - 1  # Último pixel da direita
    y = 0
    
    while y < altura - 50: # Limite seguro para busca
        padrão_encontrado = True
        y_atual = y
        
        for idx_faixa, faixa in enumerate(faixas_especificacao):
            altura_faixa_detectada = 0
            
            # Conta quantos pixels seguidos pertencem a esta faixa
            while y_atual < altura and cor_combinam(pixels[x, y_atual], faixa['cor'], tolerancia_cor):
                altura_faixa_detectada += 1
                y_atual += 1
                
            # Valida se a altura medida está dentro da margem de erro (min - max)
            if not (faixa['min'] <= altura_faixa_detectada <= faixa['max']):
                padrão_encontrado = False
                break
        
        if padrão_encontrado:
            # Padrão encontrado a partir do Y inicial da primeira faixa
            posicao_corte = y - 13
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append((posicao_corte, y_atual))
            print(f"Padrão encontrado iniciando em y={y}. Cortando 13px acima em y={posicao_corte}")
            
            # Avança o loop além do padrão encontrado para evitar re-detecções
            y = y_atual
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente com base nos pontos de corte encontrados.
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    cortes = encontrar_padrao_questoes(imagem)
    
    if not cortes:
        print("Nenhum padrão visual encontrado na imagem!")
        return
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, (posicao_corte, fim_padrao) in enumerate(cortes):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Salva o bloco final após o último corte
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(cortes)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo final: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Substitua pela sua imagem de entrada
    pasta_saida = "questoes"           # Substitua pela pasta de saída desejada
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    print("Divisão concluída!")