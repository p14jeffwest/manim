from manimlib.imports import *

class MoveToTest(Scene):
    def construct(self):
        direction = [ORIGIN, LEFT, RIGHT, UP, DOWN]
        for d in direction:
            self.move_to_obj(d)

        for d in direction:
            self.move_to_point(d)

        self.move_to_point_mask(ORIGIN, mask=np.array([0.5,0.5,0]))

    def move_to_obj(self, direction):
        rect1 = Rectangle(width=0.4, height=0.2, stroke_color=RED)
        rect2 = Rectangle(width=1, height=1, stroke_color=BLUE).move_to(np.array([2, 3, 0]))

        self.add(rect1,rect2)
        self.wait()
        self.play(rect1.move_to, rect2, {"aligned_edge":direction})
        self.wait()
        self.remove(rect1,rect2)

    def move_to_point(self, direction):
        rect1 = Rectangle(width=0.4, height=0.2, stroke_color=RED)
        rect2 = Rectangle(width=1, height=1, stroke_color=BLUE).move_to(np.array([2, 3, 0]))
        tgt_point = np.array([2,3,0])

        self.add(rect1, rect2)
        self.wait()
        self.play(rect1.move_to, tgt_point, {"aligned_edge": direction})
        self.wait()
        self.remove(rect1, rect2)

    def move_to_point_mask(self, direction, mask):
        rect1 = Rectangle(width=0.4, height=0.2, stroke_color=RED)
        rect2 = Rectangle(width=1, height=1, stroke_color=BLUE).move_to(np.array([2, 3, 0]))
        tgt_point = np.array([2,3,0])

        self.add(rect1, rect2)
        self.wait()
        self.play(rect1.move_to, tgt_point, {"aligned_edge": direction, "coor_mask":mask})
        self.wait()
        self.remove(rect1, rect2)

class ToEdgeTest(Scene):
    def construct(self):
        self.to_edge_test()
        self.to_edge_test(buff=0.5)

    def to_edge_test(self, buff=0):
        text = Text("Hello", font='Arial', stroke_width=1, size=0.4)
        rect = Rectangle(width=0.3, height=text.get_height(),stroke_color=RED)

        group = VGroup(rect,text).arrange(RIGHT)
        group.save_state()
        self.add(group)

        for d in [LEFT,RIGHT,UP,DOWN]:
            self.play(group.to_edge, d, {"buff":buff})
            self.wait()
            group.restore()
        self.remove(group)


class ToCornerTest(Scene):
    def construct(self):
        self.draw_border()
        self.to_corner_test()
        self.to_corner_test(buff=0.5)

    def draw_border(self):
        border = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, stroke_color=YELLOW)
        self.add(border)

    def to_corner_test(self, buff=0):
        text = Text("Hello", font='Arial', stroke_width=1, size=0.4)
        rect = Rectangle(width=0.3, height=text.get_height(), stroke_color=RED)

        group = VGroup(rect, text).arrange(RIGHT)
        group.save_state()
        self.add(group)

        for d in [UL, UR, DL, DR]:
            self.play(group.to_edge, d, {"buff": buff})
            self.wait()
            group.restore()
        self.remove(group)

class NextToTest(Scene):
    def construct(self):
        dir_str = ['ORIGIN', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'UL', 'UR', 'DL', 'DR']
        dir_list = [ORIGIN, LEFT, RIGHT, UP, DOWN, UL, UR, DL, DR]

        #1. next_to(obj, ORIGIN/LEFT/RIGHT/UP/DOWN/UL/UR/DL/DR)
        for str, d in zip(dir_str, dir_list):
            self.next_to_obj(str,d)

        #2. next_to(obj, direction, buff=0.5)
        for str, d in zip(dir_str, dir_list):
            self.next_to_obj(str+" buff=0.5",d, buff=0.5)

        #3. next_to(obj, LEFT, buff=0, aligned_edge=ORIGIN/LEFT/RIGHT/UP/DOWN
        for i in range(0,5):
            self.next_to_obj("LEFT, aligned_edge="+dir_str[i], LEFT, buff=0, aligned_edge=dir_list[i])

        # 4 next_to(obj, LEFT, buff=0.5, aligned_edge=ORIGIN/LEFT/RIGHT/UP/DOWN
        for i in range(0, 5):
            self.next_to_obj("LEFT, buff=0.5, aligned_edge=" + dir_str[i], LEFT, buff=0.5, aligned_edge=dir_list[i])

        # 5. next_to(point, ORIGIN/LEFT/RIGHT/UP/DOWN/UL/UR/DL/DR)
        for str, d in zip(dir_str, dir_list):
            self.next_to_point(str,d)

    def next_to_obj(self, str, direction=ORIGIN, buff=0, aligned_edge=ORIGIN):
        rect1 = Rectangle(width=0.4, height=0.2, stroke_color=RED)
        rect2 = Rectangle(width=1.5, height=1.5, stroke_color=BLUE).move_to(np.array([2, 2, 0]))
        text = Text(str, font='굴림', stroke_width=0, size=0.4).next_to(rect1, DOWN)

        self.add(rect1, rect2, text)
        self.wait(0.3)

        self.play(rect1.next_to, rect2, direction, {"buff":buff, "aligned_edge": aligned_edge})
        self.wait()
        self.remove(rect1, rect2, text)

    def next_to_point(self, str, direction=ORIGIN, buff=0, aligned_edge=ORIGIN):
        rect1 = Rectangle(width=0.4, height=0.2, stroke_color=RED)
        rect2 = Rectangle(width=1.5, height=1.5, stroke_color=BLUE).move_to(np.array([2, 2, 0]))
        text = Text(str, font='굴림', stroke_width=0, size=0.4).next_to(rect1, DOWN)

        tgt_point = np.array([2,2,0])

        self.add(rect1, rect2, text)
        self.wait(0.3)

        self.play(rect1.next_to, tgt_point, direction, {"buff": buff, "aligned_edge": aligned_edge})
        self.wait()
        self.remove(rect1, rect2, text)

