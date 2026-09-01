"""
Propósito: Cortar as imagens de colunas ao meio. As imagens já estão sem as bordas externas, agora só cortar ao meio
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "sem-bordas-externas" do passo 2 para esta pasta do passo 3

OBS2: pode ter páginas inteiras e páginas com coluas. Crie uma pasta chamada "inteiras", retire as imagens inteiras e coloque-as nessa pasta

OBS3: observe também se as páginas do seu caderno mantém a mesma altura, tem cadernos que têm duas colunas mas não são exatamente cortadas na metade... se isso acontecer, você vai ter que tratar essas páginas de forma diferente

OBS4: este código vai criar uma pasta de saída chamada "divididas-com-bordas-do-meio", vai cortar ao meio (ver linha 35) as páginas que são colunas e salvar as imagens cortadas nessa pasta criada

OBS5: execute este código. Ao cortar as colunas ao meio, vai gerar uma bordinha interna

OBS6: as imagens vão receber um novo nome, com o sufixo "_esquerda" ou "_direita" para indicar a coluna
"""

from PIL import Image
import os

pasta_imagens = "sem-bordas-externas"
pasta_saida = "divididas-com-bordas-do-meio"

os.makedirs(pasta_saida, exist_ok=True)

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith('.png'):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        imagem = Image.open(caminho_entrada)

        largura, altura = imagem.size
        
        metade_largura = largura // 2
        
        caixa_esquerda = (0, 0, metade_largura, altura)
        imagem_esquerda = imagem.crop(caixa_esquerda)
        
        caixa_direita = (metade_largura, 0, largura, altura)
        imagem_direita = imagem.crop(caixa_direita)
        
        nome_base, extensao = os.path.splitext(nome_arquivo)
        
        caminho_esquerda = os.path.join(pasta_saida, f"{nome_base}_esquerda{extensao}")
        caminho_direita = os.path.join(pasta_saida, f"{nome_base}_direita{extensao}")
        
        imagem_esquerda.save(caminho_esquerda)
        imagem_direita.save(caminho_direita)

print("Divisão das imagens ao meio concluída.")