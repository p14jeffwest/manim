from manimlib.imports import *
from info_graph import InfoGraph
from manimlib.scene.graph_scene_jeff import GraphScene_Jeff
from manimlib.mobject.number_line_jeff import NumberLine_Jeff

import scipy.interpolate as ip
from scipy.interpolate import  splrep, splev

import datetime
from datetime import timedelta

import pandas as pd

class GrowthFacatorEquation(GraphScene):
    def addInfoGraph(self):
        logo = InfoGraph()
        logo.to_corner(DR)
        self.add(logo)
    
    def construct(self):
        self.addInfoGraph()
        
        self.eq1 = self.showEq1()
        self.eq2 = self.showEq2()
        self.eq3 = self.showEq3()
        
        self.graph1 = self.showGraph1()
        self.showGuide()
        
    def showEq1(self):
        def mTex(str):
            return TexMobject(str).scale(0.9)
            
        Nd = mTex('{ N }_{ d }')        
        C = mTex('C')
        p = mTex('p')
        deltaN = mTex('\\Delta N')
        equal = mTex('=')
        
        eq = VGroup(deltaN,equal,Nd,C,p)
        eq.arrange(RIGHT)
        eq.shift(UP*2.5)
        
        self.play(ShowCreation(Nd),run_time=1.5)
        self.wait(1.5)
        
        self.play(ShowCreation(C),run_time=1.5)
        self.wait(7.5)
        
        self.play(ShowCreation(p),run_time=1.5)
        self.wait(4.5)
        
        self.play(
            ShowCreation(deltaN),
            ShowCreation(equal),
            run_time=2
        )    
        self.wait(4)
        
        eq_right = VGroup(Nd,C,p)
        self.play(Indicate(eq_right))
        self.wait(2)
        
        self.play(Flash(C))
        self.wait(2)
        
        self.play(Flash(p))
        self.wait(4)
        
        return eq
        
    def showEq2(self):
        # 이 수식을 이용해서, 현재의 감염자수를 Nd라고 했을 때(Nd), 
        # 하루가 지난 후인, d+1일째의 감염자수 Nd+1을(Nd+1)을 표현할 수 있습니다.
        def mTex(str):
            return TexMobject(str).scale(0.9)
            
        def mText(str):    
            return Text(str,font='굴림',size=0.4,stroke_width=0)
                        
        Nd1 = mTex('{ N }_{ d+1 }')
        equal = mTex('=')
        Nd = mTex('{ N }_{ d }')
        plus = mTex('+')
        inc = mText('증가분')
        eq2 = VGroup(Nd1,equal,Nd,plus,inc)
        eq2.arrange(RIGHT)
        eq2.next_to(self.eq1,DOWN)
                
        deltaN = mTex('\\Delta N')
        NdCp = mTex('{ N }_{ d }Cp')
        
        self.play(ShowCreation(Nd))
        self.wait(2)
        
        self.play(ShowCreation(Nd1),ShowCreation(equal))
        self.wait(2)
        
        # 하루가 지난 후의 감염자수는 (Nd+1), 현재의 감염자수에(Nd), 현재 감염자에의한 하루사이의 추가 감염자 증가분을 더하면될겁니다.
        # (1일 증가분)
         # (Nd+1 = Nd + 증가분)

       
        self.play(Indicate(Nd1))
        self.wait(2)
        
        self.play(Indicate(Nd))
        self.wait(2)
        
        self.play(
            ShowCreation(plus),
            ShowCreation(inc),
        )        
        self.wait(7)
        
        # 증가분은, 위에서 알아본 수식에 의하면 Nd곱하기 Cp입니다. 
        # (Nd+1 = Nd + NdCp) .
        
        self.wait(1)
        
        deltaN.move_to(inc)
        self.play(ReplacementTransform(inc,deltaN))
        self.wait(1)
        
        NdCp.move_to(deltaN)
        self.play(ReplacementTransform(deltaN,NdCp))
        self.wait(2)
        
        return VGroup(Nd1,equal,Nd,plus,NdCp)
        
    def showEq3(self):
        # 이제, 오른쪽 식을 Nd로 묶으면 이렇게 됩니다. (Nd+1 = (1+Cp)Nd)

        # 즉, Nd+1은 Nd에 어떤 값 (1+Cp)를 곱한 형태가 되고, 이는 현재의 감염자수 Nd에 어떤 값을 곱한 형태로,
        # 바로, 기하급수의 형태가되는 겁니다.
        # (1+Cp = GF)
        # 여기서 1+Cp가 Growh Factor인 겁니다.
        
        def mTex(str,color=WHITE):
            return TexMobject(str,color=color).scale(0.9)
            
        def mText(str):    
            return Text(str,font='굴림',size=0.4,stroke_width=0)
                        
        Nd1 = mTex('{ N }_{ d+1 }')
        equal = mTex('=')
        onePlusCp = mTex('(1+Cp)')
        Nd = mTex('{ N }_{ d }')
        eq = VGroup(Nd1,equal,onePlusCp,Nd)
        eq.arrange(RIGHT)
        eq.next_to(self.eq2,DOWN)
        
        underline = DashedLine(LEFT,RIGHT,color=YELLOW)
        underline.match_width(onePlusCp)
        underline.next_to(onePlusCp,DOWN,buff=0.1)
        
        gf = mTex('GF',YELLOW)
        gf.next_to(underline,DOWN,buff=0.2)
        
        #play
        self.play(ShowCreation(eq), run_time=3)
        self.wait(3)
        
        self.play(Indicate(onePlusCp))
        self.play(ShowCreation(underline))
        self.wait(3)
        
        self.play(ShowCreation(gf))
        self.wait(3)
        
        return VGroup(eq,underline,gf)
        
    def showGraph1(self):  
        def STex(str,color=WHITE):
            return TexMobject(str,color=color).scale(0.7)
        
        p0 = np.array([3.0,-2.0,0])
        p3 = np.array([4.6,0.28,0])
        p2 = np.array([5.0,0.0,0])
        p1 = np.array([5.2,-0.26,0])
        
        Nd = STex('{ N }_{ d }')
        Nd1 = STex('{ N }_{ d+1 }')
        #cross = STex('\\times')
        onePlusCp = STex('GF',YELLOW)
        
        dot_up = Dot(radius=0.07, color=WHITE)
        dot_down = Dot(radius=0.07, color=WHITE)
        
        line1 = Line(p0,p1)
        line2 = Line(p0,p2)
        line3 = Line(p0,p3)
        
        line1.scale(0.8)
        line2.scale(0.8)
        line3.scale(0.8)
        
        #2. 위치        
        dot_up.move_to(line1.get_end())
        dot_down.move_to(line1.get_start())
        
        Nd.next_to(dot_down,DOWN,buff=0.1)
        Nd1.next_to(dot_up,UP,buff=0.1)
        
        onePlusCp.next_to(line1,RIGHT,aligned_edge=LEFT)
        
        #3. play
        # 이처럼 현재의 어떤 값, 여기서는 감염자수인데, 이 어떤 값들이 작용해서 다음 수의 크기를 결정할 때,
        # 이러한 데이터는 기하급수의 모양을 띠게되는겁니다. 
        
        self.play(        
            ShowCreation(Nd),
            ShowCreation(dot_down),
            run_time=2,
        )
        self.wait(5)
        
        self.play(
            ShowCreation(line1),
            ShowCreation(onePlusCp),
            ShowCreation(dot_up),
            ShowCreation(Nd1),
            run_time=2
        )
        self.wait(2)
        
        #GF가 클수록 전염자가 급격하게 증가하는 것이기에, 이 GF를 어떻게 줄이느냐가 전염병의 확산을 막는 관건입니다.
        self.remove(dot_up,dot_down,Nd,Nd1)
        self.play(ReplacementTransform(line1,line2),run_time=1.5)
        self.play(ReplacementTransform(line2,line3),run_time=1.5)
        
        dot_up.move_to(line3.get_end())
        dot_down.move_to(line3.get_start())
        
        Nd.next_to(dot_down,DOWN,buff=0.1)
        Nd1.next_to(dot_up,UP,buff=0.1)
        
        self.play(
            FadeIn(dot_up),FadeIn(dot_down),FadeIn(Nd),FadeIn(Nd1),
        )
        self.wait(2)
        
        return VGroup(dot_down,Nd,line3,onePlusCp,dot_up,Nd1)
        
    def showGuide(self):
        def sTex(str,color=WHITE):
            return TexMobject(str,color=color).scale(0.6)
            
        def sText(str,color=WHITE):    
            return Text(str,font='굴림',size=0.3,stroke_width=0,color=color)
        
        title = sText('* GF를 줄이기 위해서는',YELLOW)
        
        gf = sTex('GF=1+')
        cp = sTex('Cp')
        eq = VGroup(gf,cp)
        eq.arrange(RIGHT)
        
        c_dec = sText('- C의 감소:')
        c_dec_comment = sText('감염자 격리')
        
        p_dec = sText('- p의 감소:')
        p_dec_comment = sText('마스크, 사회적 거리유지')
        
        #위치
        title.shift(LEFT*3)
        eq.next_to(title,DOWN,aligned_edge=LEFT)
        eq.shift(RIGHT*0.5)
        
        c_dec.next_to(eq,DOWN,aligned_edge=LEFT)
        c_dec_comment.next_to(c_dec,RIGHT)
        
        p_dec.next_to(c_dec,DOWN,aligned_edge=LEFT)
        p_dec_comment.next_to(p_dec,RIGHT)
        
        #play
        self.play(FadeIn(title),run_time=1.5)
        self.wait(2)
        
        self.play(FadeIn(eq),run_time=1.5)
        self.wait(2)
        self.play(Indicate(cp))
        self.wait()
        
        self.play(FadeIn(c_dec),run_time=1.5)
        self.wait(2)
        
        self.play(FadeIn(c_dec_comment),run_time=1.5)
        self.wait(2)
        
        self.play(FadeIn(p_dec),run_time=1.5)
        self.wait(2)
        
        self.play(FadeIn(p_dec_comment),run_time=1.5)
        self.wait(4)
