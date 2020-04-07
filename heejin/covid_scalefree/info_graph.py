
from manimlib.imports import *

class InfoGraph(VGroup):
    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        
        t = TexMobject("\\sum { " , "Info" , "Graph" , " }", 
            stroke_width=0, 
            background_stroke_width=0,            
        )
        t[0].set_color(YELLOW)
        t[1].set_color(GREEN)
        t[2].set_color(RED)
        
        e1 = Elbow(width=0.1, stroke_width=3)
        e2 = Elbow(width=0.1, stroke_width=3, angle=PI/2)
        e3 = Elbow(width=0.1, stroke_width=3,angle=PI)
        e4 = Elbow(width=0.1, stroke_width=3,angle=3*PI/2)
        
        e1.move_to(t)
        e2.move_to(t).shift(LEFT)
        e3.move_to(t).shift(LEFT+DOWN*0.6)
        e4.move_to(t).shift(DOWN*0.6)
       
        g = VGroup(e1,e2,e3,e4)
        g.shift(RIGHT*0.17 + UP*0.3)
        
        self.add(g,t)
       
        self.scale(0.3)