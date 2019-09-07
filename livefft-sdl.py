#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext
import colorsys

import numpy as np

from source import SoundCardDataSource, FFTDataSource

BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
DELAY_MS = 10

FS = 44000
RAW_SOURCE = SoundCardDataSource(num_chunks=3, sampling_rate=FS, chunk_size=4*1024)

FFT_SOURCE = FFTDataSource(RAW_SOURCE)
FFT_RANGE  = (-120, 5)

def render_line(surface, colour, buf, y_range=None, y_pos=None, downsample=5, y_zoom=1):

    width      = surface.w
    height     = surface.h
    y_pos      = y_pos or int(height / 2)
    points = downsample_to_fixed_length(buf, (0, width), downsample, y_range=y_range)

    for pa, pb in zip(points[:-1], points[1:]):
        sdl2.ext.line(surface, WHITE, (pa[0], int(y_pos + y_zoom * pa[1]),
                                       pb[0], int(y_pos + y_zoom * pb[1])))


    # print(f"-> {len(buf)}")
    # import code; code.interact(local=locals())


def colour_simple(x):
    """Return an SDL-compatible raw pixel value given a value from 0-1"""


    r, g, b = colorsys.hsv_to_rgb(0.2 + x*0.5, x, x)

    r *= 255
    g *= 255
    b *= 255

    return (int(g) << 8) + (int(b) << 16) + int(r)



def render_colour_line(surface, colour_func, y_range, buf, y_pos, downsample=1):

    # FIXME!  DEBUG!
    # buf = np.linspace(y_range[0], y_range[1], 10000)


    points = downsample_to_fixed_length(buf, (0, surface.w), downsample, y_range=y_range)
    pixels = sdl2.ext.pixels2d(surface)
    # import code; code.interact(local=locals())

    pixels[10][10] = 1000000

    for p in points:
        pixels[p[0]][y_pos] = colour_func(p[1])



def downsample_to_fixed_length(buf, x_range, resolution=1, y_range=None):
    """Takes a buffer of length n and rescales it to length x,
    returning a list of (x, y) values where y is taken from the buffer
    and x represents a point in the range given"""

    skip_index = (len(buf)-1) / x_range[1] - x_range[0]
    x_samples  = range(x_range[0], x_range[1], resolution)
    indices    = [min(len(buf-1), round(skip_index * (i - x_range[0]))) for i in x_samples]
    y_values   = np.take(buf, indices)

    # Normalise if a range is given
    if y_range is not None:
        y_values   = np.clip(y_values, y_range[0], y_range[1])
        y_values   -= y_range[0]
        y_values   *= 1.0/(y_range[1] - y_range[0])

    return list(zip(x_samples, y_values))



def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("FFT Visualiser", size=(800, 600))

    surface = window.get_surface()

    running = True
    window.show()
    fft_y_pos = 599
    while running:

        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:

                print(f"KEYDOWN: {event.key.keysym}")
            elif event.type == sdl2.SDL_KEYUP:
                print(f"KEYUP: {event}")

        window.refresh()

        # Delay and update
        sdl2.SDL_Delay(DELAY_MS)
        raw_buf = RAW_SOURCE.get_buffer()
        fft_buf = FFT_SOURCE.get_buffer()

        # Draw
        # sdl2.ext.fill(surface, BLACK)
        # render_line(surface, WHITE, raw_buf, y_zoom=10)
        render_line(surface, WHITE, fft_buf, y_range=FFT_RANGE, y_zoom=-100)
        render_colour_line(surface, colour_simple, FFT_RANGE, fft_buf, fft_y_pos)

        fft_y_pos -= 1
        if fft_y_pos < 0:
            fft_y_pos = 599

    return 0

if __name__ == "__main__":
    sys.exit(run())
