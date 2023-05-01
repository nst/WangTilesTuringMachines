import cairo
import math
import colorsys

from wtm_model import WangTM

SP = 8 # tiles legend spacer

def draw_triangle(c, color, translate, rotate):

    c.save()

    c.translate(*translate)
    c.rotate(rotate)

    c.move_to(0,0)
    c.line_to(64,0)
    c.line_to(32,32)
    c.line_to(0,0)
    c.set_source_rgb(*color)
    c.fill_preserve()
    c.set_source_rgb(0,0,0)
    c.stroke()

    c.restore()

def draw_tile(c, t, color_dict):
    
    draw_triangle(c, color_dict[t.n], translate=(0,0), rotate=0)
    c.move_to(30 - 5*len(t.n)/2., 15)
    c.show_text(t.n)
    
    draw_triangle(c, color_dict[t.e], translate=(64,0), rotate=math.pi/2)
    c.move_to(50, 35)
    c.show_text(t.e)

    draw_triangle(c, color_dict[t.s], translate=(64,64), rotate=math.pi)
    c.move_to(30 - 5*len(t.s)/2., 55)
    c.show_text(t.s)

    draw_triangle(c, color_dict[t.w], translate=(0,64), rotate=math.pi/-2)
    c.move_to(5, 35)
    c.show_text(t.w)
    
    c.save()
    c.set_line_width(1)
    c.set_source_rgb(0,0,0)
    c.rectangle(0,0,64,64)
    c.stroke()
    c.restore()

def draw_tileset(c, color_dict, tm):

    if len(tm.tiles_alphabet) == 0:
        tm.build_tiles()
    assert(len(tm.tiles_alphabet) > 0)

    # copy tiles dicts to empty them while drawing
    # this was can make sure to have drawn them all once

    tiles_alphabet = tm.tiles_alphabet.copy()
    tiles_head = tm.tiles_head.copy()
    tiles_action = tm.tiles_action.copy()
    tiles_move = tm.tiles_move.copy()

    c.save()

    c.translate(0,32)

    lines = []
    lines.append("Tileset for machine: " + tm.name)
    lines.append("           Alphabet: " + ','.join(tm.alphabet))
    lines.append("             States: " + ','.join(tm.states))
    lines.append("        Transitions: " + tm.transitions_string)

    for i,s in enumerate(lines):
        c.move_to(64+SP, 16*i)
        c.show_text(s)

    c.translate(0, 90)
    c.move_to(64+SP,-10)

    c.save()
    c.translate(64+SP, 0)
    c.show_text("Alphabet tiles")
    for a in tm.alphabet:
        draw_tile(c, tiles_alphabet.pop(a), color_dict)
        c.translate(64+SP, 0)

    c.translate(0,-10)
    c.move_to(SP, 0)
    c.show_text("Head tiles")
    c.translate(SP,10)

    c.save()
    for a in tm.alphabet:
        draw_tile(c, tiles_head.pop(a), color_dict)
        c.translate(2*(64+SP), 0)
    c.restore()

    c.restore()

    c.translate(0, 64+2*SP)

    c.save()
    c.translate(64+SP,0)
    c.show_text("Action tiles")

    c.move_to(len(tm.tiles_alphabet)*(64+SP)+SP,0)
    c.show_text("Moving tiles")
    c.restore()

    c.translate(0,10)

    c.save()
    for s in tm.states:
        c.save()
        c.move_to(64-16,32)
        c.show_text(s)
        c.translate(64+SP, 0)
        for a in tm.alphabet:
            if s+a in tiles_action:
                draw_tile(c, tiles_action.pop(s+a), color_dict)
            c.translate(64+SP, 0)

        c.translate(SP,0)

        for a in tm.alphabet:
            draw_tile(c, tiles_move.pop((" ", a, s)), color_dict)
            c.translate(64+SP, 0)
            draw_tile(c, tiles_move.pop((s, a, " ")), color_dict)
            c.translate(64+SP, 0)
        c.restore()
        c.translate(0,64+SP)

    c.restore()

    c.restore()

    # make sure that all tiles have been drawn
    
    assert(len(tiles_alphabet) == 0)
    assert(len(tiles_head) == 0)
    assert(len(tiles_action) == 0)
    assert(len(tiles_move) == 0)