CHI=0
JPN=1
THI=2
SIN=3
KOR=4
STATUS_INFECTED =0
STATUS_DEAD = 1
STATUS_CURED=2   
 
class CoronaCountry(VGroup):
    def __init__(self, id=0, color=BLUE_E, **kwargs):
        VGroup.__init__(self, **kwargs)
        
        #text
        COUNTRY_NAME = ['중국','일본','태국','싱가폴','한국',]
        text = Text(COUNTRY_NAME[id], font='굴림',size=0.3,stroke_width=0,color=YELLOW)
        
        #rect
        rect_color=color
        rect = RoundedRectangle(
            width = text.get_width()+0.1, height=text.get_height()+0.1,
            stroke_width=2, stroke_color=WHITE,fill_opacity=1, fill_color=rect_color,
            corner_radius = 0.1,
        )
        
        text.move_to(rect)  
        
        #group
        self.add(rect,text)
        
        self.rect = rect
        self.id = id
        self.text = text
    
    def get_id(self):
        return self.id
        
    def get_width(self):
        return self.rect.get_width()
        
    def get_upper_point(self):
        return self.rect.get_center() + np.array([0,self.rect.get_height()/2.0,0])
        
    def get_down_point(self):    
        return self.rect.get_center() - np.array([0,self.rect.get_height()/2.0,0]) 
        
    def get_down_arrow(self, tgt):
        down_point = self.get_down_point()
        up_point = tgt.get_upper_point()        
        return Arrow(down_point,up_point, stroke_width=2,tip_length=0.15, buff=0)
    
class CoronaPerson(VGroup):
    def __init__(self, id=0, color=BLUE_E, status=STATUS_CURED, **kwargs):
        VGroup.__init__(self, **kwargs)
        
        #circle
        circle_color = color            
        circle = Circle(radius=0.2, stroke_width=2, stroke_color=WHITE, fill_opacity=1, fill_color=circle_color)        
        
        #dot
        if status == STATUS_INFECTED:
            direction = [UL,UR,DL,DR]
            for i in range(0,4):
                dot = Dot(color=ORANGE, radius=0.05)
                dot.move_to(circle, direction[i])
                circle.add(dot)        
                   
        #text        
        if id > 32:
            text = Text("", font='굴림', size=0.1, stroke_width=0,color=YELLOW) 
        else:
            text = Text(str(id), font='굴림', size=0.3, stroke_width=0,color=YELLOW)        
        text.set_height(circle.get_width()-0.2)
        
        text.move_to(circle)  
        
        #group
        self.add(circle,text)
        
        self.circle = circle
        self.id = id
        self.text = text
    
    def get_id(self):
        return self.id
        
    def get_radius(self):
        return self.circle.radius
        
    def get_upper_point(self):
        return self.circle.get_center() + np.array([0,self.circle.radius,0])
        
    def get_down_point(self):    
        return self.circle.get_center() - np.array([0,self.circle.radius,0]) 
        
    def get_down_arrow(self, tgt):
        down_point = self.get_down_point()
        up_point = tgt.get_upper_point()
        
        return Arrow(down_point,up_point, stroke_width=2,tip_length=0.15, buff=0)   
    
  
