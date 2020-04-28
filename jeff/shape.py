from manimlib.imports import *

class SetFill(Scene):
    def construct(self):
        # self.set_fill_test()
        self.set_stroke_test()


    def set_fill_test(self):
        rect = Rectangle()
        rect.set_fill(RED_C, opacity=1)

        self.add(rect)
        self.wait()

    def set_stroke_test(self):
        rect1 = Rectangle(width=2,height=2)
        rect1.set_fill(BLUE, opacity=1)

        rect2 = rect1.copy()
        rect2.next_to(rect1,RIGHT)

        asterisk1 = TextMobject("*")
        asterisk1.set_height(0.7)
        asterisk1.set_stroke(BLACK, 3, background=True)
        asterisk1.move_to(rect1)

        asterisk2 = TextMobject("*")
        asterisk2.set_height(0.7)
        asterisk2.set_stroke(BLACK, 3, background=False)
        asterisk2.move_to(rect2)

        dot1 = Dot(radius=0.3)
        dot2 = dot1.copy()

        dot1.set_stroke(RED_E,2,background=True)
        dot2.set_stroke(RED_E, 2, background=False)

        dot1.move_to(rect1)
        dot2.move_to(rect2)

        # self.add(rect1,dot1,rect2,dot2)
        self.add(rect1,asterisk1,rect2,asterisk2)
        # self.add(asterisk1, rect1, asterisk2, rect2 )
        self.wait()

class LineTest(Scene):
    def construct(self):
        grid = self.get_grid(-7, 7, 1, -4, 4, 1)
        self.add(grid)

        # self.simple()
        # self.make_line_with_two_points()
        # self.make_general()
        # self.change_color()
        self.change_stroke_width()

    def simple(self):
        line = Line(stroke_color=RED, stroke_width=8)

        self.add(line)
        self.wait()

    def make_line_with_two_points(self):
        a = np.array([-1,1,0])
        b = np.array([1, -1, 0])

        line = Line(a,b)
        self.add(line)
        self.wait()

    def get_grid(self, sx, ex, dx, sy, ey, dy):
        def get_line(start, end):
            return Line(start,end, stroke_width=1, stroke_color=GREY, stroke_opacity=0.8)
        p = np.array
        v_lines = VGroup(*[get_line(p([x, sy, 0]), p([x, ey, 0])) for x in np.arange(sx, ex + dx, dx)])
        h_lines = VGroup(*[get_line(p([sx, y, 0]), p([ex, y, 0])) for y in np.arange(sy, ey + dy, dy)])
        return VGroup(v_lines, h_lines)

    def make_general(self):
        line = Line(LEFT, RIGHT)
        line.set_length(3)

        self.add(line)
        self.wait()

    def change_color(self):
        line = Line(stroke_color=RED, stroke_width=6)
        self.add(line)
        self.wait()

    def change_stroke_width(self):
        def get_line(w):
            line = Line(stroke_width=w)
            t = Text(str(w), size=0.3, stroke_width=0).next_to(line, LEFT, buff=0.2)
            return VGroup(t,line)

        lines = VGroup(*[get_line(w) for w in range(1,11)])

        lines.to_edge(UP, buff=0.5).arrange(DOWN, buff=0.5)
        self.add(lines)
        self.wait()

class ArrowTest(Scene):
    def construct(self):
        # self.simple_arrow()
        self.with_points()

    def simple_arrow(self):
        arrow = Arrow()

        self.add(arrow)
        self.wait()

    def with_points(self):
        arrow = Arrow(DOWN, UP)

        self.add(arrow)
        self.wait()

class Arrow_Buff(Scene):
    def construct(self):
        #1. 생성
        buff_changed = Arrow_Buff.get_buff_changed()
        scale_changed = Arrow_Buff.get_scale_changed()

        #2. 위치
        buff_changed.to_corner(UL, buff=1) #왼쪽 상단으로 buff=1의 여유를 두고 이동

        #buff_changed 안에 있는 객체들을 아래쪽으로 차례차례 배치.
        #center=False에 유의. 이렇게 하지 않으면, 객체들이 화면의 중앙에 배치되어 버림
        #aligned_edge=LEFT는, 각 객체들이 차례차례 배치될 때, 객체의 왼쪽 끝을 기준으로 정렬하라는 것
        buff_changed.arrange(DOWN, center=False, aligned_edge=LEFT)

        scale_changed.to_edge(UP, buff=1)
        scale_changed.arrange(DOWN, center=False, aligned_edge=LEFT)

        #3. Show
        self.add(buff_changed, scale_changed)
        self.wait()

    def get_scale_changed():
        #파이썬에서 값을 스텝 단위로 증가시키는 것은 정수 스템만 가능하기에,
        #소숫점 단위로 증가시킬 수 있는 numpy의 arange 메서드 이용해서 리스트 만듦
        n=np.arange(0,2.1,0.2)  #[0,2.1)까지 0.2씩 증가.  [0,2.1) : (0 <= x < 2.1)의 의미

        group = VGroup()
        for k in n:
            k = round(k,1) #소숫점 1자리에서 반올림. 이렇게 하지 않으면 소숫점이 길게 출력이되서 보기 안좋음
            arrow = Arrow()
            arrow.scale(k) #k만큼 크기 조절
            text = Text("scale:"+str(k),size=0.2,stroke_width=0) #stroke_width=0을해야 글자 두껍기가 적당해짐

            text.next_to(arrow,RIGHT)  #화살표 오른편에 글자 배치
            group.add(VGroup(arrow,text))  #arrow와 text를 VGroup으로 한 번 묶고나서 다시 이것을 group.add() 한 것에 유의
        return group

    def get_buff_changed():
        buff_size = [0,SMALL_BUFF,MED_SMALL_BUFF,MED_LARGE_BUFF]
        texts = ["0","SMALL_BUFF","MED_SMALL_BUFF","MED_LARGE_BUFF"]

        group = VGroup()
        for t, s in zip(texts,buff_size):
            arrow = Arrow(buff=s)
            text = Text(t, size=0.2, stroke_width=0)

            text.next_to(arrow,RIGHT)
            group.add(VGroup(arrow,text))
        return group

