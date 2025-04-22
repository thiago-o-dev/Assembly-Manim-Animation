from manim import *

class ASMVisualization(Scene):
    def construct(self):
        # Configuração de layout
        CODE_Y = 3
        LINE_HEIGHT = 0.3

        # Definição das linhas de código ASM
        asm_lines = [
            "| ; Iniciamos nossas variáveis",
            "| DATA SEGMENT ",
            "|     [1] DB 5 ",
            "|     [2] DB 7 ",
            "|     [3] DB ? ",
            "| DATA ENDS ",
            "|  ",
            "| START: ; Junto do start vem os registradores",
            "|     ; 1) Inicializamos o segmento de dados",
            "|     LOAD AX, [1] ; Guardamos o [1] em AX",
            "|     LOAD BX, [2] ; idem", 
            "|  ",
            "|     ; 2) Adicionamos eles", 
            "|     ADD AX, BX ; Soma os registradores",
            "|  ",
            "|     ; 3) Guardamos o resultado",
            "|     STORE AX, [3] ; Guardamos em [3]",
            "|  ",
            "| CODE ENDS ",
            "| END START " 
        ]
        # Cria Text para cada linha e posiciona manualmente
        code_texts = VGroup(*[
            Text(line, font_size=16, t2c={f"[{line.find(";")}:]": GREEN}, font="Cascadia Mono", disable_ligatures=True) # JetBrains Mono
            for line in asm_lines 
        ])
        code_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Move o grupo todo para a borda esquerda da cena
        code_texts.to_edge(LEFT, buff=0.5)

        for index, line in enumerate(code_texts):
            new_y = CODE_Y - index * LINE_HEIGHT
            # Pega a coordenada x do centro do texto, precisou ser desse jeito pq o get_x() da erro pra cct
            x = line.get_center()[0]
            # Reposiciona apenas no eixo Y, mantendo o X
            line.move_to(np.array([x, new_y, 0]))

        # Torna invisível inicialmente
        code_texts.set_opacity(0)

        # Adiciona à cena
        self.add(code_texts)

        # Cria caixas de memória
        mem1 = Rectangle(width=1, height=1, fill_color=GREY, fill_opacity=0.5).move_to([2, 2, 0])
        mem2 = Rectangle(width=1, height=1, fill_color=GREY, fill_opacity=0.5).move_to([2, 0, 0])
        mem3 = Rectangle(width=1, height=1, fill_color=GREY, fill_opacity=0.5).move_to([2, -2, 0])
        label1 = Text("[1]: 5", font_size=20).next_to(mem1, ORIGIN)
        label2 = Text("[2]: 7", font_size=20).next_to(mem2, ORIGIN)
        label3 = Text("[3]: ?", font_size=20).next_to(mem3, ORIGIN)

        # Cria registradores
        reg_ax = Rectangle(width=1, height=1, fill_color=BLUE, fill_opacity=0.5).move_to([4.5, 1, 0])
        reg_bx = Rectangle(width=1, height=1, fill_color=BLUE, fill_opacity=0.5).move_to([4.5, -1, 0])
        label_ax = Text("AX: -", font_size=20).next_to(reg_ax, ORIGIN)
        label_bx = Text("BX: -", font_size=20).next_to(reg_bx, ORIGIN)

        # Exibe caixas e labels iniciais
        #self.play(Create(mem1), Create(mem2), Create(mem3), Create(reg_ax), Create(reg_bx))
        #self.play(Write(label1), Write(label2), Write(label3), Write(label_ax), Write(label_bx))
        self.wait(1)

        # Sequência de animações: (linha, ação)
        sequence = [
            ([0,1,2,3,4,5], None),  # ; Iniciamos nossas variaveis
            ([], 'startup_memory'),  # ; Iniciamos nossas variaveis
            ([6,7], 'startup_regs'),
            ([8,9], 'load_ax'), # ; Guardamos o [1] em AX",
            ([10], 'load_bx'),      # LOAD BX aparecendo
            ([11,12,13], None),
            ([13], 'add'),
            ([14,15,16], None),
            ([16], 'store'),
            ([17,18,19], None)
        ]
        # TODO: usar uma [] para mostrar mais de 1 código por vez
        for idxs, action in sequence:
            # Mostrar linha de código
            if isinstance(idxs, int): idxs = [idxs]
            animations = [code_texts[idx].animate.set_opacity(1) for idx in idxs]
            can_play_animations = len(animations) != 0

            if can_play_animations:
                self.play(*animations)

            # Executar ação
            match action:
                case 'startup_memory':
                    self.play(Create(mem1), Create(mem2), Create(mem3))
                    self.play(Write(label1), Write(label2), Write(label3))

                case 'startup_regs':
                    self.play(Create(reg_ax), Create(reg_bx))
                    self.play(Write(label_ax), Write(label_bx))

                case 'load_ax':
                    arrow = Arrow(mem1.get_right(), reg_ax.get_left(), buff=0.1)
                    self.play(Create(arrow))
                    self.play(Transform(label_ax, Text("AX: 5", font_size=20).next_to(reg_ax, ORIGIN)))

                case 'load_bx':
                    arrow = Arrow(mem2.get_right(), reg_bx.get_left(), buff=0.1)
                    self.play(Create(arrow))
                    self.play(Transform(label_bx, Text("BX: 7", font_size=20).next_to(reg_bx, ORIGIN)))

                case 'add':
                    animations = [code_texts[idx].animate.set_color(YELLOW) for idx in idxs]
                    if can_play_animations:
                        self.play(*animations)
                    sum_label = Text("AX = 5 + 7 = 12", font_size=20).next_to(code_texts[idxs[0]], RIGHT, buff=0.5)
                    arrow = Arrow(sum_label.get_right(), reg_ax.get_left(), buff=0.1)
                    self.play(Write(sum_label))
                    self.play(Create(arrow))
                    self.play(Transform(label_ax, Text("AX: 12", font_size=20).next_to(reg_ax, ORIGIN)))
                    self.play(FadeOut(sum_label), FadeOut(arrow))

                case 'store':
                    arrow = Arrow(reg_ax.get_left(), mem3.get_right(), buff=0.1)
                    animations = [code_texts[idx].animate.set_color(YELLOW) for idx in idxs]
                    if can_play_animations:
                        self.play(*animations)
                    self.play(Create(arrow))
                    self.play(Transform(label3, Text("[3]: 12", font_size=20).next_to(mem3, ORIGIN)))
            self.wait(1)

if __name__ == "__main__":
    from manim import config
    # Aspect ratio 16:9
    config.pixel_width = 1280/2
    config.pixel_height = 720/2
    config.frame_rate = 10
    ASMVisualization().construct()
