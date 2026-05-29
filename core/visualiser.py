import plotly.graph_objects as go
from core.data_loader import get_dimensions

def _prepare_radar_data(scores: dict) -> tuple:
    """helper function to get it into radar chart format
    only called here, probably doesnt need to be public

    Args:
        scores (dict): dictionary of dimension names and scores

    Returns:
        tuple: (values (list), dimensions (list))
    """
    
    dimensions = get_dimensions()

    values = [scores.get(dim, 1) for dim in dimensions]
    values.append(values[0])
    dimensions_loop = dimensions + [dimensions[0]]
    
    return values, dimensions_loop

def create_single_radar(model_name: str, scores: dict) -> go.Figure:
    """
    creates plotly radar chart
    felt it was nicer than the line graph
    
    Args:
        model_name (str): formalism name
        scores (dict): associated scores
        
    Returns:
        go.Figure: radar chart graph object
    """

    values, categories = _prepare_radar_data(scores)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=model_name,
        line=dict(color='#1f77b4', width=2),
        fillcolor='rgba(31, 119, 180, 0.4)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5], # Locked to 0-5 to ensure visual consistency
                tickmode='linear',
                tick0=1,
                dtick=1
            )
        ),
        showlegend=True,
        title=dict(text=f"Adversary Profile: {model_name}", x=0.5)
    )

    return fig

def create_comparison_radar(target_name: str, target_scores: dict, matched_name: str, matched_scores: dict) -> go.Figure:
    """ generates a dual radar chart to highlight the gaps when a user queries an adversary
    
    Args:
        target_name (str): name of requested profile or custom
        target_scores (dict): scores of either the requested profile or custom
        matched_name (str): recommended formalism name
        matched_scores (dict): associated scores of recommended formalism
        
    Returns:
        go.Figure: radar chart graph object
    """
    target_values, categories = _prepare_radar_data(target_scores)
    matched_values, _ = _prepare_radar_data(matched_scores)

    fig = go.Figure()

    # user requested profile -------------------------------
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=categories,
        fill='toself',
        name=f"Requested: {target_name}",
        line=dict(color='#ff7f0e', width=2, dash='dot'),
        fillcolor='rgba(255, 127, 14, 0.2)'
    ))

    # recommended profile ------------------------------------------
    fig.add_trace(go.Scatterpolar(
        r=matched_values,
        theta=categories,
        fill='toself',
        name=f"Model: {matched_name}",
        line=dict(color='#2ca02c', width=2),
        fillcolor='rgba(44, 160, 44, 0.5)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickmode='linear',
                tick0=1,
                dtick=1
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        title=dict(text="Gap Analysis: Profile vs. Model Capability", x=0.5)
    )
    
    return fig
