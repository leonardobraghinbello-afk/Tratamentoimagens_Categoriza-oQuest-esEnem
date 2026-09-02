import os
from PIL import Image

# Remove o limite de tamanho de imagem para evitar o aviso/erro de DecompressionBomb
Image.MAX_IMAGE_PIXELS = None


def verificar_faixa_cor(
    pixels, x, y_inicio, altura, cor_alvo, tolerancia_cor=30
):
    """Verifica se a maioria dos pixels da faixa bate com a cor alvo (tolerando ruídos isolados)."""
    erros_permitidos = max(
        1, int(altura * 0.2)
    )  # Tolera até 20% de pixels fora do padrão na faixa
    erros = 0

    for dy in range(altura):
        pixel = pixels[x, y_inicio + dy]
        r, g, b = pixel[:3]

        if (
            abs(r - cor_alvo[0]) > tolerancia_cor
            or abs(g - cor_alvo[1]) > tolerancia_cor
            or abs(b - cor_alvo[2]) > tolerancia_cor
        ):
            erros += 1
            if erros > erros_permitidos:
                return False
    return True


def encontrar_padrao_vertical(
    imagem, x_offset=5, tolerancia_cor=30, margem_altura=3
):
    largura, altura_total = imagem.size
    pixels = imagem.load()

    cor_escura = (35, 31, 32)
    cor_branca = (255, 255, 255)

    especificacao = [
        (cor_escura, 9),
        (cor_branca, 4),
        (cor_escura, 5),
        (cor_branca, 4),
        (cor_escura, 9),
    ]

    altura_minima_padrao = sum(
        max(1, alt - margem_altura) for _, alt in especificacao
    )
    posicoes_corte = []

    # Testa a coluna recuada 'x_offset' pixels da borda direita para evitar artefatos de borda
    x = largura - x_offset

    y = 0
    while y < altura_total - altura_minima_padrao:
        y_atual = y
        padrao_encontrado = True
        altura_total_detectada = 0

        for cor_alvo, altura_base in especificacao:
            faixa_ok = False

            # Modificação: testar da altura original para as variações (prioriza o tamanho exato primeiro)
            variacoes = [altura_base] + [
                alt
                for alt in range(
                    max(1, altura_base - margem_altura),
                    altura_base + margem_altura + 1,
                )
                if alt != altura_base
            ]

            for alt_variada in variacoes:
                if y_atual + alt_variada > altura_total:
                    break

                if verificar_faixa_cor(
                    pixels,
                    x,
                    y_atual,
                    alt_variada,
                    cor_alvo,
                    tolerancia_cor,
                ):
                    y_atual += alt_variada
                    altura_total_detectada += alt_variada
                    faixa_ok = True
                    break

            if not faixa_ok:
                padrao_encontrado = False
                break

        if padrao_encontrado:
            posicao_corte = max(0, y - 13)
            posicoes_corte.append(posicao_corte)
            print(
                f"Padrão encontrado iniciando em y={y}, cortando em y={posicao_corte}"
            )
            y += max(1, altura_total_detectada)
        else:
            y += 1

    return posicoes_corte


def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size

    print(f"Imagem carregada: {largura}x{altura} pixels")

    posicoes_corte = encontrar_padrao_vertical(imagem)

    if not posicoes_corte:
        print(
            "Nenhum padrão encontrado! Tente verificar a cor no GIMP na coluna X correspondente."
        )
        return

    print(f"Encontradas {len(posicoes_corte)} ocorrências do padrão de corte")

    os.makedirs(pasta_saida, exist_ok=True)

    posicao_anterior = 0

    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue

        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

        posicao_anterior = posicao_corte

    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")


if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"
    pasta_saida = "questoes_cortadas"

    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    print("Divisão concluída!")