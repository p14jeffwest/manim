from manimlib.imports import *

class CalScreenSize(Scene):
    def construct(self):
        s_w = self.cal_screen_width()
        s_h = self.cal_screen_height()

        t1 = self.get_text("screen width=" + str(s_w))
        t2 = self.get_text("screen height=" + str(s_h))
        text = VGroup(t1, t2).arrange(DOWN)
        self.add(text)
        self.wait()

    def cal_screen_height(self):
        dot1 = Dot()
        dot2 = Dot()

        dot1.to_edge(UP, buff=0)
        dot2.to_edge(DOWN, buff=0)
        self.add(dot1, dot2)

        p1 = dot1.get_top()
        p2 = dot2.get_bottom()

        length = np.linalg.norm(p2 - p1)
        return length

    def cal_screen_width(self):
        dot1 = Dot()
        dot2 = Dot()

        dot1.to_edge(LEFT, buff=0)
        dot2.to_edge(RIGHT, buff=0)

        p1 = dot1.get_left()
        p2 = dot2.get_right()

        length = np.linalg.norm(p2 - p1)
        return length

    def get_text(self, str, size=0.3):
        return Text(str, font='굴림', stroke_width=1, size=size)

class Test(Scene):
    def construct(self):
        rect = Rectangle(width=1.5, height=1)
        you_label = TextMobject("you")
        you_label.next_to(rect, RIGHT, MED_LARGE_BUFF)
        arrow = Arrow(you_label.get_left(), rect.get_right() + 0.5 * LEFT, buff=0.1)

        self.add(rect,you_label, arrow)
        self.wait()

class FormulaCopy(Scene):
    def construct(self):
        formula = TexMobject("2x", "=", "8")
        formula.move_to(DOWN * 2)
        formula[0].set_color(RED)
        formula[2].set_color(BLUE)

        self.add(formula)
        self.wait()

        # x = TexMobject("3y")
        # x.become(formula[0], copy_submobjects=False)
        x = formula[0].copy()


        self.play(ReplacementTransform(formula[0],x))
        self.wait()

class AlignToTest(Scene):
    def construct(self):
        dir_str = [ 'UP', 'DOWN', 'LEFT', 'RIGHT']
        dir_list = [ UP, DOWN, LEFT, RIGHT]

        rect = Rectangle(width=1, height=0.4)
        rect_tgt = Rectangle(width=3, height=2).shift(RIGHT * 3, UP * 2)

        self.add(rect, rect_tgt)

        for str, dir in zip(dir_str, dir_list):
            new_rect = rect.copy()
            obj = self.get_text_rect(str, new_rect)
            self.play(obj.align_to, rect_tgt, dir)
        self.wait()

    def get_text_rect(self, str, rect):
        text = Text(str, font='Arial', stroke_width=0.1, size=0.2)

        text.move_to(rect)
        return VGroup(rect,text)

class ArrangeTest(Scene):
    def construct(self):
        str = ['Hello', 'This', 'is', 'Arrange', 'Test']
        self.display_text1(str)
        self.display_text2(str)

    def display_text1(self, str):
        text = VGroup()
        for s in str:
            t = self.get_text(s)
            text.add(t)

        text.to_edge(UP, buff=1)
        text.arrange(DOWN, buff=0.5)
        self.play(Write(text), run_time=3)
        self.wait()
        self.remove(text)

        text.move_to(ORIGIN).to_edge(LEFT, buff=1)
        text.arrange(RIGHT, buff=0.2)
        self.play(Write(text), run_time=3)
        self.wait()
        self.remove(text)

    def display_text2(self, str):
        text = VGroup(*[self.get_text(s) for s in str ])

        text.move_to(ORIGIN).to_edge(UP, buff=1)
        text.arrange(DOWN, center=False, aligned_edge = LEFT, buff=0.5)
        self.play(Write(text), run_time=3)
        self.wait()
        self.remove(text)

        text.move_to(ORIGIN).to_edge(LEFT, buff=1)
        text.arrange(LEFT, buff=0.2)
        # text.arrange(RIGHT, buff=0.2)
        self.play(Write(text), run_time=3)
        self.wait()

    def get_text(self,str):
        return Text(str, font='굴림', stroke_width=0, size=0.5)

class ArrangeInGridTest(Scene):
    def construct(self):
        y = 20
        x = 30
        colors = [RED, GREEN, BLUE]
        dots = VGroup(*[Dot() for x in range(y * x)])
        dots.arrange_in_grid(y, x, buff=SMALL_BUFF)
        for i in range(0, y*x):
            dots[i].set_color(colors[i % 3])

        self.add(dots)
        self.wait()