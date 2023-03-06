from scipy.io import wavfile
import argparse
from utils import produce_audio
import numpy as np


def create_parser():
    """
    Create parser to parse input path, output path and ratio for time stretching
    :return: ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog='Phase vocoder',
        description='Use this program for changing audio duration',
        epilog='Write path for input file, path to output file and ratio for time stretching'
    )
    parser.add_argument('input', type=str)
    parser.add_argument('output', type=str)
    parser.add_argument('time_stretch_ratio', type=float)

    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    input_path = namespace.input
    output_path = namespace.output
    time_stretch_ratio = namespace.time_stretch_ratio

    samplerate, data = wavfile.read(input_path)

    window_size = 1024
    hop_size = window_size // 4

    # Optional for working with multichannel audio
    if len(data.shape) == 1:
        result = produce_audio(data, window_size, hop_size, time_stretch_ratio)
    else:
        channels = data.shape[1]
        result = produce_audio(data[:, 0], window_size, hop_size, time_stretch_ratio)
        for ch in range(1, channels):
            result_one = produce_audio(data[:, ch], window_size, hop_size, time_stretch_ratio)
            result = np.c_[result, result_one]

    wavfile.write(output_path, samplerate, result)