class ShiftTest(Scene):
    def construct(self):
        self.move_around_with_one_object()
        self.make_lattice_fully()
        self.make_lattice_fully()

    def move_around_with_one_object(self):
        dot = Dot()
        directions = [RIGHT, UP, LEFT, LEFT, DOWN, DOWN, RIGHT, RIGHT]

        self.add(dot)
        for d in directions:
            self.play(dot.shift, d)
        self.wait()
        self.remove(dot)

    def make_latttice(self):
        dot = Dot()
        directions = [RIGHT, UP, LEFT, LEFT, DOWN, DOWN, RIGHT, RIGHT]

        dots = VGroup()  #to remove dots
        self.add(dot)
        for d in directions:
            dot = dot.copy()
            self.play(dot.shift, d)
            dots.add(dot)
        self.wait(2)
        self.remove(dots)

    def make_lattice_fully(self):
        dot = Dot()
        dot.move_to(np.array([7, 5, 0]))
        self.add(dot)
        for y in range(4, -5, -1):
            dot = dot.copy()
            self.play(dot.shift, DOWN, LEFT * 14, run_time=0.1)
            for x in range(-7, 7):
                dot = dot.copy()
                self.play(dot.shift, RIGHT, run_time=0.05)
        self.wait()

class CoordinateEx1(Scene):
    def construct(self):
        #1. create objects
        title = self.get_title()
        body = self.get_body()
        subtitle = self.get_subtitle()

        #2. locate objects
        title.move_to(ORIGIN).to_edge(UP, buff=1)
        body.next_to(title, DOWN, buff=1)
        subtitle.to_edge(DOWN, buff=0.5)

        #3. animate objects
        self.play(FadeIn(title), run_time=2)
        self.play(FadeIn(body), run_time=2)
        self.play(FadeIn(subtitle), run_time=2)
        self.wait(2)

    def get_text(self, str, color=WHITE, size=0.4):
        return Text(str, font='굴림', stroke_width=1, color=color, size=size)

    def get_title(self):
        t1 = self.get_text("IMF 국제통화기금", color=BLUE, size=0.4 )
        t2 = self.get_text("2020 세계 경제 전망", color=WHITE, size=0.6)

        t2.next_to(t1, RIGHT, buff=0.3)
        text = VGroup(t1, t2)

        underline = Line(LEFT, RIGHT, color = GREY).set_width(text.get_width())
        underline.next_to(text, DOWN, buff=0.1)

        return VGroup(text, underline)

    def get_body(self):
        t1 = self.get_text("세계", color=WHITE, size=1)
        t2 = self.get_text("-3%", color=RED, size=1.4)

        t2.next_to(t1, RIGHT, buff=0.8)
        return VGroup(t1, t2)
    
    def get_subtitle(self):
        rect1 = Rectangle(width=FRAME_WIDTH-1.5, height=0.4, fill_opacity=1, fill_color=BLUE, stroke_width=0)
        t1 = self.get_text("쿠오모", color=WHITE, size=0.3)
        t2 = self.get_text("뉴욕주지사", color=WHITE, size=0.2)
        t2.next_to(t1, RIGHT, buff=0.2)
        up_text = VGroup(t1,t2).move_to(rect1, LEFT).shift(RIGHT*0.1)
        rect1.add(up_text)

        rect2 = Rectangle(width=FRAME_WIDTH-1.5, height=0.8, fill_opacity=1, fill_color=WHITE, stroke_width=0)
        t3 = self.get_text("세계 경제 전망이 ...,", color=BLUE_E, size=0.3)
        t4 = self.get_text("물품 구매도 각 주가 책임져야...", color=BLUE_E, size=0.3)
        t4.next_to(t3, DOWN, aligned_edge=LEFT, buff=0.1)
        down_text = VGroup(t3,t4).move_to(rect2, LEFT).shift(RIGHT*0.1)
        rect2.add(down_text)

        rect2.next_to(rect1, DOWN, buff=0)
        return VGroup(rect1, rect2)

