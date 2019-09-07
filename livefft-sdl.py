#!/usr/bin/env python

import sys
import sdl2
import sdl2.ext

import numpy as np

from source import SoundCardDataSource, FFTDataSource
from visualisation import FFTVisualisation

FS = 44000
RAW_SOURCE = SoundCardDataSource(num_chunks=4, sampling_rate=FS, chunk_size=2*1024)

FFT_SOURCE = FFTDataSource(RAW_SOURCE)
FFT_RANGE  = (-120, 5)

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("FFT Visualiser", size=(800, 600),
                             flags=sdl2.SDL_WINDOW_RESIZABLE )#| sdl2.SDL_WINDOW_BORDERLESS | sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)

    # Create the visualiser to store state about the app
    surface = window.get_surface()
    visualisation = FFTVisualisation(surface, FFT_SOURCE)

    running = True
    window.show()
    while running:

        events = sdl2.ext.get_events()
        for event in events:

            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    visualisation.set_surface(window.get_surface())

            if event.type == sdl2.SDL_QUIT:
                running = False
                break

            if event.type == sdl2.SDL_KEYDOWN:

                # print(f"KEYDOWN: {dir(event.key.keysym)}")
                if event.key.keysym.scancode == sdl2.SDL_SCANCODE_ESCAPE:
                    running = False
                    break
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_S:
                    visualisation.alter_delay(-1)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_D:
                    visualisation.alter_delay(1)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_C:
                    visualisation.alter_colour_offset(0.005)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_V:
                    visualisation.alter_colour_offset(-0.005)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_Z:
                    visualisation.alter_colour_range(0.05)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_X:
                    visualisation.alter_colour_range(-0.05)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_P:
                    visualisation.toggle_pause()
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_M:
                    visualisation.toggle_party_mode()
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_Q:
                    visualisation.alter_fft_range(0.05)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_W:
                    visualisation.alter_fft_range(-0.05)
                elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_L:
                    visualisation.toggle_clock()
            # elif event.type == sdl2.SDL_KEYUP:
            #     print(f"KEYUP: {event}")

        visualisation.update()
        window.refresh()
        visualisation.delay()

    return 0

if __name__ == "__main__":
    sys.exit(run())
