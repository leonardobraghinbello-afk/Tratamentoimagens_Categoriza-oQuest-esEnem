"""
Propósito: Remover a bordinha interna que fica entre as colunas
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "divididas-com-bordas-do-meio" do passo 3 para essa pasta do passo 4

OBS2: As imagens da coluna da esquerda tem uma bordinha no lado direito

OBS3: As imagens da coluna da direita tem uma bordinha no lado esquerdo

OBS4: abra as imagens no GIMP para contar pixels e saber quantos pixels cortar da borda interna

OBS5: este código vai criar uma pasta de saída chamada "divididas-sem-bordas-do-meio", vai cortar as bordinhas internas de cada coluna e salvar as imagens cortadas nessa pasta criada

OBS6: Atualize as linhas 43 e 47 com os valores corretos de corte (esquerda, superior, direita, inferior) para a respectiva coluna (esquerda/direita)

OBS7: execute o código, e abra as imagens para conferir se as bordas foram removidas corretamente. Se não, ajuste os valores de corte e execute novamente.
"""

from PIL import Image
import os

pasta_imagens = "divididas-com-bordas-do-meio"
pasta_saida = "divididas-sem-bordas-do-meio"

os.makedirs(pasta_saida, exist_ok=True)

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(".png"):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        imagem = Image.open(caminho_entrada)
        
        largura, altura = imagem.size
        
        # Aplica o corte original das bordas totais
        caixa_corte = (0, 0, largura, altura)
        
        # Aplica cortes adicionais baseados no nome do arquivo
        if nome_arquivo.endswith("_esquerda.png"):
            # Remover pixels da borda direita das imagens de coluna da esquerda, nesse exemplo, 25 pixels
            caixa_corte = (caixa_corte[0], caixa_corte[1], caixa_corte[2] - 24, caixa_corte[3]) # ATUALIZE AQUI O VALOR DE CORTE PARA A COLUNA DA ESQUERDA (esquerda, superior, direita, inferior)
        
        elif nome_arquivo.endswith("_direita.png"):
            # Remover pixels da borda esquerda das imagens de coluna da direita, nesse exemplo, 25 pixels
            caixa_corte = (caixa_corte[0] + 25, caixa_corte[1], caixa_corte[2], caixa_corte[3]) # ATUALIZE AQUI O VALOR DE CORTE PARA A COLUNA DA DIREITA (esquerda, superior, direita, inferior)
        
        imagem_cortada = imagem.crop(caixa_corte)
        
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        imagem_cortada.save(caminho_saida)

print("Recorte das bordas concluído.")