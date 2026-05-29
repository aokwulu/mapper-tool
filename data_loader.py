import os
import pandas as pd
import streamlit as st

FORMALISMS_PATH = "data/formalisms.csv"
PRESETS_PATH = "data/presets.csv"

@st.cache_data # caches for performance
def load_data(path: str) -> pd.DataFrame:
    """loads mappings from csv files
    Args:
        path (str): the path to the csv file

    Returns:
        pd.DataFrame: the loaded mappings as dataframes
    """
    if not os.path.exists(path):
        st.error(f"Could not find {path}. have you run derive_profiles.py?")
        return pd.DataFrame()
        
    with open(path, "r") as f:
        data = pd.read_csv(f, index_col=0)
        if "Archetype_ID" in data.index.name or data.index.name == "Archetype_ID":
            archetype_mapping = {
                0: "Script Kiddie",
                1: "Malicious Insider",
                2: "APT",
                3: "Compromised Credential",
                4: "Anarchist"
            }
            data.index = data.index.map(lambda x: archetype_mapping.get(x, x))
        return data
        
def get_dimensions() -> list[str]:
    """returns the schema dimensions to make sure that it is the same every time
    also checks that they are the same as each other

    Returns:
        list[str]: the dimensions of the schema
    """
    loaded_formalisms = load_data(FORMALISMS_PATH)
    loaded_presets = load_data(PRESETS_PATH)

    if list(loaded_formalisms.columns)[-6:] == list(loaded_presets.columns)[-6:]:
        return list(loaded_formalisms.columns)[-6:]
    else:
        return []