class InfectedNetwork(Scene):
    def construct(self):
        self.add_logo()
        self.add_title()

        self.super31_group = VGroup() #31번관련 객체 그룹화용
        self.create_network()
        
        self.show_contact_number()
        self.show_table()

        #만약31번이 없었다면
        self.show_if_not_31()

    def show_if_not_31(self):
        self.play(FocusOn(self.super31_group))
        for i in range(3): #3초
            self.play(Indicate(self.super31_group, scale_factor=1.1 ),run_time=0.5)
            self.wait(0.5)

        self.play(FadeOut(self.super31_group),run_time=2)
        self.wait(2)

    def show_table(self):
        def sText(str,color=WHITE):
            return Text(str,color=color,stroke_width=0,font='나눔고딕',size=0.2)
                
        def get_col(s1,s2,s3,s4,s5):
            t1=sText(s1); t2=sText(s2); t3=sText(s3); t4=sText(s4); t5=sText(s5)
            text = VGroup(t1,t2,t3,t4,t5)
            text.arrange(DOWN)
            return text
                
        c1 = get_col(
            '항목',
            '1차 감염자수(N)',
            '평균 접촉자수(C)',
            '감염 확률(p)',
            'GF',
        )
        
        c2 = get_col(
            '31번 포함',
            '19',
            '118',
            '0.67%',
            '1.79',
        )
        
        c3 = get_col(
            '31번 제외',
            '18',
            '99',
            '0.03%',
            '1.02',
        )
        
        
        #position        
        c1.to_edge(LEFT,buff=2)
        c1.shift(DOWN*2)
        c2.next_to(c1,RIGHT,buff=1)
        c3.next_to(c2,RIGHT,buff=1)
        
        #rect
        header = VGroup(c1[0],c2[0],c3[0])
        header_rect = Rectangle(
            width = header.get_width()+1.2, 
            height = header.get_height()+0.2,
            fill_opacity=0.8, color=RED_E,
            stroke_width=0,
        )
        header_rect.move_to(header)
        
        #play
        self.play(
            FadeIn(header_rect),
            FadeIn(c1),
            FadeIn(c2),
            FadeIn(c3),
        )
        self.wait(3)
        
        self.play(Indicate(c2[2],scale_factor=1.3,color=YELLOW,run_time=1.5) )
        self.wait(0.5)
        self.play(Indicate(c2[3],scale_factor=1.3,color=YELLOW,run_time=1) )
        self.wait(0.5)
        self.play(Indicate(c2[4],scale_factor=1.3,color=YELLOW,run_time=1) )
        self.wait(3)
        
        self.play(Indicate(c3[2],scale_factor=1.3,color=YELLOW,run_time=1) )
        self.wait(0.5)
        self.play(Indicate(c3[3],scale_factor=1.3,color=YELLOW,run_time=1) )
        self.wait(0.5)
        self.play(Indicate(c3[4],scale_factor=1.3,color=YELLOW,run_time=1) )
        self.wait(1)
        
        self.play(
            Indicate(c2[2],scale_factor=1.3,color=YELLOW,run_time=1.5),
            Indicate(c2[3],scale_factor=1.3,color=YELLOW,run_time=1.5),
            Indicate(c2[4],scale_factor=1.3,color=YELLOW,run_time=1.5),
            run_time=2,
        )
        
        self.wait(4)
        
        self.play(Flash(self.persons[31]))
        self.play(Indicate(self.persons[31],scale_factor=1.2,color=BLUE_E,run_time=0.5))
        self.play(Indicate(self.persons[31],scale_factor=1.2,color=BLUE_E,run_time=0.5))
        
        self.wait(4)       
    
        
    def show_contact_number(self):
        def sText(str,color=WHITE):
            return Text(str,color=color,stroke_width=0,font='굴림',size=0.2)
            
        #1.remove: countries_text, countries, county2first_line, second2third_line, third_persons
        self.play(
            FadeOut(self.countries_text),FadeOut(self.countries),
            FadeOut(self.county2first_line),FadeOut(self.second2third_line),
            FadeOut(self.third_persons),            
        )
                
        #2.접촉자수 rect
        rect_group = VGroup()
        for p in self.first_persons:
            rect = self.get_contact_rect(p.get_id())
            rect.next_to(p,UP,buff=0.05)
            rect_group.add(rect)

            if(p.get_id() == 31):
                self.super31_group.add(rect)
        
         #3. 접촉자 수 텍스트
        contact_text = sText('접촉자 수')  
        contact_text.next_to(rect_group,LEFT,aligned_edge=LEFT)
        contact_text.to_edge(LEFT,buff=0.4)
        
        #play
        self.add(contact_text)
        self.play(FadeIn(rect_group),run_time=4)
        self.wait(2)
        
        self.play(Indicate(self.first_persons,scale_factor=1.05,color=BLUE_E),run_time=0.5)
        self.play(Indicate(self.first_persons,scale_factor=1.05,color=BLUE_E),run_time=0.5)
        self.wait(4)    
            
    def create_network(self):
        def sText(str,color=WHITE):
            return Text(str,color=color,stroke_width=0,font='굴림',size=0.2)
        
        #입국 국가들
        countries = VGroup()
        for i in range(5):
            countries.add(self.get_country(i))
        countries_text = sText('유입 국가')    
        
        #감염자들
        persons = VGroup()        
        for i in range(0,35): #0:dummy
            persons.add(self.get_person(i))
                
        #1차감염자
        first = [1,2,3,4,5,7,8,12,13,15,16,17,19,23,24,26,27,29,31]
        first_persons = VGroup()
        for i in first:
            first_persons.add(persons[i])
        first_text = sText('1차 감염')   

        #2차 감염자
        second = [6,28,9,14,20,18,22,25,30,33,34]
        second_persons = VGroup()
        for i in second:
            second_persons.add(persons[i])   
        
        #3차 감염자
        third = [10,11,21]
        third_persons = VGroup()
        for i in third:
            third_persons.add(persons[i])    
            
        #31번에 의한
        comment31_0 = sText('약250명',color=YELLOW) 
        comment31_1 = sText('31번 확진자의 경우') 
        comment31_2 = sText('신천지 교회에서의')
        comment31_3 = sText('예배 참석자수 및')
        comment31_4 = sText('감염자 수로 추정')
        comment31 = VGroup(comment31_0,comment31_1,comment31_2,comment31_3,comment31_4)
        comment31.arrange(DOWN,buff=0.2)
                    
        #2. 배치
        countries.arrange(RIGHT,buff=1.5)
        countries.shift(UP*2)
        countries_text.next_to(countries,LEFT,aligned_edge=LEFT)
        countries_text.to_edge(LEFT,buff=0.4)
        
        first_persons.arrange(RIGHT,buff=0.2)        
        first_persons.to_edge(LEFT, buff=1.5)
        first_persons.shift(UP*0.5)
        first_text.next_to(first_persons,LEFT,aligned_edge=LEFT)
        first_text.to_edge(LEFT,buff=0.4)
                
        county2first_line = self.get_country2first(countries,first_persons)  #입국국가 - 1차감염자 
        first2second_line = self.get_first2second(first_persons,second_persons)  #1차 - 2차 
        second2third_line = self.get_second2third(second_persons,third_persons)  #2차-3차 
        
        comment31.to_edge(RIGHT,buff=0.6)
        comment31.shift(DOWN*1.5)
                
        #3. play
        self.play(FadeIn(countries),run_time=1)
        self.play(ShowCreation(county2first_line),run_time=3)
        self.play(FadeIn(first_persons),run_time=1)
        self.add(countries_text,first_text)
        self.wait()
       
        self.play(ShowCreation(first2second_line),run_time=2)
        self.play(FadeIn(second_persons),run_time=0.5)
        self.add(comment31)
                
        self.play(ShowCreation(second2third_line))
        self.play(FadeIn(third_persons),run_time=0.3)
        self.wait(3)
        
        self.play(Flash(persons[29]))
        self.wait(2)
        self.play(Flash(persons[31]))
                
        #for remove: countries_text, countries, county2first_line, second2third_line, third_persons,comment31
        self.countries_text = countries_text
        self.countries = countries
        self.county2first_line = county2first_line
        self.second2third_line = second2third_line
        self.third_persons = third_persons
        self.comment31 = comment31
        self.persons = persons
        
        self.first_persons = first_persons

        self.super31_group.add(persons[31],persons[33],persons[34],comment31)
               
        
    def get_second2third(self, second_persons, third_persons):        
        dic = {
            6:[10,11,21],                      
        }
        
        lines = VGroup()       
        for p1 in second_persons:
            if p1.get_id() in dic:
                left_person = None
                for p2 in third_persons:               
                    if p2.get_id() in dic[p1.get_id()]:
                        if left_person is None:
                            p2.next_to(p1,DOWN,buff=0.35)                            
                            lines.add(p1.get_down_arrow(p2))
                            left_person=p2
                        else:
                            p2.next_to(left_person,RIGHT,buff=0.1)
                            lines.add(p1.get_down_arrow(p2))
                            left_person=p2
                            
        return lines 
        
    def get_first2second(self, first_persons, second_persons):        
        dic = {
            3:[6,28],
            5:[9],
            12:[14],
            15:[20],
            16:[18,22],
            26:[25],
            29:[30],
            31:[33,34],
        }
        
        lines = VGroup()       
        for p1 in first_persons:
            if p1.get_id() in dic:
                left_person = None
                for p2 in second_persons:               
                    if p2.get_id() in dic[p1.get_id()]:
                        if left_person is None:
                            p2.next_to(p1,DOWN,buff=0.35)
                            arrow = p1.get_down_arrow(p2)
                            lines.add(arrow)
                            left_person=p2

                            if p1.get_id() == 31:
                                self.super31_group.add(arrow)
                        else:
                            p2.next_to(left_person,RIGHT,buff=0.1)
                            arrow = p1.get_down_arrow(p2)
                            lines.add(arrow)
                            left_person=p2

                            if p1.get_id() == 31:
                                self.super31_group.add(arrow)
                            
        return lines 
        
    def get_country2first(self,countries, first_persons):        
        map = [
            [1,2,3,4,5,7,8,13,15,23,24,26,27], #중국            
            [12],                               #일본
            [16],                               #태국
            [17,19],                             #싱가폴
            [29,31],                            #한국
        ]
        
        lines = VGroup()
        for c in countries:
            for p in first_persons:               
                if p.get_id() in map[c.get_id()]:
                    lines.add(c.get_down_arrow(p))
        return lines            
    
    def get_person(self,id):
        country_list = [
            KOR, #0 dummy
            CHI, #1
            KOR, #2
            KOR, #3
            KOR, #4
            KOR, #5
            KOR, #6
            KOR, #7
            KOR, #8
            KOR, #9
            KOR, #10
            KOR, #11
            CHI, #12
            KOR, #13
            KOR, #14
            KOR, #15
            KOR, #16
            KOR, #17
            KOR, #18
            KOR, #19
            KOR, #20
            KOR, #21
            KOR, #22
            CHI, #23
            KOR, #24
            KOR, #25
            KOR, #26
            CHI, #27
            CHI, #28
            KOR, #29
            KOR, #30
            KOR, #31
            KOR, #32
            KOR, #33
            KOR, #34
            KOR, #35
            KOR, #36            
        ]
        
        color = [RED_E, GREY,  GREEN_E, ORANGE, BLUE_E, ]
        return CoronaPerson(id, color[country_list[id]]) 
        
    def get_country(self,country_id):
        color = [RED_E, GREY,  GREEN_E, ORANGE, BLUE_E, ]
        return CoronaCountry(country_id, color[country_id])
        
    def get_contact_rect(self, id):
        cnt_list = [
            0,
            45,75,16,95,31,
            17,9,113,2,43,
            0,420,0,3,15,
            438,290,8,67,2,
            6,1,23,0,11,
            0,32,15,114,20,
            460,
        ]
        
        cnt = cnt_list[id]
        
        rect_height = cnt * (1.7/500)  #2.5 Unit : 500명
        
        #rect_opacity = 0 if transparent else 0.8
        rect_opacity = 0.8
        
        rect = Rectangle(           
            width = 0.3,
            height = rect_height, 
            stroke_width = 0,
            fill_opacity = rect_opacity,
            fill_color = GREY,
        )
        cnt_text = Text(str(cnt), size=0.25, font='굴림', stroke_width=0, color=YELLOW)
        cnt_text.next_to(rect,UP,buff=0.05)
        
        
        
        return VGroup(rect,cnt_text)    
    
    def add_logo(self):
        self.logo = logo = InfoGraph()
        logo.to_corner(DR)
        self.add(self.logo)
    
    def add_title(self):
        def mText(str,color=WHITE):
            return Text(str,color=color,stroke_width=0,font='굴림',size=0.4)
        title = mText('COVID19 감염자 네트워크(한국, ~2/19일까지)')  
        title.to_edge(UP,buff=0.5)  
        title.to_edge(LEFT,buff=0.8)
        self.add(title)  