class Arrow_TipLength(Scene):
    def construct(self):
        size = np.arange(0,0.41,0.05)

        g = VGroup()
        for s in size:
            s = round(s,2)
            arrow = Arrow(tip_length=s)
            text = Text("tip_length="+str(s), size=0.3, stroke_width=0)
            text.next_to(arrow,RIGHT)
            g.add(VGroup(arrow,text))

        g.to_edge(UP,buff=1)
        g.arrange(DOWN, aligned_edge=LEFT)

        self.add(g)
        self.wait()

class Arrow_TipLength2(Scene):
    def construct(self):
        arrow = Arrow()
        arrow.tip.scale(0.75)  # 화살촉의 크기 조정
        arrow.tip.set_stroke(WHITE, width=5)  # 화살촉의 둘레 선: 흰색이고 width=5
        arrow.tip.set_fill(opacity=0)  # 화살촉 내부를 투명하게

        self.add(arrow)
        self.wait()

class DashedLine_Dash(Scene):
    def construct(self):
        self.simple_dash()
        # self.no_spacing()
        # self.with_spacing()

    def simple_dash(self):
        line_1 = DashedLine(LEFT, RIGHT * 2)

        line_2 = DashedLine(LEFT, RIGHT)
        line_2.set_length(3)

        line_3 = DashedLine(LEFT, UR, color=RED, opacity=0.7, stroke_width=10)
        line_3.set_length(3)

        group = VGroup(line_1, line_2, line_3)
        group.arrange(DOWN)
        self.add(group)
        self.wait()

    def no_spacing(self):
        n = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]

        group = VGroup()
        for k in n:
            text = Text("dash_length=" + str(k), size=0.2, stroke_width=0)
            line = DashedLine(LEFT*3,RIGHT, dash_length=k)
            line.next_to(text,RIGHT)
            group.add(VGroup(text,line))

        group.to_edge(UP,buff=1)
        group.arrange(DOWN, buff=0.5)

        self.add(group)
        self.wait()
        self.remove(group)

    def with_spacing(self):
        n = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]

        group = VGroup()
        for k in n:
            text = Text("dash_length=" + str(k), size=0.2, stroke_width=0)
            line = DashedLine(LEFT*3,RIGHT, dash_length=k,  positive_space_ratio=0.8)
            line.next_to(text,RIGHT)
            group.add(VGroup(text,line))

        group.to_edge(UP,buff=1)
        group.arrange(DOWN, buff=0.5)

        self.add(group)
        self.wait()

class VectorTest(MovingCameraScene):
    def construct(self):
        self.get_vector_test()
        # self.get_angle_test()

    def get_vector_test(self):
        plane = NumberPlane()
        a = np.array([1,3,0])
        b = np.array([2,2,0])

        vector_a = Vector(a)
        vector_b = Vector(b)

        c = Arrow(a,b, buff=0)
        vector_c = Vector(c.get_vector())

        self.add(plane)
        self.add(vector_a, vector_b, c)
        self.play(ShowCreation(vector_c))

        self.wait()

    def get_angle_test(self):
        self.setup() #MovingCameraScene's setup

        plane = NumberPlane()
        a = np.array([1, 3, 0])
        b = np.array([2, 2, 0])

        vector_a = Vector(a)
        vector_b = Vector(b)

        c = Arrow(a, b, buff=0, color=RED)
        vector_c = Vector(c.get_vector(), color=RED)

        angle = c.get_angle()
        arc = Arc(0, angle, radius=0.5)
        angle_text = DecimalNumber(angle / DEGREES).next_to(arc,RIGHT)

        #play
        self.add(plane,c)
        self.play(TransformFromCopy(c,vector_c))

        self.play(
            Succession(
                ShowCreation(arc),
                ShowCreation(angle_text),
            ),
        )
        self.play(self.camera_frame.scale, 0.7,)

        self.wait(3)