def run_and_draw_tiles(c, color_dict, tm, input, head_pos):

    c.save()
    
    for step,left_shifts,tape in tm.run_gen(input, head_pos):

        c.save()

        c.translate(-64*left_shifts,64-SP)

        c.move_to(-32,32)

        c.show_text("%d" % step)

        for t in tape:
            draw_tile(c, t, color_dict)
            c.translate(64,0)
        c.restore()
        
        c.translate(0,64)

    c.restore()

    output = ''.join([t.s for t in tape]).replace(tm.states[-1],"").strip(tm.blank_symbol)

    io_length = max(len(input), len(output))

    c.save()
    c.translate(-64*left_shifts,0)
    c.move_to(0,-32)
    c.show_text("Machine     : " + tm.name)
    c.move_to(0,-16)
    c.show_text("Transitions : " + tm.transitions_string)
    c.move_to(0,0)
    c.show_text("Input:      : " + input.rjust(io_length))
    c.move_to(0,16)
    c.show_text("Output:     : " + output.rjust(io_length))
    c.move_to(0,32)
    c.show_text("      Steps : " + str(step))
    c.restore()

def build_color_dict(tm):

    keys = set()
    keys.update(tm.alphabet)
    keys.update(tm.states)
    keys.update(set([s+a for s in tm.states for a in tm.alphabet]))

    d = {}
    d['#'] = (1,1,1)
    d[' '] = (0.9,0.9,0.9)
    d['0'] = (1,0.5,0.5)
    d['1'] = (0.5,1,0.5)
    d['H'] = (0.7,0.7,0.7)
    d['H1'] = (0,0.6,0)
    d['H0'] = (1,0.3,0)
    d['H#'] = (1,1,0)
    
    N = len(set(keys)-set(d.keys()))
    HSV_tuples = [(x/(N), 0.6, 1.0) for x in range(N)]
    RGB_tuples = [colorsys.hsv_to_rgb(*x) for x in HSV_tuples]
    
    for k in sorted(list(keys)):
        if not k in d:
            d[k] = RGB_tuples.pop()

    return d

def canvas_size(tm, tape, steps, output, draw_tileset, draw_tiling):
    
    tileset_width = 64*2 + len(tm.tiles_alphabet)*(64+SP) + SP + 2*len(tm.tiles_head)*(64+SP)
    tiling_width = (len(tape))*64

    width = 0
    if draw_tileset:
        width += tileset_width
    if draw_tiling:
        width += tiling_width + 2*64
    
    tileset_height = 4*64+(64+SP)*len(tm.states)
    tiling_height = 64*(steps+3)+32
    
    height = 0
    if draw_tileset and draw_tiling:
        height = max(tileset_height, tiling_height)
    elif draw_tileset:
        height = tileset_height
    else:
        height = tiling_height
    
    return (width, height, tileset_width)

def draw_tm(tm: WangTM, input, head_pos=0, tileset=True, tiling=True):

    # first run to get the size
    step, left_shifts, tape, output = tm.run(input, head_pos)

    w,h,tileset_width = canvas_size(tm, tape, step, output, tileset, tiling)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), h)
    c = cairo.Context(surface)

    c.set_antialias(cairo.ANTIALIAS_NONE)

    fo = cairo.FontOptions()
    fo.set_antialias(cairo.ANTIALIAS_NONE)
    c.set_font_options(fo)

    c.select_font_face("Courier New")
    c.set_font_size(14)

    c.set_line_width(1)

    c.set_source_rgb(1,1,1)
    c.paint()

    c.set_source_rgb(0,0,0)

    #

    color_dict = build_color_dict(tm)
    
    if tileset:
        draw_tileset(c, color_dict, tm)
    
    if tileset and tiling:
        c.translate(tileset_width, 0)

    if tiling:
        c.translate(left_shifts*64+64, 64)
        run_and_draw_tiles(c, color_dict, tm, input, head_pos)

    import os
    dir = "tilings"
    if not os.path.exists(dir):
        os.makedirs(dir)
    s = "wtm_" + tm.name.replace(" ", "_").lower() + ".png"
    filename = os.path.sep.join([dir, s])
    surface.write_to_png(filename)

    return filename
