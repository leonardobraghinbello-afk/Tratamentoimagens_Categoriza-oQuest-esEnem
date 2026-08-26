"""
Propósito: converter o arquivo PDF em imagens PNG
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025.
Atualização: 03/06/2026

OBS1: procure no site do governo a sua prova, baixe o PDF e coloque na mesma pasta deste script

OBS2: na linha 21, especifique o nome do arquivo PDF que deseja converter.

OBS3: este código vai criar uma pasta de saída chamada "imagens-convertidas" e vai pegar página por página do PDF e salvar como imagens PNG nessa pasta.

OBS4: depois de executar, tem que excluir as imagens com nome de código estranho da pasta de saída, deixando só os nomes que fazem sentido

OBS5: Seu objetivo é deixar apenas as questões. Por isso abra cada uma das imagens, exclua as páginas de capa, proposta de redação e rascunho da redação e qualquer outra página que não tenha questões.
"""

from pdf2image import convert_from_path
import os

arquivo = "cadernoazul.pdf"
pasta_saida = "imagens-convertidas"

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

resolucao_dpi = 300

print (f"Convertendo '{arquivo}' para imagens com {resolucao_dpi} DPI...")

try:
    images = convert_from_path(
        arquivo,
        dpi = resolucao_dpi,
        output_folder = pasta_saida,
        fmt = "png",
        paths_only = False,
    )

    for i, image in enumerate(images):
        image_filename = os.path.join(pasta_saida, f"pagina_enem_{i+1}.png")
        image.save(image_filename)
        print(f"Página {i+1} salva como '{image_filename}'")

    print(f"\nConversão concluída! As imagens foram salvas na pasta '{pasta_saida}'.")

except Exception as e:
    print (f"Ocorreu um erro durante a conversão: {e}")
    print("Verifique se o Poppler está instalado corretamente, se o caminho do PDF está correto ou se o PDF não está corrompido.")