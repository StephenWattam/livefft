#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext

from source import SoundCardDataSource

BLACK = sdl2.ext.Color(0, 0, 0)
DELAY_MS = 10

FS = 44000
DATA_SOURCE = SoundCardDataSource(num_chunks=3, sampling_rate=FS, chunk_size=4*1024)

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
        print(f"-> {buf}")

        # Draw
        sdl2.ext.fill(window.get_surface(), BLACK)

    return 0

if __name__ == "__main__":
    sys.exit(run())
