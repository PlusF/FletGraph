import pandas as pd
from dataloader import DataLoader
from constants import ENVIRONMENT, CONDITION


def get_df():
    directory = r'C:\Users\rkane\Documents\data_Rayleigh'
    # env:   0: Air,                   1: Vacuum,               2: Water
    # cond:  0: before water exposure, 1: after water exposure, 2: in water, 3: after baking
    data = {
        r'\230524\sif\1_560_air_1684930195.4375477_1684998589.5986567.asc': {
            'env': 0,
            'ND': 10,
            'cond': 0,
        },  # Air, 32%, before water exposure
        r'\230524\sif\1_560_3.56Pa_1684930195.471517_1684931291.0099418.asc': {
            'env': 1,
            'ND': 10,
            'cond': 0,
        },  # Vacuum, 10%, before water exposure
        r'\230524\sif\1_560_4.26Pa_1684930195.418307_1684931314.1334267.asc': {
            'env': 1,
            'ND': 32,
            'cond': 0,
        },  # Vacuum, 32%, before water exposure
        r'\230524\sif\1_560_3.50Pa_1684930195.4549568_1684931449.0301821.asc': {
            'env': 1,
            'ND': 50,
            'cond': 0,
        },  # Vacuum, 50%, before water exposure
        # TODO: 50times_1 & 2が何のデータか確認
        r'\230525\air5_1685002470.2369397_1685002634.9141688.asc': {
            'env': 0,
            'ND': 5,
            'cond': 1,
        },  # Air, 5%, after water exposure
        r'\230525\air10_1685002470.2550666_1685002671.514385.asc': {
            'env': 0,
            'ND': 10,
            'cond': 1,
        },  # Air, 10%, after water exposure
        r'\230525\air32_1685002470.2740061_1685002698.4063935.asc': {
            'env': 0,
            'ND': 32,
            'cond': 1,
        },  # Air, 32%, after water exposure
        r'\230525\air50_1685002470.2944698_1685002913.0545907.asc': {
            'env': 0,
            'ND': 50,
            'cond': 1,
        },  # Air, 50%, after water exposure
        # TODO: laser_checkの条件確認 ND10%?
        r'\230529\2\CNT560_air10%_1685353907.8937964.asc': {
            'env': 0,
            'ND': 10,
            'cond': 1,
        },  # Air, 10%, after water exposure
        r'\230529\2\CNT560_air32%_1685353907.9170496.asc': {
            'env': 0,
            'ND': 32,
            'cond': 1,
        },  # Air, 32%, after water exposure
        r'\230529\2\CNT560_air50%_1685353907.9409862.asc': {
            'env': 0,
            'ND': 50,
            'cond': 1,
        },  # Air, 50%, after water exposure
        r'\230529\2\CNT560_air50%_30sec_1685353907.9968395.asc': {
            'env': 0,
            'ND': 50,
            'cond': 1,
        },  # Air, 50%, after water exposure
        r'\230529\2\CNT560_air50%_3sec_1685353907.9689114.asc': {
            'env': 0,
            'ND': 50,
            'cond': 1,
        },  # Air, 50%, after water exposure
        r'\230529\2\CNT560_vacuum_1685353908.0207818.asc': {
            'env': 1,
            'ND': 10,
            'cond': 1,
        },  # Vacuum, 10%, after water exposure
        r'\230529\2\CNT560_vacuum2_1685353908.0467026.asc': {
            'env': 1,
            'ND': 10,
            'cond': 1,
        },  # Vacuum, 10%, after water exposure
        r'\230529\2\CNT560_water_1685353907.871831.asc': {
            'env': 2,
            'ND': 10,
            'cond': 2,
        },  # Water, 10%, during water exposure
        r'\230601\5_Vacuum1%_narrower_aligned_1685603296.2044065.asc': {
            'env': 1,
            'ND': 1,
            'cond': 3,
        },  # Vacuum, 1%, after baking
        r'\230601\5_Vacuum5%_narrower_aligned_1685603296.2225509.asc': {
            'env': 1,
            'ND': 5,
            'cond': 3,
        },  # Vacuum, 5%, after baking
        r'\230601\5_Vacuum25%_narrower_aligned_1685603296.3104334.asc': {
            'env': 1,
            'ND': 25,
            'cond': 3,
        },  # Vacuum, 25%, after baking
        r'\230601\5_Vacuum32%_narrower_aligned_2_1685603296.3371189.asc': {
            'env': 1,
            'ND': 32,
            'cond': 3,
        },  # Vacuum, 32%, after baking
        r'\230601\5_Vacuum50%_narrower_aligned_2_1685603296.3773515.asc': {
            'env': 1,
            'ND': 50,
            'cond': 3,
        },  # Vacuum, 50%, after baking
        r'\230601\5_Vacuum50%_narrower_aligned_3_1685603296.4038866.asc': {
            'env': 1,
            'ND': 50,
            'cond': 3,
        },  # Vacuum, 50%, after baking
        r'\230601\6_Air32%_2_1685603296.4551036.asc': {
            'env': 0,
            'ND': 32,
            'cond': 3,
        },  # Air, 32%, after baking
        r'\230601\6_Air50%_2_1685603296.480021.asc': {
            'env': 0,
            'ND': 50,
            'cond': 3,
        },  # Air, 50%, after baking
    }
    data_fullpath = {}
    for key, value in data.items():
        data_fullpath[directory + key] = value

    dl = DataLoader()
    dl.load_files(data_fullpath.keys())

    data_all = {}
    for filename in data_fullpath.keys():
        data_all[filename] = {
            'environment': ENVIRONMENT[data_fullpath[filename]['env']],
            'ND filter': data_fullpath[filename]['ND'],
            'condition': CONDITION[data_fullpath[filename]['cond']],
            'xdata': dl.spec_dict[filename].xdata,
            'ydata': dl.spec_dict[filename].ydata,
        }

    df = pd.DataFrame(data=data_all).T
    df = df.reset_index(names='filename')
    df = df.reindex(columns=['environment', 'ND filter', 'condition', 'filename', 'xdata', 'ydata'])

    return df