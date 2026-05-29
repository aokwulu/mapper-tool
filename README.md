
# diss

## file structure

adversary-mapper-toolkit/
│
├── data/
│   ├── formalisms.csv <- average scores from each formalism
│   └── presets.csv <-  predefined adversary archetypes derived from the script
|   └-- raw_data.csv <- all papers and their scores from gap analysis
|   └-- derive_profiles.py <- performs k means clustering to derive the adversary profiles
|
│
├── core/
│   ├── __init__.py
│   ├── data_loader.py <- handles parsing and validating the JSON
│   ├── matcher.py <- contains the Euclidean math and gap analysis logic
│   └── visualiser.py <- wraps Plotly graph objects to generate radar charts
│
├── app.py <- the main Streamlit interface application
├── requirements.txt <- dependencies
└── README.md <- this file

## how to run

1. make sure that all the required dependencies are installed. dependencies and their respective versions can be found in requirements.txt
2. ensure that you are in the root directory
3. run with `streamlit run app.py` and a tab should open in your browser

## academic integrity

- all code is mine and was written by me, the following tools helped with automation
  - the structure of docstrings was generated using the autoDocstring VS code extension
