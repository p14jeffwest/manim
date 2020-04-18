from manimlib.imports import *

class ColorTest(Scene):
    def construct(self):
        # self.set_color_test()
        # self.display_color_map()
        self.gradient_test()

    def set_color_test(self):
        dot = Dot()
        rect = Rectangle()
        line = Line(ORIGIN, RIGHT)
        text = Text("Hello")

        group = VGroup(dot,rect,line, text).arrange(DOWN)

        #default color
        self.add(group)
        self.wait()

        #change color to red
        group.set_color(RED)
        self.play(ShowCreation(group))
        self.wait()

        #
        # group.set_color(YELLOW, family=False)
        group.set_color(YELLOW)
        self.play(ShowCreation(group))
        self.wait()

        self.remove(group)

    def display_color_map(self):
        def make_color(str,val):
            t = Text(str, font='Arial', stroke_width=0, size=0.2)
            rect = Rectangle(width=0.5, height=0.4, fill_opacity=1, fill_color=val).set_color(val)
            return VGroup(rect,t).arrange(DOWN,buff=0.08)

        map_size = len(COLOR_MAP)
        group = VGroup(*[make_color(str,val) for str,val in COLOR_MAP.items()])
        # group = VGroup()
        # for str, val in COLOR_MAP.items():
        #     group.add(make_color(str,val))

        # group.arrange_in_grid(6,10,aligned_edge=LEFT, buff=0.6)
        group.arrange_in_grid(6, 10, buff=0.4)
        self.add(group)
        self.wait(2)

        self.remove(group)

    def gradient_test(self):
        #dots
        dots = VGroup(*[Dot(radius=0.15) for i in range(20)])
        dots.arrange(RIGHT)
        dots.set_color_by_gradient(PINK, BLUE, YELLOW)

        #text
        text = TextMobject("Gradient Color")
        text.set_color_by_gradient(RED,YELLOW)
        text.next_to(dots, UP)

        #play
        self.play(
            FadeIn(dots),
            Write(text),
            run_time=2,
        )
        self.wait()

        self.remove(dots, text)


