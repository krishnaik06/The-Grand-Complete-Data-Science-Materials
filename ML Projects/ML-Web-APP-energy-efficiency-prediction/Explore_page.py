import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('cleaned_housing_data.csv')

def  show_explore_page():
    st.markdown(
        """
        <div style="background-color: #3498db; padding: 10px; border-radius: 10px;">
            <h1 style="color: white;">EXPLORE THE PROPERTY ATTRIBUTES OF BUILDINGS IN NOTTINGHAM</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("""### distribution of property types""")
    data=df["PROPERTY_TYPE"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

    st.write("""### distribution of built form""")
    data=df["BUILT_FORM"].value_counts()
    st.bar_chart(data)

    st.write("""### distribution of Hot water source""")
    data=df["HOTWATER_source"].value_counts()
    st.bar_chart(data)

    st.write("""### distribution of Energy Ratings""")
    data=df["CURRENT_ENERGY_RATING"].value_counts()
    st.bar_chart(data)


    
    st.write("""### Average heating cost in each energy rating""")
    data = df.groupby(["CURRENT_ENERGY_RATING"])["HEATING_COST_CURRENT"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Energy rating by total floor area""")
    data= df.groupby(["CURRENT_ENERGY_RATING"])["TOTAL_FLOOR_AREA"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Heating Cost by number of rooms""")
    data = df.groupby(["NUMBER_HABITABLE_ROOMS"])["HEATING_COST_CURRENT"].mean().sort_values(ascending=True)
    st.line_chart(data)






    

    
