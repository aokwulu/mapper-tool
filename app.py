import streamlit as st
from core.data_loader import load_data, get_dimensions, FORMALISMS_PATH, PRESETS_PATH
from core.matcher import find_closest_model, calculate_gaps, generate_recommendation_text
from core.visualiser import create_single_radar, create_comparison_radar

# config -------------------------------------------------------------------------

st.set_page_config(
    page_title="Dissertation Visualiser", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dissertation Visualiser")
st.markdown("""
This decision-support toolkit helps users align their target adversary profiles 
with a choice of Modelling & Simulation (M&S) formalism.
""")
st.divider()

# load the data -------------------------------------------------------------------------

formalisms_data = load_data(FORMALISMS_PATH)
presets_data = load_data(PRESETS_PATH)
dimensions = get_dimensions()

# side bar ------------------------------------------------------------------------

mode = st.sidebar.radio(
    "Options:",
    ["View Formalism", "Query Preset Adversary Profile", "Query Custom Adversary Profile"]
)

# view formalism --------------------------------------------------------------------
if mode == "View Formalism":
    st.header("Explore Formalism Assumptions")
    st.write("Select a mathematical formalism to view its assumptions of adversary behaviour.")
    
    selected_model = st.selectbox("Select Formalism:", formalisms_data.index.tolist())
    
    if selected_model:
        model_profile = formalisms_data.loc[selected_model].to_dict()
        
        # radar chart
        fig = create_single_radar(selected_model, model_profile)
        st.plotly_chart(fig, use_container_width=True)
        
        # raw scores
        with st.expander("View Raw Dimension Scores"):
            cols = st.columns(len(dimensions))
            for i, dim in enumerate(dimensions):
                cols[i].metric(label=dim, value=model_profile.get(dim, 1))

# view profile ------------------------------------------------------------------------------------
elif mode == "Query Preset Adversary Profile":
    st.header("Match an Adversary Archetype")
        
    st.write("Select an adversary archetype to find the most suitable M&S formalism.")
    
    selected_preset = st.selectbox("Select Archetype:", list(presets_data.index))
    
    if selected_preset:
        target_profile = presets_data.loc[selected_preset].to_dict()
        
        # find the closest formalism
        best_match_name, best_match_profile = find_closest_model(target_profile, formalisms_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # comparison radar chart
            fig = create_comparison_radar(selected_preset, target_profile, best_match_name, best_match_profile)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.success(f"**Primary Recommendation:** {best_match_name}")
            gaps = calculate_gaps(target_profile, best_match_profile)
            warning_text = generate_recommendation_text(best_match_name, gaps)    
            if gaps:
                st.warning(warning_text)
            else:
                st.info(warning_text)

# custom profile ------------------------------------------------------------------------------------

elif mode == "Query Custom Adversary Profile":
    st.header("Design Custom Adversary Profile")
    st.write("Adjust the sliders below to define a specific threat actor. The engine will dynamically recommend the most suitable formalism")
    
    target_profile = {}

    cols = st.columns(3)
    for i, dim in enumerate(dimensions):
        with cols[i % 3]:
            # Default to 3 (Moderate)
            target_profile[dim] = st.slider(f"{dim} Score", min_value=1, max_value=5, value=3, step=1)
            
    st.divider()

    best_match_name, best_match_profile = find_closest_model(target_profile, formalisms_data)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = create_comparison_radar("Custom Threat", target_profile, best_match_name, best_match_profile)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.success(f"**Primary Recommendation:** {best_match_name}")
        
        gaps = calculate_gaps(target_profile, best_match_profile)
        warning_text = generate_recommendation_text(best_match_name, gaps)
        
        if gaps:
            st.warning(warning_text)
        else:
            st.info(warning_text)
