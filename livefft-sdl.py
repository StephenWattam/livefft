#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext
import numpy as np

from source import SoundCardDataSource

BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
DELAY_MS = 1

FS = 44000
DATA_SOURCE = SoundCardDataSource(num_chunks=3, sampling_rate=FS, chunk_size=4*1024)
Y_ZOOM = 1000



def render_line(surface, colour, buf, y_pos=None, downsample=5):

    width      = 800
    height     = 600
    y_pos      = y_pos or int(height / 2)
    skip_index = (len(buf)-1) / width
    x_pixels    = range(0, width, downsample)
    indices    = [min(len(buf-1), round(skip_index * i)) for i in x_pixels]
    points     = list(zip(x_pixels, np.take(buf, indices)))

    for pa, pb in zip(points[:-1], points[1:]):
        sdl2.ext.line(surface, WHITE, (pa[0], int(y_pos + Y_ZOOM * pa[1]),
                                       pb[0], int(y_pos + Y_ZOOM * pb[1])))




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
        buf = DATA_SOURCE.get_buffer()

        # Draw
        sdl2.ext.fill(surface, BLACK)
        render_line(surface, WHITE, buf)

    return 0

if __name__ == "__main__":
    sys.exit(run())
