import streamlit as st
import rustlib as rl

st.title("Heat Exchanger Simulator")

# Tabs
tabs = st.tabs(
    ["Heat Exchanger Type", "HX setup", "Numerics", "Physics", "Constraints", "Results"]
)

# Tab 1: Heat Exchanger Type
with tabs[0]:
    exchanger_type = st.selectbox("Select heat exchanger type", ["Straight rack"])
    flow_orientation = st.selectbox(
        "Select flow orientation", ["co-flow", "Counter-flow"]
    )

    external_flow_direction = st.selectbox(
        "Select flow direction", ["Out-in", "In-out"]
    )

# Tab 2: Boundary Conditions
with tabs[1]:
    st.title(f"Case set up")
    with st.container():
        st.subheader(f"Boundary conditions")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Boundary conditions for Tube side flow")
            fluid_water = st.selectbox("Fluid", ["Water"])
            st.number_input("Tube side inlet temperature (°C)", value=100)
            st.number_input("Tube side inlet pressure (kPa)", value=30)
            st.number_input("Tube side mass flow (kg/s)", value=1)
        with col2:
            st.write(f"Boundary conditions for Shell side flow")
            fluid_air = st.selectbox("Fluid", ["Air"])
            st.number_input("Shell side inlet temperature (°C)", value=100)
            st.number_input("Shell side inlet pressure (kPa)", value=30)
            st.number_input("Shell side mass flow (kg/s)", value=1)
    with st.container():
        st.subheader(f"Geometry definition")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Tube spacing")
            st.number_input("Xt (mm)", value=1.1)
            st.number_input("Xl (mm)", value=1.1)
        with col2:
            st.write(f"Tube properties")
            st.number_input("Tube OD (mm)", value=1.5)
            st.number_input("Tube wall thickness (mm)", value=0.15)
            st.number_input("Tube length (mm)", value=100)
            tube_material = 


# Tab 3: Correlations (e.g. vary choices based on exchanger type)
with tabs[2]:
    st.write(f"Choose correlations for: **{exchanger_type}**")
    if exchanger_type == "Shell and Tube":
        st.selectbox("Correlation", ["Dittus-Boelter", "Sieder-Tate", "Gnielinski"])
    elif exchanger_type == "Plate":
        st.selectbox("Correlation", ["Martin", "Kakaç–Shah"])
    elif exchanger_type == "Air Cooled":
        st.selectbox("Correlation", ["Zukauskas", "Colburn"])

if st.button("Run Simulation"):
    with tabs[3]:
        results = 2 * 3

        st.subheader("Results")
        st.write(f"NTU: {results}")
