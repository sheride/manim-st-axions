from manim import *
from manim_slides import Slide
import numpy as np
import scipy.interpolate

class Slides(Slide):
    def construct(self):
        def formatText(string, scale, color):
            return Text(string).set_color(color).scale(scale)
        
        def makeEllipse(color):
            return Ellipse(width=2.5, height=2.5, fill_opacity=0.5, color=color, stroke_width=10)
            
        def parametricUpdater(f, g, ax, t):
            return lambda a: a.move_to(ax.c2p(f(t.get_value()), g(t.get_value())))

        def update_path(path, dot):
                previous_path = path.copy()
                previous_path.add_points_as_corners([dot.get_center()])
                path.become(previous_path)

        def pathUpdater(dot):
            return lambda p: update_path(p, dot)

        def sweepCurveSetup(vt, ax, x, y, color=WHITE):
            init = ax.coords_to_point(x(vt.get_value()), y(vt.get_value()))
            dot = Dot(point=init, color=color)
            dot.z_index = 2
            dot.add_updater(parametricUpdater(x, y, ax, vt))
            path = VMobject(stroke_color=color)
            path.set_points_as_corners([dot.get_center(), dot.get_center()])
            path.add_updater(pathUpdater(dot))
            path.z_index = 2
            
            return dot, path
            
        def KahlerConeMF(paths, kahler_vertices, stretched_vertices, 
                         x_range, y_range, kx_range, ky_range, num_axions):
            header = Title("Axion Parameters as Function of Moduli Space", color=WHITE)
            self.add(header.to_edge(UP))
            self.next_slide()
            
            # import axion data
            xs = [[np.loadtxt(f'{p}/x_{i+1}.txt') for i in range(num_axions)] for p in paths]
            ys = [[np.loadtxt(f'{p}/y_{i+1}.txt') for i in range(num_axions)] for p in paths]
            ks = np.array([[np.loadtxt(f'{p}/k_{i+1}.txt') for i in range(2)] for p in paths])

            # generate axes
            plot_ax = Axes(
                x_range=x_range, 
                y_range=y_range,
                axis_config={"include_tip": False, 'include_numbers': True})
            k_ax = Axes(
                x_range=kx_range, 
                y_range=ky_range,
                axis_config={"include_tip": False, 'include_numbers': True})
            # VGroup(plot_ax, k_ax).arrange(LEFT, buff=1).scale_to_fit_width(12)
            
            header_text = ['Moduli Space', 'Axion Parameter Space']
            header_text_ob = [Text(t).scale(1) for t in header_text]
            master = Group(*header_text_ob, k_ax, plot_ax).arrange_in_grid(
                2, 2, buff=2, col_alignments=['c']*2, row_alignments=['c']*2)
            master.scale_to_fit_width(13).next_to(header, DOWN).shift(DOWN)
            
            plot_xlabel = plot_ax.get_x_axis_label("\log_{10}(m_a)", edge=DOWN, direction=DOWN)
            plot_ylabel = plot_ax.get_y_axis_label("\log_{10}(f)", edge=UP, direction=UP)
            k_xlabel = k_ax.get_x_axis_label("\\tau_{1}", edge=DOWN, direction=DOWN)
            k_ylabel = k_ax.get_y_axis_label("\\tau_{2}", edge=UP, direction=UP)
            ax_related = [plot_ax, plot_xlabel, plot_ylabel, k_ax, k_xlabel, k_ylabel]

            # cones
            k_cone, s_cone = [
                Polygon(*[k_ax.c2p(*i) for i in v]) for v in [kahler_vertices,
                                                              stretched_vertices]]
            k_cone.stroke_width = 0
            k_cone.set_fill(GREY, opacity=1)
            k_cone.z_index = 0
            s_cone.stroke_width = 0
            s_cone.set_fill(PURPLE_A, opacity=0.5)
            s_cone.z_index = 1

            # interpolate
            x_fs = [[scipy.interpolate.interp1d(row2[0], x, bounds_error=False, fill_value=x[-1]) for x in row1] for row1, row2 in zip(xs, ks)]
            y_fs = [[scipy.interpolate.interp1d(row2[0], y, bounds_error=False, fill_value=y[-1]) for y in row1] for row1, row2 in zip(ys, ks)]
            k_fs = [[scipy.interpolate.interp1d(row2[0], k, bounds_error=False, fill_value=k[-1]) for k in row1] for row1, row2 in zip(ks, ks)]

            # set up moving dots
            ts = [ValueTracker(row[0][0]) for row in ks]
            colors = [BLUE, RED, GREEN, PURPLE]
            xy_dots_paths = [[sweepCurveSetup(t, plot_ax, f, g, color=c) for f, g in zip(row1, row2)] for t, c, row1, row2 in zip(ts, colors, x_fs, y_fs)]
            k_dots_paths = [sweepCurveSetup(t, k_ax, row[0], row[1], color=c) for t, row, c in zip(ts, k_fs, colors)]

            # animate
            self.wait(1)
            self.next_slide()
            self.add(
                *ax_related, 
                *[c for a in xy_dots_paths for b in a for c in b], *[b for a in k_dots_paths for b in a],
                *header_text_ob)
            self.wait(1)
            self.next_slide()
            self.play(FadeIn(k_cone))
            self.next_slide()
            self.play(FadeIn(s_cone))
            self.next_slide()
            for t, row in zip(ts, ks):
                self.play(t.animate.set_value(row[0][-1]), run_time=5)
                self.next_slide()
            self.wait()
        
        def A_Title():
            # Title
            title = VGroup(
                Text("Manim Slides").scale(3),
                Text("A Case Study via String Theory & Axions"),
            ).arrange(DOWN)

            # Manim Slides Logo
            logo = ImageMobject("./images/manim_slides_white_logo.png").scale(0.75).next_to(title,DOWN)

            # Positioning
            group = Group(title, logo).arrange(DOWN, buff=1).scale_to_fit_height(6)

            # Animation
            self.wait(1)
            self.next_slide()
            self.play(FadeIn(title.submobjects[0]))
            self.next_slide()
            self.play(FadeIn(title.submobjects[1]))
            self.next_slide()
            self.play(FadeIn(logo))
            self.next_slide()
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
            
        def B_TOC():
            # Header
            header = Title("Talk Overview", color=WHITE)
            self.add(header.to_edge(UP))

            # Main Bullets
            bullets = [
                "1. Intro to Manim & Manim Slides",
                "2. Axions & String Theory in 30 s",
                "3. Axion Parameters and Moduli Space",
                "4. Conclusion"]
            bullet_group = VGroup(*[formatText(b, 0.8, WHITE) for b in bullets]).arrange(
                direction=DOWN, aligned_edge=LEFT, buff=0.5)

            # Subbullets
            subbullets = [
                ["What are these libraries?",
                 "What can they do?",
                 "Why should I use them?"],
                ["What are string theory's parameters?",
                 "What's an axion?"],
                ["Visualization of abstract,\n" 
                 + "higher-dimensional spaces"],
                ["How does this relate to scientific communication?"]]
            subbullets_groups = [
                VGroup(*[formatText(sb, 0.6, GREY) for sb in sb_set]).arrange(
                direction=DOWN, aligned_edge=LEFT, buff=0.25).next_to(b, DOWN, buff=0.5).align_to(b, LEFT)
                for sb_set, b in zip(subbullets, bullet_group)]

            # Animation
            self.wait(1)
            self.next_slide()
            for b, sb_group in zip(bullet_group.submobjects, subbullets_groups):
                self.play(Write(b))
                self.next_slide()
                for sb in sb_group.submobjects:
                    self.play(FadeIn(sb))
                    self.next_slide()
                self.play(FadeOut(sb_group))
                b.set_opacity(0.5)
            bullet_group.set_opacity(1)
            self.next_slide()
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
            
        def C_ManimIntro():
            header = Title("What is Manim?", color=WHITE)
            self.wait(1)
            self.add(header.to_edge(UP))
            self.next_slide()

            bullets = [
                '   - Manim is a Python package for mathematical animations\n' + 
                '     developed by Grant Sanderson for math education YouTube\n' +
                '     channel 3Blue1Brown (since ~2015)',
                '   - In particular, Manim permits diverse, precise animations\n' +
                '     of Tex(t), shapes, graphs, vectors, and more',
                '   - ManimGL is a fork of the original code, maintained by the\n' + 
                '     3b1b community for public use (since 2020)',
                '   - ManimSlides is an extension of ManimGL designed for making\n' + 
                '     presentations']
            bullet_group = VGroup(
                *[formatText(b, 0.6, WHITE) for b in bullets]).arrange(
                direction=DOWN, aligned_edge=LEFT, buff=0.5).next_to(header, DOWN).shift(DOWN * 0.5)

            image_3b1b_header = ['Linear Algebra', 'Calculus', 'Misc. Math']
            image_3b1b_text = [
                formatText(h, 0.6, BLUE) for h in image_3b1b_header]
            image_3b1b_text_group = Group(*image_3b1b_text).arrange(RIGHT, buff=2.5).next_to(bullet_group[0], DOWN).shift(DOWN * 0.5)
            image_names_3b1b = [f'./images/3b1b_{f}' for f in ['cross_product', 'integration', 'triples']]
            images_3b1b = [
                ImageMobject(name).scale(0.4).next_to(t, DOWN) 
                for name, t in zip(image_names_3b1b, image_3b1b_text_group)]
            images_3b1b_group = Group(*images_3b1b)# .arrange(RIGHT, buff=1).next_to(DOWN)

            self.play(FadeIn(bullet_group[0]))
            self.next_slide()
            for i, t in zip(images_3b1b_group, image_3b1b_text):
                self.play(FadeIn(i, t))
                self.next_slide()
            self.play(FadeOut(*images_3b1b_group, *image_3b1b_text))
            self.next_slide()

            self.play(FadeIn(bullet_group[1]))
            self.next_slide()
            self.play(FadeIn(bullet_group[2]))
            self.next_slide()
            self.play(FadeIn(bullet_group[3]))
            self.next_slide()
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
            
        def D_WhyManim():
            header = Title("Motivating Manim: What Goes Into A Talk?", color=WHITE)
            self.add(header.to_edge(UP))
            self.wait(1)
            self.next_slide()

            circle_names = [
                'Slide Design',
                'Typesetting',
                'Computation'
            ]

            circleSlide = makeEllipse(BLUE).shift(LEFT)
            circleType  = makeEllipse(RED).shift(RIGHT)
            circleComp  = makeEllipse(YELLOW).shift(DOWN * 1.5)
            circles = [circleSlide, circleType, circleComp]

            circle_text = []
            for c, t, d, shift in zip(circles, circle_names, [UP, UP, DOWN], [0.5 * LEFT, 0.5 * RIGHT, None]):
                circle_text.append(Text(t).scale(0.75).next_to(c, d))
                if shift is not None:
                    circle_text[-1].shift(shift)

            circle_group = VGroup(*circles)
            # circle_text_group = VGroup(*circles, *circle_text).next_to(header, DOWN)

            for c, t in zip(circles, circle_text):
                self.play(FadeIn(c, t))
                self.next_slide()

            leftText = Text('We can do these\nseparately...').next_to(header, DOWN).to_edge(LEFT).shift(DOWN * 0.5 + LEFT * 0.5).scale(0.5)
            rightText = Text('But integrated\ntools can be nicer!').next_to(header, DOWN).to_edge(RIGHT).shift(DOWN * 0.5 + RIGHT * 0.5).scale(0.5)

            leftLogoFiles = ['powerpoint', 'latex_white', 'python']        
            rightLogoFiles = ['beamer_transparent', 'mathematica', 'manim_slides_white']

            logos = []
            for logoList in [leftLogoFiles, rightLogoFiles]:
                temp = []
                for name in logoList:
                    temp.append(ImageMobject(f'./images/{name}_logo.png'))
                    temp[-1].scale(1 / temp[-1].get_width())
                logos.append(temp)

            leftLogos, rightLogos = logos
            rightLogos[-1].scale(2)

            self.play(Write(leftText))
            self.next_slide()

            temp = leftText
            mini_circles = []
            for c, logo, color in zip(circles, leftLogos, [BLUE, RED, YELLOW]):
                mini_circles.append(Difference(c, Union(*[d for d in circles if d != c]), color=color, fill_opacity=0.5))
                self.play(mini_circles[-1].animate.scale(0.3).next_to(temp, DOWN, buff=0.75))
                self.next_slide()
                temp = mini_circles[-1]
                self.play(FadeIn(logo.next_to(temp, RIGHT)))
                self.next_slide()

            ints = [Difference(Intersection(circleSlide, circleType), circleComp, color=PURPLE, fill_opacity=0.5), 
                    Difference(Intersection(circleType,  circleComp), circleSlide, color=ORANGE, fill_opacity=0.5), 
                    Intersection(*circles, color=DARK_BROWN, fill_opacity=0.5)]

            self.play(Write(rightText))
            self.next_slide()

            temp = rightText
            for i, logo, scale in zip(ints, rightLogos, [0.75, 0.5, 1.5]):
                self.play(i.animate.scale(scale).next_to(temp, DOWN, buff=0.75))
                self.next_slide()
                temp = i
                self.play(FadeIn(logo.next_to(temp, LEFT)))
                self.next_slide()

            emphasis = Group(rightLogos[-1], ints[-1])
            green_box = SurroundingRectangle(emphasis, color=GREEN, buff=0.2, stroke_width=10)
            everything_else = circles + circle_text + mini_circles + ints[:-1] + [
                leftText, rightText] + leftLogos + rightLogos[:-1]

            self.play(Create(green_box))
            self.next_slide()
            self.play(emphasis.animate.center().scale(4), 
                      FadeOut(green_box),
                      *[a.animate.set_opacity(0.1) for a in everything_else])
            self.next_slide()
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
        
        def E_IntroToString1():
            header = Title("String \& Axions in 30 s, Pt 1", color=WHITE)
            self.add(header.to_edge(UP))
            self.wait(1)
            self.next_slide()

            bullets = [
                '   - String theory models quantum gravity (1D strings > 0D pt. particles)',
                '   - String theory demands 10D spacetime, real life features 4 (large) D:\n' +
                '     reconcile with 4 large, 6 small',
                '   - Small 6D shape = topology (# of holes) + geometry (hole sizes)',
                '   - Geometry parameterized by moduli spaces, strongly influences 4D physics\n',
                '   - Axions are light, weakly coupled, massive scalar particles predicted\n' + 
                '     generically by string theory',]
            bullet_group = VGroup(
                *[formatText(b, 0.6, WHITE) for b in bullets]).arrange(
                direction=DOWN, aligned_edge=LEFT, buff=0.5).next_to(header, DOWN).shift(DOWN * 0.5)
            
            self.play(FadeIn(bullet_group[0]))
            self.next_slide()
            a = ImageMobject('./images/string_white').next_to(bullet_group[0], DOWN, buff=0.5)
            self.play(FadeIn(a))
            self.next_slide()
            self.play(FadeOut(a))
            self.next_slide()
            self.play(FadeIn(bullet_group[1]))
            self.next_slide()
            self.play(FadeIn(bullet_group[2]))
            self.next_slide()
            b = ImageMobject('./images/cy1')
            b.scale(1.5 / b.get_width())
            c = ImageMobject('./images/cy2')
            c.scale(1.5 / c.get_width())
            group = Group(b, c).arrange(RIGHT, buff=2).next_to(bullet_group[2], DOWN)
            self.play(FadeIn(b), FadeIn(c))
            self.next_slide()
            self.play(FadeOut(b), FadeOut(c))
            self.next_slide()
            self.play(FadeIn(bullet_group[3]))
            self.next_slide()
            self.play(FadeIn(bullet_group[4]))
            self.next_slide()
            
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
        
        def F_IntroToString2():
            path = './h11_2_112823/circle'
            thetas = np.loadtxt(f'{path}/theta.txt')
            ms = np.loadtxt(f'{path}/m.txt')
            fs = np.loadtxt(f'{path}/f.txt')
            ks = np.loadtxt(f'{path}/k.txt')
            div_vols = np.loadtxt(f'{path}/div_vols.txt')
            metrics = 1e5 * np.loadtxt(f'{path}/metrics.txt')
            
            header = Title("String \& Axions in 30 s, Pt 2", color=WHITE)
            self.add(header.to_edge(UP))
            self.wait(1)
            self.next_slide()
            
            header_text = ['Moduli Space', 
                           'Geometry', 
                           'Physics']
            # headlines = Group(*[Text(t) for t in header_text]).arrange(RIGHT, buff=2).next_to(
            #     header, DOWN).scale_to_fit_width(13)
            
            ms_f = [scipy.interpolate.interp1d(thetas, m, bounds_error=False, fill_value=m[-1]) for m in ms.T]
            fs_f = [scipy.interpolate.interp1d(thetas, f, bounds_error=False, fill_value=f[-1]) for f in fs.T]
            ks_f = [scipy.interpolate.interp1d(thetas, k, bounds_error=False, fill_value=k[-1]) for k in ks.T]
            div_vols_f = [scipy.interpolate.interp1d(thetas, d, bounds_error=False, fill_value=d[-1]) for d in div_vols.T]
            metrics_f = [scipy.interpolate.interp1d(thetas, e, bounds_error=False, fill_value=e[-1]) for e in metrics.T]
            
            k_ax = Axes(
                x_range=(-2.5, -1, 0.5), 
                y_range=(3, 5),
                y_length=12,
                axis_config={"include_tip": False, 'include_numbers': True, "font_size": 100})
            plot_ax = Axes(
                x_range=(-25, 15, 10), 
                y_range=(15.4, 16, 0.2),
                y_length=12,
                axis_config={"include_tip": False, 'include_numbers': True, "font_size": 100})
            
            ti = ValueTracker(0)

            elems = [DecimalNumber(0, num_decimal_places=2, include_sign=True, unit=None).scale(0.75)
                     for _ in range(4)]
            for elem, f in zip(elems, metrics_f):
                elem.add_updater(lambda d, f=f: d.set_value(f(ti.get_value())))
            matrix = MobjectMatrix([[elems[0], elems[1]], [elems[2], elems[3]]]).scale(3)
            
            nls = [NumberLine(
                (0, 120, 20), length=8, rotation=90 * DEGREES, include_numbers=True, label_direction=LEFT, font_size=75) 
                   for i in range(len(div_vols.T))]
            nl_group = Group(*nls).arrange(RIGHT, buff=2)
            
            middle = Group(Tex('Kahler metric\n($\\times 10^{5}$)').scale(2.5), 
                           matrix,
                           Tex('Submanifold volumes').scale(2.5), 
                           nl_group).arrange(DOWN, buff=2).scale_to_fit_height(15)
            
            div_vol_dots = [Dot().set_color(RED) for _ in nls]
            for dot, f, nl in zip(div_vol_dots, div_vols_f, nls):
                dot.add_updater(lambda d, f=f, nl=nl: d.move_to(nl.number_to_point(f(ti.get_value()))))
            
            # masterGroup = Group(k_ax, middle, plot_ax).arrange(
                # RIGHT, buff=2).scale_to_fit_width(13).next_to(headlines, DOWN)
                
            header_text_ob = [Text(t).scale(3) for t in header_text]
            master = Group(*header_text_ob, k_ax, middle, plot_ax).arrange_in_grid(
                2, 3, buff=2, col_alignments=['c']*3, row_alignments=['c']*2)
            master.scale_to_fit_width(13).next_to(header, DOWN)
                
            plot_xlabel = plot_ax.get_x_axis_label("\log_{10}(m_a)", edge=DOWN, direction=DOWN)
            plot_ylabel = plot_ax.get_y_axis_label("\log_{10}(f)", edge=UP, direction=UP)
            k_xlabel = k_ax.get_x_axis_label("\\tau_{1}", edge=DOWN, direction=DOWN)
            k_ylabel = k_ax.get_y_axis_label("\\tau_{2}", edge=UP, direction=UP)
            labels = [plot_xlabel, plot_ylabel, k_xlabel, k_ylabel]            
            
            k_dot, k_path = sweepCurveSetup(ti, k_ax, ks_f[0], ks_f[1], color=BLUE)
            mf_dot_1, mf_path_1 = sweepCurveSetup(ti, plot_ax, ms_f[0], fs_f[0], color=BLUE)
            mf_dot_2, mf_path_2 = sweepCurveSetup(ti, plot_ax, ms_f[1], fs_f[1], color=BLUE)
            
            # animate
            self.add(k_ax, k_dot, k_path, k_xlabel, k_ylabel, header_text_ob[0])
            self.wait(1)
            self.next_slide()
            self.add(middle, header_text_ob[1])
            self.wait(1)
            self.next_slide()
            self.add(plot_ax, mf_dot_1, mf_path_1, mf_dot_2, mf_path_2, plot_xlabel, plot_ylabel, header_text_ob[2])
            self.wait(1)
            self.next_slide(loop=True)
            self.add(*div_vol_dots)
            self.play(ti.animate.set_value(2 * np.pi), run_time=10, rate_func=linear)
            self.next_slide()
            # self.wait()
            
            # self.wipe(self.mobjects_without_canvas, [])
            # for obj in div_vol_dots + [k_dot, mf_dot_1, mf_dot_2] + elems:
                # obj.remove()
                
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
        
        def G_KahlerConeAxion():
            self.wait(1)
            KahlerConeMF(
                paths=[f'./h11_3_112823/ray{i+1}' for i in range(3)],
                kahler_vertices=[[0,0], [11,0], [11,11]], 
                stretched_vertices=[[3,2], [11,2], [11,10]], 
                x_range=[-300, 50, 50], 
                y_range=[14.8, 15.6, 0.2], 
                kx_range=[0, 11, 1], 
                ky_range=[0, 11, 1],
                num_axions=3)
            
            self.next_slide()
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
            
        def H_Conclusion():
            header = Title("Conclusions", color=WHITE)
            self.add(header.to_edge(UP))
            self.wait(1)
            self.next_slide()

            bullets = [
                '   - Manim (and its extentions) offer a powerful, accessible way to\n' + 
                '     streamline and animate scientific presentations',
                '   - E.g., can visualize dependence of physical parameters on abstract,\n' +
                '     higher dimensional parameter spaces',
                '   - Certainly, Manim has a learning curve, and programming is more time\n' +
                '     consuming than drag-and-drop...',
                "   - ...but we'll end with a Q: how is our success in striving toward the\n" +
                '     widespread comprehension of our ideas impacted by modality?\n']
            bullet_group = VGroup(
                *[formatText(b, 0.6, WHITE) for b in bullets]).arrange(
                direction=DOWN, aligned_edge=LEFT, buff=0.5).next_to(header, DOWN).shift(DOWN * 0.5)
            
            self.play(FadeIn(bullet_group[0]))
            self.next_slide()
            self.play(FadeIn(bullet_group[1]))
            self.next_slide()
            self.play(FadeIn(bullet_group[2]))
            self.next_slide()
            self.play(FadeIn(bullet_group[3]))
            self.next_slide()
            
            self.wipe(self.mobjects_without_canvas, [])
            self.next_slide()
        
        self.wait_time_between_slides = 0.5
        
        A_Title()
        B_TOC()
        C_ManimIntro()
        D_WhyManim()
        E_IntroToString1()
        F_IntroToString2()
        G_KahlerConeAxion()
        H_Conclusion()
        
        self.play(FadeIn(Text('Thanks!').scale(2)))