import numpy as np
from core.data_loader import get_dimensions
import pandas as pd

def find_closest_model(target_profile: pd.Series, formalisms_data: pd.DataFrame) -> tuple:
    """
    calculates Euclidean distance between target profile and every formalism in the dataset
    
    Args:
        target_profile (pd.Series): scores, either from archetype or the sliders
        formalisms_data (pd.DataFrame): all formalisms
        
    Returns:
        tuple: (best_match_name (str), best_match_profile (dict))
    """
    dimensions = get_dimensions()
    target_vector = np.array([target_profile.get(dim, 1) for dim in dimensions])
    best_match_name = None
    best_match_profile = None
    min_distance = float('inf')
    
    formalisms_data = formalisms_data.to_dict(orient='index')  # messy solution fix later
    
    for model_name, model_profile in formalisms_data.items():
        model_vector = np.array([model_profile.get(dim, 1) for dim in dimensions]) # converting to numpy array
        
        # euclidean distance: sqrt(sum((U - F)^2))
        distance = np.linalg.norm(target_vector - model_vector)
        
        if distance < min_distance:# find model with smallest distance
            min_distance = distance
            best_match_name = model_name
            best_match_profile = model_profile
            
    return best_match_name, best_match_profile


def calculate_gaps(target_profile: pd.Series, matched_profile: pd.Series) -> dict:
    """
    calculates gaps between the target profile and the matched model
    
    Args:
        target_profile (pd.Series): scores from either archetype or the sliders
        matched_profile (pd.Series): scores from the recommended formalism
        
    Returns:
        dict: {dimension: difference}
    """
    dimensions = get_dimensions()
    gaps = {}
    
    for dim in dimensions:
        target_score = target_profile.get(dim, 1)
        model_score = matched_profile.get(dim, 1)
        
        d = model_score - target_score
        
        if d < 0:
            gaps[dim] = round(d, 2)

        if d > 0:
            gaps[dim] = round(d, 2)
            
    return gaps


def generate_recommendation_text(matched_model: str, gaps: dict) -> str:
    """
    generates dynamic warning text
    
    Args:
        matched_model (str): recommended formalism
        gaps (dict): differences where the model doesnt exactly fit (the dimension: diff)
        
    Returns:
        str: markdown warning text to be displayed in the UI
    """
    if not gaps:# this literally cannot happen
        return f"**{matched_model}** is an excellent mathematical fit for this adversary profile."
    

    warning_text = f"**{matched_model}** is the closest overall match, but it is not an exact fit for all dimensions:\n\n"
    
    for dim, d in gaps.items():
        if d < 0:
            warning_text += f"*   **{dim}:** Falls short by {abs(d)} points.\n"
        else:
            warning_text += f"*   **{dim}:** Exceeds requirement by {d} points.\n"

    low_gaps = [dim.lower() for dim, d in gaps.items() if d > 0]
    high_gaps = [dim.lower() for dim, d in gaps.items() if d < 0]



    warning_text += f"""\n> **Recommendation:** To ensure accurate resilience scoring, you should run a supplementary simulation focused specifically on validating defenses against 
                    {"low "+" or ".join([", ".join(low_gaps[:-1]),low_gaps[-1]]) if low_gaps else ""}
                    {("and " if low_gaps and high_gaps else "")}
                    {("high "+" or ".join([", ".join(high_gaps[:-1]),high_gaps[-1]]) if high_gaps else "")} 
                    threats.
                    """ # clean enough?
                    
    return warning_text

