import marimo

__generated_with = "0.20.2"
app = marimo.App(sql_output="polars")

with app.setup:
    from manim import (
        Dot,
        Circle,
        Square,
        VGroup,
        Text,
        MathTex,
        Axes,
        FadeIn,
        FadeOut,
        Create,
        Write,
        Transform,
        ReplacementTransform,
        MoveToTarget,
        AnimationGroup,
        Succession,
        Arrow,
        GrowArrow,
        LaggedStart,
        SurroundingRectangle,
        BLUE,
        RED,
        GREEN,
        WHITE,
        YELLOW,
        GRAY,
        BLACK,
        ORIGIN,
        UP,
        DOWN,
        LEFT,
        RIGHT,
        linear,
        smooth,
        config,
    )
    from manim_slides import Slide
    import numpy as np


@app.cell
def _():
    import marimo as mo
    from pathlib import Path

    return Path, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # MapReduce in Python
    A visual guide to understanding the MapReduce paradigm.
    """)
    return


@app.cell
def _(SHIFT):
    class MapReducePresentation(Slide):
        def construct(self):
            self.camera.background_color = BLACK

            # ── Colours for each stage ───────────────────────────────
            INPUT_COLOR   = WHITE
            MAP_COLOR     = BLUE
            SHUFFLE_COLOR = YELLOW
            REDUCE_COLOR  = RED
            ARROW_COLOR   = GRAY

            # Horizontal positions for each stage column
            INPUT_X   = -5
            MAP_X_VAL =  1.5
            STAGE_STEP = 3.0   # distance between stage columns

            # ── Title Slide ──────────────────────────────────────────
            title    = Text("MapReduce in Python", font_size=56, color=BLUE)
            subtitle = Text("A Visual Guide",      font_size=36, color=WHITE)
            title_group = VGroup(title, subtitle).arrange(DOWN)
            self.play(FadeIn(title_group))
            self.next_slide()
            self.play(FadeOut(title_group))

            # ── SLIDE 2 : Input Data ─────────────────────────────────
            slide_title = Text("Step 1 — Input Data", font_size=30, color=YELLOW).to_edge(UP)
            self.play(FadeIn(slide_title))

            f1_text = Text('File 1: "Tyler the Creator"', font_size=24, color=WHITE)
            f2_text = Text('File 2: "Tyler is the best"',  font_size=24, color=WHITE)

            f1_box = SurroundingRectangle(f1_text, color=INPUT_COLOR, buff=0.25)
            f2_box = SurroundingRectangle(f2_text, color=INPUT_COLOR, buff=0.25)

            f1_group = VGroup(f1_text, f1_box)
            f2_group = VGroup(f2_text, f2_box)

            input_group = VGroup(f1_group, f2_group).arrange(DOWN, buff=0.8)
            input_group.move_to([INPUT_X, 0, 0])  # place at far left from the start

            self.play(FadeIn(input_group))
            self.next_slide()

            # ── SLIDE 3 : Map Phase ───────────────────────────────────
            new_slide_title = Text("Step 2 — Map Phase", font_size=30, color=YELLOW).to_edge(UP)
            self.play(ReplacementTransform(slide_title, new_slide_title))
            slide_title = new_slide_title

            # All 7 emitted key-value pairs (both files combined in one MAP box)
            map_kvs = VGroup(
                Text("('Tyler',   1)", font_size=18, color=WHITE),
                Text("('the',     1)", font_size=18, color=WHITE),
                Text("('Creator', 1)", font_size=18, color=WHITE),
                Text("('Tyler',   1)", font_size=18, color=WHITE),
                Text("('is',      1)", font_size=18, color=WHITE),
                Text("('the',     1)", font_size=18, color=WHITE),
                Text("('best',    1)", font_size=18, color=WHITE),
            ).arrange(DOWN, buff=0.18)

            map_kvs.move_to([0, -0.1, 0])
            map_rect  = SurroundingRectangle(map_kvs, color=MAP_COLOR, buff=0.28)
            map_label = Text("MAP", font_size=22, color=MAP_COLOR).next_to(map_rect, UP, buff=0.08)
            map_stage = VGroup(map_kvs, map_rect, map_label)

            # Input is already at INPUT_X — no slide needed, just draw arrows and reveal MAP
            arr_in1 = Arrow(
                f1_group.get_right(), map_rect.get_left() + UP * 0.65,
                buff=0.1, stroke_width=2.5, max_tip_length_to_length_ratio=0.08, color=WHITE,
            )
            arr_in2 = Arrow(
                f2_group.get_right(), map_rect.get_left() + DOWN * 0.65,
                buff=0.1, stroke_width=2.5, max_tip_length_to_length_ratio=0.08, color=WHITE,
            )

            self.play(GrowArrow(arr_in1), GrowArrow(arr_in2))
            self.play(Create(map_rect), FadeIn(map_label), FadeIn(map_kvs))

            self.next_slide()

            # ── SLIDE 4 : Shuffle & Sort ─────────────────────────────
            new_slide_title = Text("Step 3 — Shuffle & Sort", font_size=30, color=YELLOW).to_edge(UP)
            self.play(ReplacementTransform(slide_title, new_slide_title))
            slide_title = new_slide_title

            # SHUFFLE_X stays fixed at MAP_X_VAL (map will slide left to make room)
            SHUFFLE_X = MAP_X_VAL
            shuffle_kvs = VGroup(
                Text("'Tyler'   : [1, 1]", font_size=18, color=WHITE),
                Text("'the'     : [1, 1]", font_size=18, color=WHITE),
                Text("'Creator' : [1]",    font_size=18, color=WHITE),
                Text("'is'      : [1]",    font_size=18, color=WHITE),
                Text("'best'    : [1]",    font_size=18, color=WHITE),
            ).arrange(DOWN, buff=0.25)
            shuffle_kvs.move_to([SHUFFLE_X, -0.1, 0])
            shuffle_rect  = SurroundingRectangle(shuffle_kvs, color=SHUFFLE_COLOR, buff=0.28)
            shuffle_label = Text("SHUFFLE & SORT", font_size=18, color=SHUFFLE_COLOR).next_to(shuffle_rect, UP, buff=0.08)
            shuffle_stage = VGroup(shuffle_kvs, shuffle_rect, shuffle_label)

            # Fade out the input boxes & file arrows; slide map_stage left to make room
            self.play(
                FadeOut(input_group),
                FadeOut(arr_in1),
                FadeOut(arr_in2),
                map_stage.animate.shift(LEFT * STAGE_STEP),
            )

            # Reveal the shuffle stage
            self.play(Create(shuffle_rect), FadeIn(shuffle_label), FadeIn(shuffle_kvs))

            # Arrows: each of the 7 map KVs points to its grouped shuffle slot
            # map indices  →  shuffle indices
            map_to_shuffle = [(0, 0), (1, 1), (2, 2), (3, 0), (4, 3), (5, 1), (6, 4)]
            ms_arrows = VGroup(*[
                Arrow(
                    map_kvs[mi].get_right(), shuffle_kvs[si].get_left(),
                    buff=0.05, stroke_width=1.0, max_tip_length_to_length_ratio=0.05, color=ARROW_COLOR,
                )
                for mi, si in map_to_shuffle
            ])
            self.play(LaggedStart(*[GrowArrow(a) for a in ms_arrows], lag_ratio=0.07))

            current_group2 = VGroup(map_stage, ms_arrows, shuffle_stage)
            self.next_slide()

            # ── SLIDE 5 : Reduce Phase ────────────────────────────────
            new_slide_title = Text("Step 4 — Reduce Phase", font_size=30, color=YELLOW).to_edge(UP)
            self.play(ReplacementTransform(slide_title, new_slide_title))
            slide_title = new_slide_title

            REDUCE_X = SHUFFLE_X + STAGE_STEP
            reduce_kvs = VGroup(
                Text("('Tyler',   2)", font_size=18, color=GREEN),
                Text("('the',     2)", font_size=18, color=GREEN),
                Text("('Creator', 1)", font_size=18, color=GREEN),
                Text("('is',      1)", font_size=18, color=GREEN),
                Text("('best',    1)", font_size=18, color=GREEN),
            ).arrange(DOWN, buff=0.25)
            reduce_kvs.move_to([REDUCE_X, -0.1, 0])
            reduce_rect  = SurroundingRectangle(reduce_kvs, color=REDUCE_COLOR, buff=0.28)
            reduce_label = Text("REDUCE", font_size=20, color=REDUCE_COLOR).next_to(reduce_rect, UP, buff=0.08)
            reduce_stage = VGroup(reduce_kvs, reduce_rect, reduce_label)

            # Slide everything left so shuffle ends up centred; reduce slides in from the right
            self.play(current_group2.animate.shift(LEFT * SHIFT))

            self.play(Create(reduce_rect), FadeIn(reduce_label), FadeIn(reduce_kvs))

            # Arrows: each shuffle slot → its reduce output (1-to-1)
            sr_arrows = VGroup(*[
                Arrow(
                    shuffle_kvs[i].get_right(), reduce_kvs[i].get_left(),
                    buff=0.05, stroke_width=1.0, max_tip_length_to_length_ratio=0.05, color=ARROW_COLOR,
                )
                for i in range(5)
            ])
            self.play(LaggedStart(*[GrowArrow(a) for a in sr_arrows], lag_ratio=0.1))

            self.next_slide()

    return (MapReducePresentation,)


@app.cell
def _(MapReducePresentation):
    from moterm import Kmd

    MapReducePresentation

    out1 = Kmd("manim-slides render map_reduce_slides.py MapReducePresentation")
    out1
    return Kmd, out1


@app.cell
def _(Kmd, out1):
    out1 

    out2 = Kmd("manim-slides convert MapReducePresentation -c controls=true map_reduce_presentation.html --one-file")
    out2
    return (out2,)


@app.cell
def _(Path, mo, out2):
    out2

    mo.iframe(Path("map_reduce_presentation.html").read_text())
    return


@app.cell(hide_code=True)
def _():
    return


if __name__ == "__main__":
    app.run()
