#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext
import numpy as np

from source import SoundCardDataSource, FFTDataSource

BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
DELAY_MS = 1

FS = 44000
RAW_SOURCE = SoundCardDataSource(num_chunks=3, sampling_rate=FS, chunk_size=4*1024)

FFT_SOURCE = FFTDataSource(RAW_SOURCE)
FFT_RANGE  = (-120, 5)

def render_line(surface, colour, buf, y_pos=None, downsample=5, y_zoom=1):

    width      = surface.w
    height     = surface.h
    y_pos      = y_pos or int(height / 2)
    points = downsample_to_fixed_length(buf, (0, width), downsample, limit=(-100, 100))

    for pa, pb in zip(points[:-1], points[1:]):
        sdl2.ext.line(surface, WHITE, (pa[0], int(y_pos + y_zoom * pa[1]),
                                       pb[0], int(y_pos + y_zoom * pb[1])))


    # print(f"-> {len(buf)}")
    # import code; code.interact(local=locals())

def downsample_to_fixed_length(buf, rnge, resolution=1, limit=(float("-inf"), float("inf"))):
    """Takes a buffer of length n and rescales it to length x,
    returning a list of (x, y) values where y is taken from the buffer
    and x represents a point in the range given"""

    skip_index = (len(buf)-1) / rnge[1] - rnge[0]
    x_samples  = range(rnge[0], rnge[1], resolution)
    indices    = [min(len(buf-1), round(skip_index * (i - rnge[0]))) for i in x_samples]
    points     = list(zip(x_samples, np.clip(np.take(buf, indices), limit[0], limit[1]) ))

    return points





def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("FFT Visualiser", size=(800, 600))

    surface = window.get_surface()

    running = True
    window.show()
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
        sdl2.ext.fill(surface, BLACK)
        # render_line(surface, WHITE, raw_buf, y_zoom=10)
        render_line(surface, WHITE, fft_buf, y_zoom=-1, downsample=5)

    return 0

if __name__ == "__main__":
    sys.exit(run())