def sText(str,color=WHITE):
    return Text(str,font='굴림',stroke_width=0,color=color,size=0.2)

def mText(str,color=WHITE):
            return Text(str,color=color,stroke_width=0,font='굴림',size=0.4)

def nd_func(x):
    sigma = 30
    mu = 150
    return 70000 * (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

def powerlaw_func(x):
    return 1000.0 * x ** (-1)

class PowerLaw(GraphScene_Jeff):
    CONFIG = {
        "x_axis_label": "",
        "y_axis_label": "",
        "x_min": 0,
        "x_max": 310, #x축을 실제데이터보다 2 칸 더 많게
        "x_tick_frequency":50,
        "x_axis_width": FRAME_WIDTH-2.5,
        
        "y_axis_height": FRAME_HEIGHT-2.5, 
        "y_min": 0,
        "y_max": 1100,         
        "y_tick_frequency": 100,
        "graph_origin":  DOWN * (FRAME_HEIGHT/2-1.2)  + LEFT * (FRAME_WIDTH/2 - 1.2),       
    }

    def setup(self):
        super().setup()
        self.setup_axes()
        
        self.add_x_label()  #x축 라벨        
        self.add_y_label()  #y축 라벨

    def add_x_label(self): 
        x_label = VGroup(*[
            sText(str(i)).next_to(self.x_axis.number_to_point(i),DOWN,buff=0.2)
            for i in range(0,self.x_max,self.x_tick_frequency) 
        ])
        self.x_axis.add(x_label)

    def add_y_label(self):
        y_label = VGroup(*[
            sText(str(i)).next_to(self.y_axis.number_to_point(i),LEFT,buff=0.2)
            for i in range(0,self.y_max,self.y_tick_frequency) if i > 0
        ])
        self.y_axis.add(y_label)

    def construct(self):
        self.add_logo()
        self.add_title()

        # 그래프들: 멱함수, 정규분포
        power_graph = self.get_power_graph()
        power_graph_hidden = self.get_power_graph(color=GREY, opacity=0.3)

        nd_graph = self.get_nd_graph()

        # 1.1 멱함수 그래프
        # self.play(ShowCreation(power_graph))
        # self.wait(2)

        # 1.1 x축 깜빡깜빡: "x축은 얼마나 많은 수의 사람을 감염시켰느냐를 나타냅니다."(4초)
        self.play(Indicate(self.x_axis, scale_factor=1.05))
        self.play(Indicate(self.x_axis, scale_factor=1.05))
        self.wait(3)

        #1.2 즉, 한명을 감염시켰으면 x축의 1의 위치에, 100명을 감염시켰으면 x축의 100을 가리키도록 하고,
        self.move_pointer()

        #1.3 y축은 그러한 사람들의 수, 즉, 한명을 감염시키는 사람들의 빈도수(x=1 점선 왔다 갔다),
        #    100명을 감염시킨 사람들이 얼마나 있는지(x=100...)를 나타내도록하면,
        self.move_pointer_line()

        # 1.4 "그래프의 모양은 이렇게(그래프 그림) 됩니다."
        self.display_powerlaw_graph(power_graph)

        #1.5 x의 값이 작을때 매우 큰 값을 가지고, 그 이후 급격히 수가 작아지긴 하지만,
        #    매우 큰 x값까지도 y값이 존재하는, 매우 긴 꼬리를 가집니다.
        self.show_moving_dot(power_graph)

        #1.6 감염자수를 가지고 그래프를 이해해보면,
        self.show_moving_line(power_graph)

        #1.7 멱함수그래프, Scale Free Network
        self.show_power_law_text()

        #2.1정규분포
        self.play(ReplacementTransform(power_graph, power_graph_hidden), run_time=2)
        self.play(ShowCreation(nd_graph), run_time=4)
        self.wait(3)

        #2.2정규분포 영역 설명
        self.explain_nd_graph(nd_graph, mu=150)

        #2.3 코로나19는, 이러한 정규분포가 아니고, 대다수의 소수전파자와, 약간의 슈퍼전파자로 이루어지는 분포입니다.
        self.play(FadeOut(nd_graph),run_time=2)

        power_graph = self.get_power_graph()
        self.play(ReplacementTransform(power_graph_hidden, power_graph), run_time=2)
        self.show_moving_line(power_graph)
        self.wait(3)

        # self.play(
        #     FadeOut(power_graph), FadeOut(self.x_axis), FadeOut(self.y_axis),
        # )


        # nd_graph = self.get_nd_graph()
        # self.add(nd_graph)

    def explain_nd_graph(self, graph, mu):
        left_max = 90
        right_min = 210
        delta = 10
        gamma = 40
        mu_area = self.get_riemann_rectangles(
            graph,
            x_min=mu - delta, x_max=mu + delta,
            dx=1, stroke_width=0,
        ).set_fill(opacity=0.5, color=RED)

        left_area = self.get_riemann_rectangles(
            graph,
            x_min=left_max-gamma, x_max=left_max,
            dx=1, stroke_width=0,
        ).set_fill(opacity=0.5, color=RED)

        right_area = self.get_riemann_rectangles(
            graph,
            x_min=right_min, x_max=right_min+gamma,
            dx=1, stroke_width=0,
        ).set_fill(opacity=0.5, color=RED)

        # area내에서 라인이 왔다 갔다
        tracker = ValueTracker(0)
        cx = tracker.get_value
        def get_changing_line(type):
            if type == 0:
                k = mu; t=1   #150 -> 160
            elif type == 1:
                k = mu; t=-1  #150 -> 140
            elif type == 2:
                k = mu + delta; t=-1   #160 -> 150
            elif type == 3:
                k = mu - delta; t=1   #140 -> 150
            elif type == 4:
                k = right_min; t=1     #210 -> 250
            elif type == 5:
                k = right_min+gamma; t=-1    #250 -> 210
            elif type == 6:
                k = left_max-gamma; t=1     #50 -> 90
            elif type == 7:
                k = left_max; t=-1    #90 -> 50

            ctp = self.coords_to_point
            return always_redraw(
                lambda : Line(ctp(k+t*cx(),0),
                              ctp(k+t*cx(),graph.underlying_function(k+t*cx())),
                              color=RED, stroke_width=3, stroke_opacity=1,
                              )
            )

        center_to_right = get_changing_line(0)
        center_to_left = get_changing_line(1)
        right_to_center = get_changing_line(2)
        left_to_center = get_changing_line(3)

        minright_to_edge = get_changing_line(4)
        edge_to_minright = get_changing_line(5)
        edge_to_maxleft = get_changing_line(6)
        maxleft_to_edge = get_changing_line(7)

        # play center area
        self.add(mu_area)

        self.add(center_to_right, center_to_left)
        self.play(tracker.set_value, delta, run_time=3)
        self.remove(center_to_right, center_to_left)

        tracker.set_value(0)
        self.add(right_to_center, left_to_center)
        self.play(tracker.set_value, delta, run_time=3)
        # self.play(FadeOut(right_to_center, left_to_center))
        self.remove(right_to_center, left_to_center)

        self.wait()

        # play 가장자리 area
        self.add(left_area, right_area)

        tracker.set_value(0)
        self.add(edge_to_minright, edge_to_maxleft)
        self.play(tracker.set_value, gamma, run_time=2)
        self.remove(edge_to_minright, edge_to_maxleft)

        tracker.set_value(0)
        self.add(minright_to_edge, maxleft_to_edge)
        self.play(tracker.set_value, gamma, run_time=2)
        self.remove(minright_to_edge, maxleft_to_edge)

        tracker.set_value(0)
        self.add(edge_to_minright, edge_to_maxleft)
        self.play(tracker.set_value, gamma, run_time=2)
        self.remove(edge_to_minright, edge_to_maxleft)

        self.wait(3)
        self.remove(mu_area, left_area, right_area)

    def show_power_law_text(self):
        t1 = mText("멱함수 그래프", color=YELLOW)
        t2 = mText(": Scale Free Network의 경우 나타나는 특성")

        t1.shift(UP)
        t2.next_to(t1, DOWN)

        self.play(FadeIn(t1), run_time=3)
        self.play(FadeIn(t2), run_time=4)
        self.wait(3)

        self.remove(t1,t2)

    # x축의 주어진 위치를 가리키는 포인터 생성
    def get_x_pointer(self, x, func, is_line=True):
        triangle = RegularPolygon(n=3, start_angle=np.pi / 2, color=RED, stroke_width=2, stroke_opacity=0.9)
        triangle.set_height(0.25)
        triangle.next_to(self.coords_to_point(x, 0), DOWN, buff=0)

        start = self.coords_to_point(x, 0)
        end = self.coords_to_point(x, func(x))
        line = Line(start, end, color=RED, stroke_opacity=0.9, stroke_width=2)

        group = VGroup(triangle,line) if is_line else triangle
        return group

    def move_pointer(self):
        pointer_1 = self.get_x_pointer(2, powerlaw_func, is_line=False)
        pointer_100 = self.get_x_pointer(100, powerlaw_func, is_line=False)

        self.play(FadeIn(pointer_1))
        self.play(Indicate(pointer_1))
        self.wait(3)
        self.remove(pointer_1)

        self.play(FadeIn(pointer_100),run_time=2)
        self.play(Indicate(pointer_100))
        self.wait(3)
        self.remove(pointer_100)

    def move_pointer_line(self):
        tracker1 = ValueTracker(2)
        changing_pointer1 = always_redraw(
            lambda: self.get_x_pointer(tracker1.get_value(), powerlaw_func)
        )

        tracker2 = ValueTracker(0)
        changing_pointer2 = always_redraw(
            lambda: self.get_x_pointer(100 - tracker2.get_value(), powerlaw_func)
        )

        # 왔다 갔다
        self.add(changing_pointer1)
        self.play(tracker1.set_value, 100, run_time=9)
        self.remove(changing_pointer1)

        self.add(changing_pointer2)
        self.play(tracker2.set_value, 98, run_time=6)
        self.play(FadeOut(changing_pointer2))
        self.wait()

    def show_moving_line(self,graph, is_short=False):
        tracker = ValueTracker(1)
        ctp = self.coords_to_point
        cx = tracker.get_value

        is_reverse = False
        reverse_start = 9

        def get_dotline():
            x = reverse_start - cx() if is_reverse else cx()
            dot = Dot(ctp(x, graph.underlying_function(x)), radius=0.07, fill_color=RED, fill_opacity=0.9)
            line = Line(ctp(x,0),ctp(x,graph.underlying_function(x)),stroke_width=2,color=RED)
            return VGroup(line,dot)

        dotline = always_redraw(get_dotline)

        self.add(dotline)
        run_time = 1 if is_short else 2
        for i in range(2):
            tracker.set_value(1)
            is_reverse = False if i % 2 == 0 else True
            self.play(tracker.set_value, 8, run_time=run_time)

        self.wait()

        # 긴꼬리(8초)
        run_time = 3 if is_short else 1
        tracker.set_value(8)
        is_reverse = False
        self.play(tracker.set_value, 300, run_time=run_time)

        reverse_start = 300
        tracker.set_value(0)
        is_reverse=True
        self.play(tracker.set_value, 50, run_time=1)

        tracker.set_value(250)
        is_reverse = False
        self.play(tracker.set_value, 300, run_time=1)

        self.wait(2)

        self.remove(dotline)

    def show_moving_dot(self, graph):
        tracker = ValueTracker(1)
        ctp = self.coords_to_point
        cx = tracker.get_value

        is_reverse = False
        reverse_start = 11
        def get_dot():
            x = reverse_start-cx() if is_reverse else cx()
            return Dot(ctp(x,graph.underlying_function(x)),radius=0.07,fill_color=RED, fill_opacity=0.9)

        dot = always_redraw(get_dot)

        self.add(dot)
        for i in range(2):
            tracker.set_value(1)
            is_reverse = False if i%2 == 0 else True
            self.play(tracker.set_value, 10, run_time=2)

        self.wait()

        #급격히
        tracker.set_value(1)
        is_reverse = False
        self.play(tracker.set_value, 50, run_time=2)
        self.wait(1.5)

        #긴꼬리(8초)
        reverse_start = 350
        for i in range(3):
            tracker.set_value(50)
            is_reverse = False if i%2 == 0 else True
            self.play(tracker.set_value, 300, run_time=2.5)

        self.wait(2)

        self.remove(dot)

    def display_powerlaw_graph(self, graph):
        self.play(ShowCreation(graph),run_time=3)
        self.wait(2)

    def get_nd_graph(self, color=BLUE_E, opacity=1):
        start_x = 1
        end_x = self.x_max - 10
        return self.get_graph(nd_func, color=color, x_min=start_x, x_max=end_x, stroke_width=4, stroke_opacity=opacity)

    def get_power_graph(self, color=BLUE_E, opacity=1):
        start_x = 1
        end_x = self.x_max - 10

        x0 = range(start_x, end_x + 1)
        y0 = tuple([powerlaw_func(t) for t in x0])

        graph = self.get_graph_from_points(x0, y0, color=color, step_size=0.001, stroke_width=4, stroke_opacity=opacity)
        return graph

    def add_title(self):
        title = mText('무척도 네트워크(Scale Free Network) 그래프')
        title.to_edge(UP, buff=0.5)
        title.to_edge(LEFT, buff=0.8)
        self.add(title)

    def add_logo(self):
        self.logo = logo = InfoGraph()
        logo.to_corner(DR)
        self.add(self.logo)
     
class ScaleFreeNetwork(Scene):
    def construct(self):
        self.add_logo()
        self.add_title()
        self.show_picture()

    def show_picture(self):
        random_pic = ImageMobject("assets/img/random.png")
        free_pic = ImageMobject("assets/img/scalefree.png")

        random_pic.scale(1.5)
        free_pic.scale(1.5)

        pic = Group(random_pic, free_pic)
        pic.arrange(RIGHT)

        random_text = sText("Random Network")
        free_text = sText("Scale Free Network")

        random_text.next_to(random_pic, DOWN)
        free_text.next_to(free_pic, DOWN)
        text = VGroup(random_text, free_text)

        #play
        self.play(
            FadeIn(random_pic),
            FadeIn(random_text),
            run_time=4,
        )
        self.wait(3)

        self.play(
            FadeIn(free_pic),
            FadeIn(free_text),
            run_time=2,
        )

        self.play(Indicate(free_pic,scale_factor=1.1), run_time=0.5)
        self.play(Indicate(free_pic,scale_factor=1.1), run_time=0.5)

        self.wait(1)

    def add_title(self):
        title = mText('사람들 간의 연결 네트워크')
        title.to_edge(UP, buff=0.5)
        title.to_edge(LEFT, buff=0.8)
        self.play(FadeIn(title), run_time=2)

    def add_logo(self):
        self.logo = logo = InfoGraph()
        logo.to_corner(DR)
        self.add(self.logo)


def make_text(str, color=WHITE, size=0.4):
    return Text(str, font='굴림', color=color, size=size, stroke_width=0)

def make_axis_label(str):
    return Text(str, font='굴림', size=0.13, stroke_width=0, color=WHITE)

def make_dotlabel_text(str):
    return Text(str, font='굴림', size=0.13, stroke_width=0, color=YELLOW)

def make_date_list(start_date, end_date):
    oneday = timedelta(days=1)
    d = start_date
    day_list = list()
    while d != (end_date + oneday):
        # day_month = (d.strftime('%d'), d.strftime('%m'))
        day_month = (d.strftime('%d'), d.strftime('%b'))
        day_list.append(day_month)
        d += oneday
    return day_list

# 주어진 시퀀스 x를 받아서, 해당 date 객체 리턴. 0=START_DATE  1=START_DATE+1
def convert_to_date(x):
    # 0 = START_DATE
    s_date = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
    tgt_date = s_date + timedelta(days=x)
    return tgt_date

# date를 받아서 해당 시퀀스 x를 리턴, START_DATE=0
def convert_to_seq(date_str):
    s_date = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
    tgt_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    diff = tgt_date - s_date
    return diff.days

class CoronaKorea(GraphScene_Jeff):
    START_DATE = '2020-1-21'  # 0
    END_DATE = '2020-3-25'  # 64
    X_MAX = 66

    CONFIG = {
        "x_axis_label": "",
        "y_axis_label": "",
        "x_min": 0,
        "x_max": X_MAX,  # x축을 실제데이터보다 2 칸 더 많게
        "x_tick_frequency": 1,
        "x_axis_width": FRAME_WIDTH - 2.5,

        "y_axis_height": FRAME_HEIGHT - 2.5,
        "y_min": 0,
        "y_max": 10000,
        "y_tick_frequency": 1000,
        "graph_origin": DOWN * (FRAME_HEIGHT / 2 - 1.2) + LEFT * (FRAME_WIDTH / 2 - 1.2),
    }

    def setup(self):
        super().setup()
        self.setup_axes()

        self.add_date_on_x()  # 날짜

        self.add_y_label(self.y_axis)

        # self.add_verticle_line()  #날자 구분선
        self.add_horizantal_line()

    def add_date_on_x(self, extend=False):
        group = VGroup()
        tgt_date_list = make_date_list(datetime.datetime.strptime(self.START_DATE, '%Y-%m-%d'),
                                       datetime.datetime.strptime(self.END_DATE, '%Y-%m-%d'))
        # for i,day_month in zip(it.count(),tgt_date_list):
        for i, day_month in enumerate(tgt_date_list):
            if (i % 2 == 0):
                day = make_axis_label(day_month[0])
                month = make_axis_label(day_month[1])
                day.next_to(self.x_axis.number_to_point(i), DOWN, buff=0.2)
                month.next_to(day, DOWN, buff=0.1)

                group.add(day, month)

        day_label = make_axis_label('Day').next_to(group[0], LEFT)
        month_label = make_axis_label('Month').next_to(group[1], LEFT)
        group.add(day_label, month_label)

        self.x_axis.add(group)

    def add_y_label(self, y_axis):
        group = VGroup()
        for i in range(self.y_min, self.y_max + 1, self.y_tick_frequency):
            t = make_axis_label(str(i))
            # t.move_to(self.coords_to_point(0,i),RIGHT)
            t.move_to(y_axis.number_to_point(i), RIGHT)
            t.shift(LEFT * 0.2)

            group.add(t)

        # y_label = make_axis_label('감염자 수').move_to(self.coords_to_point(0,self.y_max),UP)
        y_label = make_axis_label('Confirmed Cases').move_to(y_axis.number_to_point(self.y_max), UP)
        y_label.shift(UP * 0.4)

        group.add(y_label)

        # self.y_axis.add(group)
        y_axis.add(group)

    def add_horizantal_line(self):
        lines = VGroup(*[
            Line(self.coords_to_point(0, y), self.coords_to_point(self.x_max, y), color=GREY, stroke_width=2,
                 stroke_opacity=0.7)
            for y in range(self.y_min + self.y_tick_frequency, self.y_max + 1, self.y_tick_frequency)
        ])

        self.add(lines)
        self.horizantal_lines = lines

    def construct(self):
        self.add_logo()
        self.add_title()

        df = self.read_infected_num_data()
        graph_origin = self.get_korea_graph(df, tgt="KOREA", color=RED_E)
        graph_ifnot31 = self.get_korea_graph(df, tgt="KOREA2", color=BLUE_E)
        t1 = sText("31번 확진자가 발생하지 않았을 경우의 그래프", color=BLUE)
        t1.move_to(self.coords_to_point(49,800))

        #play
        self.play(ShowCreation(graph_origin))
        self.wait()
        self.play(
            ShowCreation(graph_ifnot31),
            FadeIn(t1),
            run_time=2
        )
        self.wait(5)

        self.show_moving_dot(graph_origin)

    def show_moving_dot(self, graph):
        tracker = ValueTracker(1)
        ctp = self.coords_to_point
        cx = tracker.get_value

        def get_dot():
            return Dot(ctp(cx(), graph.underlying_function(cx())), radius=0.07, fill_color=YELLOW, fill_opacity=1)

        dot = always_redraw(get_dot)
        self.add(dot)
        self.play(tracker.set_value,63, run_time=4)

        self.wait(3)

    def get_korea_graph(self, df, tgt="KOREA",color=RED):
        start_x = 0
        end_x = 64

        x0 = range(start_x, end_x + 1)
        y0 = tuple(df[tgt].values.tolist())

        graph = self.get_graph_from_points(x0, y0, color=color, step_size=0.001, stroke_width=4)

        return graph

    def read_infected_num_data(self):
        df = pd.read_excel("한국_코로나 확진수.xlsx",
                           sheet_name='감염자현황(3.25)',
                           header=2,
                           usecols="B:D",
                           )

        return df

    def get_h_line(self, y):
        return Line(self.coords_to_point(0, y), self.coords_to_point(self.x_max, y), color=GREY, stroke_width=2,
                    stroke_opacity=0.7)

    def change_y_axis_scale(self, y_min, y_max, tick_frequency):
        self.y_min = y_min
        self.y_max = y_max
        self.y_tick_frequency = tick_frequency

        # new y_axis
        y_num_range = float(self.y_max - self.y_min)
        self.space_unit_to_y = self.y_axis_height / y_num_range

        y_axis = NumberLine_Jeff(  # by Jeff
            # y_axis = NumberLine(
            is_y_axis=True,  # by Jeff

            x_min=self.y_min,
            x_max=self.y_max,
            unit_size=self.space_unit_to_y,
            tick_frequency=self.y_tick_frequency,
            leftmost_tick=self.y_bottom_tick,
            numbers_with_elongated_ticks=self.y_labeled_nums,
            color=self.axes_color,
            line_to_number_vect=LEFT,
            label_direction=LEFT,
        )
        y_axis.shift(self.graph_origin - y_axis.number_to_point(0))
        y_axis.rotate(np.pi / 2, about_point=y_axis.number_to_point(0))

        self.add_y_label(y_axis)

        self.play(ReplacementTransform(self.y_axis, y_axis), run_time=0.2)

        self.y_axis = y_axis

        # horizantal_lines
        self.play(Transform(self.horizantal_lines, self.get_h_line(0)), run_time=0.3)
        self.remove(self.horizantal_lines)
        self.add_horizantal_line()

    def add_title(self):
        title = mText('한국 코로나19 확진자 수 추이(1/21~3/25)')
        title.to_edge(UP, buff=0.5)
        title.to_edge(LEFT, buff=0.8)
        self.play(FadeIn(title), run_time=2)

    def add_logo(self):
        self.logo = logo = InfoGraph()
        logo.to_corner(DR)
        self.add(self.logo)

class CoronaKorea2(GraphScene_Jeff):
    START_DATE = '2020-1-21'  # 0
    END_DATE = '2020-4-5'  # 75
    X_MAX = 83

    CONFIG = {
        "x_axis_label": "",
        "y_axis_label": "",
        "x_min": 0,
        "x_max": X_MAX,  # x축을 실제데이터보다 2 칸 더 많게
        "x_tick_frequency": 1,
        "x_axis_width": FRAME_WIDTH - 2.5,

        "y_axis_height": FRAME_HEIGHT - 2.5,
        "y_min": 0,
        "y_max": 50000,
        "y_tick_frequency": 10000,
        "graph_origin": DOWN * (FRAME_HEIGHT / 2 - 1.2) + LEFT * (FRAME_WIDTH / 2 - 1.2),
    }

    def setup(self):
        super().setup()
        self.setup_axes()

        self.add_date_on_x()  # 날짜

        self.add_y_label(self.y_axis)

        # self.add_verticle_line()  #날자 구분선
        self.add_horizantal_line()

    def add_date_on_x(self, extend=False):
        group = VGroup()
        tgt_date_list = make_date_list(datetime.datetime.strptime(self.START_DATE, '%Y-%m-%d'),
                                       datetime.datetime.strptime(self.END_DATE, '%Y-%m-%d'))
        # for i,day_month in zip(it.count(),tgt_date_list):
        for i, day_month in enumerate(tgt_date_list):
            if (i % 2 == 0):
                day = make_axis_label(day_month[0])
                month = make_axis_label(day_month[1])
                day.next_to(self.x_axis.number_to_point(i), DOWN, buff=0.2)
                month.next_to(day, DOWN, buff=0.1)

                group.add(day, month)

        day_label = make_axis_label('Day').next_to(group[0], LEFT)
        month_label = make_axis_label('Month').next_to(group[1], LEFT)
        group.add(day_label, month_label)

        self.x_axis.add(group)

    def add_y_label(self, y_axis):
        group = VGroup()
        for i in range(self.y_min, self.y_max + 1, self.y_tick_frequency):
            t = make_axis_label(str(i))
            # t.move_to(self.coords_to_point(0,i),RIGHT)
            t.move_to(y_axis.number_to_point(i), RIGHT)
            t.shift(LEFT * 0.2)

            group.add(t)

        # y_label = make_axis_label('감염자 수').move_to(self.coords_to_point(0,self.y_max),UP)
        y_label = make_axis_label('Confirmed Cases').move_to(y_axis.number_to_point(self.y_max), UP)
        y_label.shift(UP * 0.4)

        group.add(y_label)

        # self.y_axis.add(group)
        y_axis.add(group)

    def add_horizantal_line(self):
        lines = VGroup(*[
            Line(self.coords_to_point(0, y), self.coords_to_point(self.x_max, y), color=GREY, stroke_width=2,
                 stroke_opacity=0.7)
            for y in range(self.y_min + self.y_tick_frequency, self.y_max + 1, self.y_tick_frequency)
        ])

        self.add(lines)
        self.horizantal_lines = lines

    def construct(self):
        self.add_logo()
        # self.add_title()

        df = self.read_infected_num_data()
        graph = self.get_korea_graph(df, tgt="KOREA", color=GREEN, start=0, end=75)
        graph_expected = self.get_korea_graph(df, tgt="expected", color=GREEN,start=0,end=83)
        graph_worst = self.get_korea_graph(df, tgt="worst", color=GREEN,start=0,end=83)

        #play
        self.play(ShowCreation(graph), run_time=5)
        self.wait(2)

        self.play(ReplacementTransform(graph, graph_worst), run_time=5)
        self.wait(2)
        self.play(ReplacementTransform(graph_worst, graph_expected), run_time=2)
        self.wait(4)

        # self.show_moving_dot(graph_expected)

    def show_moving_dot(self, graph):
        tracker = ValueTracker(1)
        ctp = self.coords_to_point
        cx = tracker.get_value

        def get_dot():
            return Dot(ctp(cx(), graph.underlying_function(cx())), radius=0.07, fill_color=YELLOW, fill_opacity=1)

        dot = always_redraw(get_dot)
        self.add(dot)
        self.play(tracker.set_value,63, run_time=4)

        self.wait(3)

    def get_korea_graph(self, df, tgt="KOREA",start=0, end=64,color=RED):
        start_x = start
        end_x = end

        x0 = range(start_x, end_x + 1)
        len_x = len(x0)
        y0 = tuple(df[tgt].values.tolist()[0:len_x])

        # print("len x0", len(x0))
        # print("len y0", len(y0))

        graph = self.get_graph_from_points(x0, y0, color=color, step_size=0.001, stroke_width=4)

        return graph

    def read_infected_num_data(self):
        df = pd.read_excel("한국_코로나 확진수.xlsx",
                           sheet_name='감염자현황(3.25)',
                           header=2,
                           usecols="B:F",
                           )

        return df

    def get_h_line(self, y):
        return Line(self.coords_to_point(0, y), self.coords_to_point(self.x_max, y), color=GREY, stroke_width=2,
                    stroke_opacity=0.7)

    def change_y_axis_scale(self, y_min, y_max, tick_frequency):
        self.y_min = y_min
        self.y_max = y_max
        self.y_tick_frequency = tick_frequency

        # new y_axis
        y_num_range = float(self.y_max - self.y_min)
        self.space_unit_to_y = self.y_axis_height / y_num_range

        y_axis = NumberLine_Jeff(  # by Jeff
            # y_axis = NumberLine(
            is_y_axis=True,  # by Jeff

            x_min=self.y_min,
            x_max=self.y_max,
            unit_size=self.space_unit_to_y,
            tick_frequency=self.y_tick_frequency,
            leftmost_tick=self.y_bottom_tick,
            numbers_with_elongated_ticks=self.y_labeled_nums,
            color=self.axes_color,
            line_to_number_vect=LEFT,
            label_direction=LEFT,
        )
        y_axis.shift(self.graph_origin - y_axis.number_to_point(0))
        y_axis.rotate(np.pi / 2, about_point=y_axis.number_to_point(0))

        self.add_y_label(y_axis)

        self.play(ReplacementTransform(self.y_axis, y_axis), run_time=0.2)

        self.y_axis = y_axis

        # horizantal_lines
        self.play(Transform(self.horizantal_lines, self.get_h_line(0)), run_time=0.3)
        self.remove(self.horizantal_lines)
        self.add_horizantal_line()

    def add_title(self):
        title = mText('한국 코로나19 확진자 수 추이(1/21~3/25)')
        title.to_edge(UP, buff=0.5)
        title.to_edge(LEFT, buff=0.8)
        self.play(FadeIn(title), run_time=2)

    def add_logo(self):
        self.logo = logo = InfoGraph()
        logo.to_corner(DR)
        self.add(self.logo)

class Airport(Scene):
    def construct(self):
        self.add_logo()
        self.add_title()

        #항공네트워크 (13초)
        airport_network = self.get_airport_network_image()
        self.play(FadeIn(airport_network), run_time=3)
        self.wait()
        self.play(FadeOut(airport_network))

        world_map = self.get_world_korea_map()
        self.play(FadeIn(world_map), run_time=2)
        # self.draw_grid()

        self.draw_everywhere()
        self.draw_using_hub()
        self.remove(world_map)

        self.play(FadeIn(airport_network), run_time=2)
        # self.draw_grid()
        self.draw_hub_blink()

        self.wait()


    def draw_hub_blink(self):
        def get_circle(p, color=RED, stroke_color = YELLOW):
            circle= Circle(
                radius=0.15, fill_opacity=0.8, color=color,
                stroke_opacity=1, stroke_color=stroke_color, stroke_width=2,
            )
            circle.move_to(np.array([p[0] / 10.0, p[1] / 10.0, 0]))
            return circle
        points = [
            (-1.1, 11), (9.5, 12), (-27, 8), (-26.2, 6), (-25, 3), (-26, -7.8), (-15, -11), (7, -12), (9.5, 12),
            (13.5, 6.2), (14.5, 4.2), (20, 1.5), (28, 0), (29.2, -6.8), (32, 2.5), (32.5, 7.5), (38.5, 7), (-30.5, 1.5),
            (-36, 5.8), (-18.5, -14.5)

        ]

        circles = VGroup()
        for p in points:
            circle = get_circle(p)
            circles.add(circle)

        dark_circles = VGroup()
        for p in points:
            circle = get_circle(p, color=BLACK, stroke_color=BLACK)
            dark_circles.add(circle)

        self.play(FadeIn(circles), run_time=2)
        self.play(Indicate(circles, scale_factor=1.1))
        self.wait(0.5)
        self.play(Indicate(circles, scale_factor=1.1))
        self.wait(4)

        self.play(ReplacementTransform(circles, dark_circles), run_time=5)
        self.wait(6)


    def get_arc(self, s,e):
        angle = TAU/8
        if s[1] > e[1]:
            angle = -(TAU/8)
        return ArcBetweenPoints(
            np.array([s[0]/10.0, s[1]/10.0, 0]),
            np.array([e[0]/10.0, e[1]/10.0, 0]),
            angle=angle, stroke_width=1.5, color=YELLOW,
        )

    def draw_using_hub(self):
        seoul = (29, 3.5)
        london = (1,5)
        points = [
            (3, 8), (1, 10), (1, 9), (1, 8), (4, 7), (5, 7), (6, 7), (5, 3), (6, 3), (7, 4), (8, 5), (4, 4), (4.5, 4.5),
            (8, 3), (8, 3.5), (9, 4), (4, 3), (4.5, 3), (1, 11), (1, 11.5), (1, 12.1), (1, 12.3), (4, 10), (4, 10.1),
            (4, 10.3), (4, 10.5), (-4, 3), (-4, 3.1), (-4, 3.3), (1, 4), (3, 13), (3, 13.1), (3, 12), (3, 12.5),
            (3.1, 12), (3.3, 11), (3.4, 10.9)

        ]

        arc_seoul = self.get_arc(seoul,london)
        arcs = VGroup()
        for p in points:
            arc = self.get_arc(london,p)
            arcs.add(arc)

        self.play(ShowCreation(arc_seoul), run_time=5)
        self.wait(2)

        self.play(ShowCreation(arcs), run_time=7)
        self.wait(3)

        self.remove(arcs, arc_seoul)

    def draw_everywhere(self):
        seoul = (29,3.5)
        points = [
            (-35, 18), (-32, 15), (-31, 17), (-28, -1), (-26, 15), (-26, 14), (-26, 13), (-26, 11), (-23, 11),
            (-18, -22), (-20, 5), (-20, 4), (-20, 3), (-18, 8), (-17, -6), (-17, -8), (-17, -10), (-17, -17),
            (-15, -11), (-12, 23), (-11, 21), (-10, 20), (-10, 16), (-8, 17), (0, 5), (0, 0), (0, -1), (0, -3), (1, -3),
            (1, -4), (1, -5), (2, -5), (5, -10), (5, -11), (5, -12), (8, -6), (9.5, 8), (10, 10), (11, 9), (12, 8),
            (13, 7), (14, 6), (15, 5), (15, 15), (15, 14), (16, 13), (23, -4), (23, -5), (25, 17), (25, 18), (30, 18),
            (30, -12), (31, -13), (31, -15), (31, 2), (32, -14), (32, 7), (33, 12), (33, -8), (33, -12), (34, 12),
            (35, -15), (40, -20), (-30, 10), (-29, 9), (-28, 8), (-27, 7), (-26, 6), (-25, 5), (-24, 4), (-23, 3),
            (-22, 7), (10, 2), (11, 2), (13, 2), (14, 3), (30, 19), (30, 18), (31, 18), (34, 17), (5, -15), (5, -14),
            (5, -16), (5, -12), (5, -11), (5, -10), (5, -9), (5, -8), (6, -7), (7, -6), (-19, -20), (-19, -17),
            (-21, -8), (-28, 3), (-28, 5), (-30, 5), (-28, 13), (25, 15), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1),
            (8, 0), (22, 17), (22, 16), (22, 15), (22, 14), (22, 13), (22, 12), (22, 11), (-5, 1), (-4, 1), (-3, 1),
            (-2, 1), (33, 20), (-18, -20), (-18, -19), (-18, -18), (-18, -17), (-18, -16), (-18, -15), (-18, -14),
            (-17, -18), (-17, -17), (-17, -16), (-17, -15), (-17, -14), (0, 6), (1, 6), (2, 6), (3, 5), (4, 6), (5, 6),
            (6, 7), (-16, 21),
        ]

        arcs = VGroup()
        for p in points:
            arc = self.get_arc(seoul,p)
            arcs.add(arc)

        self.play(ShowCreation(arcs), run_time=7)
        self.wait(2)
        self.play(FadeOut(arcs))

    def get_world_map(self):
        map = ImageMobject("assets/img/worldmap_empty.png")
        map.scale(2.5)
        return map

    def get_world_korea_map(self):
        map = ImageMobject("assets/img/worldmap_korea.png")
        map.scale(2.5)
        return map

    def draw_grid(self):
        def miniText(str, color=WHITE):
            return Text(str,font='굴림',stroke_width=0,color=color,size=0.15)

        def get_line(s,e):
            return Line(s, e, color=GREY, stroke_width=1,)

        def get_thick_line(s, e):
            return Line(s, e, color=RED, stroke_width=1)


        x_min = -70
        x_max = 70
        y_min = -40
        y_max = 40

        v_lines = VGroup()
        x_labels = VGroup()
        for x in range(x_min, x_max+1):
            if x % 10 == 0 :
                line = get_thick_line(np.array([x/10.0,y_min/10.0,0]), np.array([x/10.0,y_max/10.0,0]),)
            else:
                line = get_line(np.array([x / 10.0, y_min / 10.0, 0]), np.array([x / 10.0, y_max / 10.0, 0]), )
            v_lines.add(line)

            if x % 5 == 0:
                t = miniText(str(x))
                t.move_to(np.array([x/10.0,(y_min+10)/10.0,0]))
                x_labels.add(t)

        h_lines = VGroup()
        y_labels = VGroup()
        for y in range(y_min, y_max+1):
            if y % 10 == 0:
                line = get_thick_line(np.array([x_min / 10.0, y / 10.0, 0]), np.array([x_max / 10.0, y / 10.0, 0]), )
            else:
                line = get_line(np.array([x_min/10.0,y/10.0,0]), np.array([x_max/10.0,y/10.0,0]),)

            h_lines.add(line)

            if y%5 == 0:
                t = miniText(str(y))
                t.move_to(np.array([(x_min+10)/10.0, y/10.0,0]))
                y_labels.add(t)

        self.add(v_lines, h_lines)
        self.add(x_labels, y_labels)

    def get_airport_network_image(self):
        airport_network = ImageMobject("assets/img/airport2.jpg")
        airport_network.scale(2.3)

        t = sText("출처:phys.org")
        t.next_to(airport_network, DOWN, aligned_edge=LEFT, buff=0.2)

        return Group(airport_network,t)

    def add_title(self):
        title = mText('전 세계 항공 네트워크')
        title.to_edge(UP, buff=0.5)
        title.to_edge(LEFT, buff=0.8)
        self.play(FadeIn(title), run_time=2)

    def add_logo(self):
        self.logo = logo = InfoGraph()
        logo.to_corner(DR)
        self.add(self.logo)
