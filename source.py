import threading
import numpy as np
from datetime import datetime, timedelta
import time
import pyaudio




class DataSource():

    def get_buffer():
        return []



class SoundCardDataSource(DataSource):

    def __init__(self, num_chunks, channels=1, sampling_rate=44100,
                 chunk_size=1024):
        self.fs = sampling_rate
        self.channels = int(channels)
        self.chunk_size = int(chunk_size)
        self.num_chunks = int(num_chunks)

        # Check format is supported
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        dev = self.pyaudio.get_default_input_device_info()
        if not self.pyaudio.is_format_supported(
                rate=sampling_rate,
                input_device=dev['index'],
                input_channels=channels,
                input_format=pyaudio.paInt16):
            raise RuntimeError("Unsupported audio format or rate")

        # Allocate buffers
        self._allocate_buffer()

        # Callback function is called with new audio data
        def callback(in_data, frame_count, time_info, status):
            samples = SoundCardDataSource.data_to_array(in_data, self.channels)
            self._write_chunk(samples)
            return (None, pyaudio.paContinue)

        # Start the stream
        self.stream = self.pyaudio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            frames_per_buffer=self.chunk_size,
            rate=self.fs,
            stream_callback=callback,
            input=True
        )

    def __del__(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pyaudio.terminate()

    def _write_chunk(self, samples):
        self.buffer[self.next_chunk, :, :] = samples
        self.next_chunk = (self.next_chunk + 1) % self.buffer.shape[0]

    def _allocate_buffer(self):
        self.buffer = np.zeros((self._num_chunks,
                                self.chunk_size,
                                self.channels))
        self.next_chunk = 0

    @property
    def num_chunks(self):
        return self._num_chunks

    @num_chunks.setter
    def num_chunks(self, num_chunks):
        n = max(1, int(num_chunks))
        if n * self.chunk_size > 2**16:
            n = 2**16 // self.chunk_size
        self._num_chunks = n
        self._allocate_buffer()

    def get_buffer(self):
        """Return all chunks joined together"""
        a = self.buffer[:self.next_chunk]
        b = self.buffer[self.next_chunk:]
        return np.concatenate((b, a), axis=0) \
                 .reshape((self.buffer.shape[0] * self.buffer.shape[1],
                           self.buffer.shape[2]))

    @property
    def timeValues(self):
        N = self.buffer.shape[0] * self.buffer.shape[1]
        return np.linspace(0, N/self.fs, N)

    @staticmethod
    def data_to_array(data, channels):
        return (np.frombuffer(data, dtype=np.int16)
                .reshape((-1, channels))
                .astype(float) / 2**15)





class FFTDataSource(threading.Thread):

    def __init__(self, source):
        super().__init__()
        self._source = source

    def run(self):
        print("Thread running")


    # Based on function from numpy 1.8
    @staticmethod
    def rfftfreq(n, d=1.0):
        """
        Return the Discrete Fourier Transform sample frequencies
        (for usage with rfft, irfft).

        The returned float array `f` contains the frequency bin centers in cycles
        per unit of the sample spacing (with zero at the start). For instance, if
        the sample spacing is in seconds, then the frequency unit is cycles/second.

        Given a window length `n` and a sample spacing `d`::

        f = [0, 1, ..., n/2-1, n/2] / (d*n) if n is even
        f = [0, 1, ..., (n-1)/2-1, (n-1)/2] / (d*n) if n is odd

        Unlike `fftfreq` (but like `scipy.fftpack.rfftfreq`)
        the Nyquist frequency component is considered to be positive.

        Parameters
        ----------
        n : int
        Window length.
        d : scalar, optional
        Sample spacing (inverse of the sampling rate). Defaults to 1.

        Returns
        -------
        f : ndarray
        Array of length ``n//2 + 1`` containing the sample frequencies.
        """
        if not isinstance(n, int):
            raise ValueError("n should be an integer")
        val = 1.0/(n*d)
        N = n//2 + 1
        results = np.arange(0, N, dtype=int)
        return results * val

    @staticmethod
    def fft_slices(x):
        Nslices, Npts = x.shape
        window = np.hanning(Npts)

        # Calculate FFT
        fx = np.fft.rfft(window[np.newaxis, :] * x, axis=1)

        # Convert to normalised PSD
        Pxx = abs(fx)**2 / (np.abs(window)**2).sum()

        # Scale for one-sided (excluding DC and Nyquist frequencies)
        Pxx[:, 1:-1] *= 2

        # And scale by frequency to get a result in (dB/Hz)
        # Pxx /= Fs
        return Pxx ** 0.5

    @staticmethod
    def find_peaks(Pxx):
        # filter parameters
        b, a = [0.01], [1, -0.99]
        Pxx_smooth = filtfilt(b, a, abs(Pxx))
        peakedness = abs(Pxx) / Pxx_smooth

        # find peaky regions which are separated by more than 10 samples
        peaky_regions = nonzero(peakedness > 1)[0]
        edge_indices = nonzero(diff(peaky_regions) > 10)[0]  # RH edges of peaks
        edges = [0] + [(peaky_regions[i] + 5) for i in edge_indices]
        if len(edges) < 2:
            edges += [len(Pxx) - 1]

        peaks = []
        for i in range(len(edges) - 1):
            j, k = edges[i], edges[i+1]
            peaks.append(j + np.argmax(peakedness[j:k]))
        return peaks