class TangentTest(Scene):
    def construct(self):
        circle = Circle()

        t_line = TangentLine(circle,0)

        self.add(circle)
        self.add(t_line)

        self.wait()

class ArcTest(Scene):
    def construct(self):
        # self.default_arc()
        # self.arc_between_test1()
        self.arc_between_test2()

    def default_arc(self):
        arc = Arc()

        self.add(arc)
        self.wait()

    def arc_between_test1(self):
        values = [PI / 8, PI / 4, PI / 2, PI, 3 * PI / 2]
        strs = ["PI/8", "PI/4", "PI/2", "PI", "3*PI/2"]

        def get_arc_text(str, angle_value):
            arc = ArcBetweenPoints(LEFT, RIGHT, angle=angle_value)
            num = Text(str, size=0.35, stroke_width=0).next_to(arc, UP)
            return VGroup(arc, num)

        arcs = VGroup(*[get_arc_text(str, angle_value) for str, angle_value in zip(strs, values)])
        arcs.arrange(RIGHT)

        self.add(arcs)
        self.wait()


    def arc_between_test2(self):
        tracker = ValueTracker(1.15)
        arc = ArcBetweenPoints(LEFT+UP*2,RIGHT+UP*2, angle=TAU/1.15)
        arc = always_redraw(lambda : ArcBetweenPoints(LEFT+UP*2,RIGHT+UP*2, angle=TAU/tracker.get_value()))

        self.add(arc)
        self.play(tracker.set_value, 8, rate_func=there_and_back, run_time=4)
        self.wait()

class PolygonTest(Scene):
    def construct(self):
        # self.simple_polygon()
        # self.simple_regularpolygon()
        # self.simple_regularpolygon2()
        # self.regulat_test3()
        # self.simple_triangle()
        # self.simple_tip()
        # self.simple_rect()
        # self.simple_square()
        # self.simple_rounded_rect()
        self.round_test()

    def simple_polygon(self):
        p = Polygon(UP + LEFT, ORIGIN, DOWN + LEFT, RIGHT)

        self.add(p)
        self.wait()

    def simple_regularpolygon(self):
        p = RegularPolygon()

        self.add(p)
        self.wait()

    def simple_regularpolygon2(self):
        left = RegularPolygon()
        right = RegularPolygon(start_angle=PI / 2)

        self.add(left, right.shift(RIGHT*2))
        self.wait()

    def regulat_test3(self):
        tracker = ValueTracker(3)

        rp = RegularPolygon(3, fill_opacity=1, fill_color=RED)
        num = DecimalNumber(3, num_decimal_places=0).next_to(rp, UP)

        def update_func(mob):
            n = int(tracker.get_value())
            new_mob = RegularPolygon(n, fill_opacity=1, fill_color=RED)
            mob.become(new_mob)
            num.set_value(n)

        self.add(rp, num)
        self.play(
            tracker.set_value, 12,
            UpdateFromFunc(rp, update_func),
            rate_func=linear, run_time=5
        )
        self.wait()

    def simple_triangle(self):
        triangle = Triangle()

        self.add(triangle)
        self.wait()

    def simple_tip(self):
        tip = ArrowTip()

        self.add(tip)
        self.wait()

    def simple_rect(self):
        rect = Rectangle()

        self.add(rect)
        self.wait()

    def simple_square(self):
        square = Square()

        self.add(square)
        self.wait()

    def simple_rounded_rect(self):
        rect = RoundedRectangle()

        self.add(rect)
        self.wait()

    def round_test(self):
        values = [0.1, 0.5, 1, 1.5, 2]

        def get_rect(val):
            rect = RoundedRectangle(corner_radius=val).scale(0.5)
            text = Text(str(val), size=0.3, stroke_width=0).next_to(rect, UP)
            return VGroup(rect, text)

        rects = VGroup(*[get_rect(v) for v in values])
        rects.arrange(RIGHT)

        self.add(rects)
        self.wait()

class ArcTest(Scene):
    def construct(self):
        # self.circle_test()
        # self.simple_ellipse()
        # self.simple_annulus()
        # self.simple_annularsector()
        self.simple_sector()

    def circle_test(self):
        circle1 = Circle(
            radius=1,
            stroke_width=6,
            stroke_color=RED,
            fill_opacity=1.0,
            fill_color=BLUE)
        circle2 = circle1.copy()
        circle2.set_fill(color=RED, opacity=1.0)

        circle1.to_edge(LEFT)
        circle2.to_edge(RIGHT)

        self.add(circle1)
        self.play(
            Transform(circle1, circle2),
            run_time=4,
        )
        self.wait()

    def simple_ellipse(self):
        ellipse = Ellipse()

        self.add(ellipse)
        self.wait()

    def simple_annulus(self):
        annulus = Annulus()

        self.add(annulus)
        self.wait()

    def simple_annularsector(self):
        a_secor = AnnularSector()

        self.add(a_secor)
        self.wait()

    def simple_sector(self):
        sector = Sector()

        self.add(sector)
        self.wait()
