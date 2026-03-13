import pandas as pd
import numpy as np
import pytest

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.app import create_sex_completion_rate_df

@pytest.fixture
def sample_input_df():
    df = pd.DataFrame({
        "Completion_Rate_Primary_Male": [.5, .5, .3, .7, .6, .9, .9, .7, .6, .4],
        "Completion_Rate_Primary_Female": [.5, .5, .4, .6, .9, .8, .9, .6, .7, .5],
        "Completion_Rate_Lower_Secondary_Male": [.5, .4, .3, .6, .4, .7, .9, .6, .6, .2],
        "Completion_Rate_Lower_Secondary_Female": [.5, .5, .2, .5, .6, .7, .8, .6, .7, .3],
        "Completion_Rate_Upper_Secondary_Male": [.5, .4, .2, .6, .3, .7, .8, .5, .3, .2],
        "Completion_Rate_Upper_Secondary_Female": [.3, .5, .2, .4, .5, .5, .8, .4, .3, .2],
        "Region": ["R1", "R1", "R1", "R1", "R1", "R2", "R2", "R2", "R2", "R2",],
        "iso3": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
        "some_other_column": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    })
    return df

@pytest.fixture
def sample_output_df():
    df = pd.DataFrame({
        'Sex': {
            0: 'Female',
            1: 'Female',
            2: 'Female',
            3: 'Male',
            4: 'Male',
            5: 'Male'
            },
        'Education_Level': {
            0: 'Lower Secondary',
            1: 'Primary',
            2: 'Upper Secondary',
            3: 'Lower Secondary',
            4: 'Primary',
            5: 'Upper Secondary'
            },
        'Completion_Rate': {
            0: 0.5399999999999999,
            1: 0.64,
            2: 0.41000000000000003,
            3: 0.52,
            4: 0.61,
            5: 0.45
            }
        })
    return df

def test_correct_output(sample_input_df, sample_output_df):
    """Test that the function is giving the correct output"""
    df_test = create_sex_completion_rate_df(sample_input_df).select_dtypes(include='number')
    df_val = sample_output_df.select_dtypes(include='number')  # type: ignore

    assert np.isclose(df_test, df_val).all(), "create_sex_completion_rate_df() is giving incorrect output."