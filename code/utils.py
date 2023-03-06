from scipy import signal
import numpy as np


def create_frames(x: np.ndarray, hop: int, window_size: int) -> (np.ndarray, int):
    """
    Splits a vector in overlapping frames and stores these frames into a matrix.
    :param x: data vector.
    :param hop: number of samples between adjacent windows.
    :param window_size: size of each window.
    :return: tuple of resulting matrix made of all the frames and number of frames in the matrix.
    """
    number_slices = int(np.floor((len(x) - window_size) / hop))
    x = x[:number_slices * hop + window_size]
    vector_frames = np.zeros((int(np.floor(len(x) / hop)), window_size))

    for i in range(number_slices):
        index_time_start = i * hop
        index_time_end = i * hop + window_size - 1

        vector_frames[i, :] = x[index_time_start: index_time_end + 1]

    return vector_frames, number_slices


def fusion_matrix(frames_matrix: np.ndarray, hop: int) -> np.ndarray:
    """
    Overlap adds the frames from the input matrix.
    :param frames_matrix: matrix made of all the frames.
    :param hop: number of samples between adjacent windows.
    :return: resulting vector from overlap add.
    """
    shape_matrix = frames_matrix.shape
    number_frames = shape_matrix[0]
    size_frames = shape_matrix[1]

    vector_time = np.zeros(number_frames * hop - hop + size_frames)

    time_index = 0
    for i in range(number_frames):
        vector_time[time_index: time_index + size_frames] += np.conj(frames_matrix[i, :].T)

        time_index += hop

    return vector_time


def produce_audio(data: np.ndarray, window_size: int, hop_size: int, alpha: float) -> np.ndarray:
    """
    Time-stretch the input signal.
    :param data: vector to be processed.
    :param window_size: size of the window.
    :param hop_size: size of the hop.
    :param alpha: ratio for time stretching.
    :return: result vector.
    """
    # Parameters
    hop = hop_size
    hop_out = round(alpha * hop)
    wn = signal.hann(window_size * 2 + 1)
    wn = wn[1::2]

    # Source data
    x = data
    x = np.concatenate((np.zeros(hop * 3), x))

    # Initialization
    y, number_frames_input = create_frames(x, hop, window_size)
    number_frames_output = number_frames_input
    outputy = np.zeros((number_frames_output, window_size))
    phase_cumulative = 0
    previous_phase = 0

    for i in range(number_frames_input):
        # Analysis
        current_frame = y[i, :]
        current_frame_windowed = current_frame * np.conj(wn.T) / np.sqrt((window_size / hop) / 2)
        current_frame_windowed_fft = np.fft.fft(current_frame_windowed)
        mag_frame = np.abs(current_frame_windowed_fft)
        phase_frame = np.angle(current_frame_windowed_fft)

        # Processing
        delta_phi = phase_frame - previous_phase
        previous_phase = phase_frame
        delta_phi_prime = delta_phi - hop * 2 * np.pi * np.array(range(window_size)) / window_size
        delta_phi_prime_mod = np.mod(delta_phi_prime + np.pi, 2 * np.pi) - np.pi
        true_freq = 2 * np.pi * np.array(range(window_size)) / window_size + delta_phi_prime_mod / hop
        phase_cumulative += hop_out * true_freq

        # Synthesis
        output_mag = mag_frame
        output_frame = np.real(np.fft.ifft(output_mag * np.exp(1j * phase_cumulative)))
        outputy[i, :] = output_frame * np.conj(wn.T) / np.sqrt((window_size / hop_out) / 2)

    output_time_stretched = fusion_matrix(outputy, hop_out)

    return output_time_stretched
