# Código de um vídeo de codigo Assembly

Video exemplo feito com Manim, python.

Segue aqui o objetivo do vídeo:

> ![image](https://github.com/user-attachments/assets/8d5665bc-b3f6-42fc-8ab0-c4be20d572b0)
>
> Utilizar essa imagem, para gerar de forma criativa esse fluxo que acontece entre a arquitetura do computador, poderá ser feito animações, teatro, gameficação ou qualquer forma que mostre como esses dados trafegam e geram os resultados.

Tem o .mp4 final na root do projeto, caso você renderize outro, ele estará na pasta media.

# Como rodar:

Instale a biblioteca de renderização .mp4 com `pip3 install manim`, se der um erro de ffmpeg é um rolo pra arrumar.

Rode o comando `manim -pql asm_visualization.py ASMVisualization` para renderizar o vídeo. (caso apareça um warning de PATH, use `python -m manim -pql asm_visualization.py ASMVisualization`)

Para informações mais completas, siga o guia de instalação em https://docs.manim.community/en/stable/installation.html