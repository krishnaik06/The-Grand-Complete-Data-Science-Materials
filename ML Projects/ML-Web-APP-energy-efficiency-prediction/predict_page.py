import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
nn = data["model"]
le_property = data["le_property"]
le_built = data["le_built"]
le_water = data["le_water"]
le_walls = data["le_walls"]
le_heat = data["le_heat"]
scaler = data["scaler"]

def show_predict_page():
    st.markdown(
        """
        <div style="background-color: #3498db; padding: 10px; border-radius: 10px;">
            <h1 style="color: white;">ML MODEL FOR ENERGY EFFICIENCY AMONG BUILDINGS</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("""### Please enter your Property Attributes to predict your energy efficiency rating""")

    

    PROPERTY_TYPE = (
        "House",
        "Flat",
        "Bungalow",
        "Maisonette",
    )
    BUILT_FORM = ( 
        "Mid-Terrace",
        "Semi-Detached",
        "End-Terrace", 
        "Detached", 
        "Enclosed Mid-Terrace", 
        "Enclosed End-Terrace",
    )
    HOTWATER_source = ( 
        "Main System",
        "Electric heat pump",
        "Community Scheme", 
        "No system present",
        "Gas boiler",
        "Secondary system",
    )
    WALLS_CATEGORY = (
        "no insulation",
        "Insulated",
        "External insulation",
        "partial insulation",
        "internal insulation",
    )
    MAINHEAT_DESCRIPTION = (
        "Boiler and radiators", 
        "Electric storage heaters", 
        "Electric room heaters", 
        "Community scheme",
        "Gas room heater",
        "No system present",
        "Underfloor Boilers",
        "Warm Air(electric/gas)",
        "Portable electric heaters",
        "Radiators and Electric heater",
        "Fuel Room heater",
        "Heat pumps (Air, water)",
        "Electric ceiling heating",
    )

    PROPERTY_TYPE = st.selectbox("PROPERTY TYPE", PROPERTY_TYPE)
    BUILT_FORM = st.selectbox("BUILT FORM", BUILT_FORM)
    HEATING_COST_CURRENT = st.slider("RECENT TOTAL COST FOR HEATING", 0, 41862, 10)
    TOTAL_FLOOR_AREA = st.slider("Total floor area", 20, 70, 20)
    NUMBER_HABITABLE_ROOMS = st.slider("Number of habitable Rooms", 0, 70, 3)
    NUMBER_OPEN_FIREPLACES =st.slider("Number of open fireplace", 0, 70, 3)
    HOTWATER_source = st.selectbox("HOTWATER SOURCE", HOTWATER_source)
    WALLS_CATEGORY = st.selectbox("WALLS CATEGORY", WALLS_CATEGORY)
    MAINHEAT_DESCRIPTION = st.selectbox("MAIN HEATING DESCRIPTION", MAINHEAT_DESCRIPTION)

    OK = st.button("predict")
    if  OK:
        TEST = np.array([[PROPERTY_TYPE, BUILT_FORM, HEATING_COST_CURRENT, TOTAL_FLOOR_AREA, NUMBER_HABITABLE_ROOMS, NUMBER_OPEN_FIREPLACES, HOTWATER_source, WALLS_CATEGORY, MAINHEAT_DESCRIPTION]])
        TEST[:, 0] = le_property.transform(TEST[:, 0])
        TEST[:, 1] = le_built.transform(TEST[:, 1])
        TEST[:, 6] = le_water.transform(TEST[:, 6])
        TEST[:, 7] = le_walls.transform(TEST[:, 7])
        TEST[:, 8] = le_heat.transform(TEST[:, 8])
        numerical_values = TEST[:, 2:6].astype(float)
        scaled_values = scaler.transform(numerical_values)
        TEST[:, 2:6] = scaled_values
        TEST = TEST.astype(float)

        ENERGY_RATING = nn.predict(TEST)
        st.subheader(f"Your Property Energy rating is {ENERGY_RATING[0]:}")
    
    st.write("""**Energy ratings range from A to G, with A being considered the most energy-efficient, indicating the highest level of energy performance, and G being the least energy**""")















