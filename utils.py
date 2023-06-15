import os
import numpy as np


def check_and_create_dir(dirname: str):
    if os.path.exists(dirname):
        return
    os.mkdir(dirname)


def remove_cosmic_ray_1d(spectrum: np.ndarray, width: int, threshold: float):
    spectrum = spectrum.copy()
    intensity = np.diff(spectrum)
    median_int = np.median(intensity)
    mad_int = np.median([np.abs(intensity - median_int)])
    if mad_int == 0:
        mad_int = 1e-4
    modified_scores = 0.6745 * (intensity - median_int) / mad_int
    spikes = abs(modified_scores) > threshold

    for i in np.arange(len(spikes)):
        if spikes[i]:
            w = np.arange(i - width, i + 1 + width)  # スパイク周りの2 m + 1個のデータを取り出す
            w = w[(0 <= w) & (w < (spectrum.shape[0] - 1))]  # 範囲を超えないようトリミング
            w2 = w[spikes[w] == False]  # スパイクでない値を抽出し，
            if len(w2) > 0:
                spectrum[i] = np.mean(spectrum[w2])  # 平均を計算し補完
    return spectrum


def smooth_1d(spectrum, width):
    num_front = width // 2
    num_back = width // 2 + 1 if width % 2 else width // 2
    arr_append_front = np.array([spectrum[:i+1].mean() for i in range(num_front)])
    arr_append_back = np.array([spectrum[::-1][:i+1].mean() for i in range(num_back)])
    spectrum_extended = np.hstack([arr_append_front, spectrum, arr_append_back])
    spectrum_smoothed = np.convolve(spectrum_extended, np.ones(width) / width, mode='same')
    return spectrum_smoothed[num_front:-num_back]


def calc_tick_from_range(xmin, xmax):
    xmin *= 10
    xmax *= 10
    xmin = np.ceil(xmin)
    xmax = np.ceil(xmax)
    ticks = np.arange(xmin, xmax) / 10
    labels = (f'{t:.01f}' for t in ticks)
    return ticks, labels
