import streamlit as st
import math
import plotly.graph_objs as go
import numpy as np

class SoilProperties:
    def __init__(self, density, cohesion, friction_angle, k0):
        self.density = density
        self.cohesion = cohesion
        self.friction_angle = math.radians(friction_angle)
        self.k0 = k0

class TBMProperties:
    def __init__(self, diameter, length, weight, face_pressure):
        self.diameter = diameter
        self.length = length
        self.weight = weight
        self.face_pressure = face_pressure

def calculate_vertical_stress(depth, soil_properties):
    g = 9.81
    return soil_properties.density * g * depth

def calculate_horizontal_stress(vertical_stress, soil_properties, method):
    if method == 'At Rest':
        return soil_properties.k0 * vertical_stress
    elif method == 'Active':
        ka = math.tan(math.pi/4 - soil_properties.friction_angle/2)**2
        return ka * vertical_stress - 2 * soil_properties.cohesion * math.sqrt(ka)
    elif method == 'Passive':
        kp = math.tan(math.pi/4 + soil_properties.friction_angle/2)**2
        return kp * vertical_stress + 2 * soil_properties.cohesion * math.sqrt(kp)

def calculate_pore_pressure(depth, water_table_depth):
    g = 9.81
    water_density = 1000
    if depth > water_table_depth:
        return water_density * g * (depth - water_table_depth)
    return 0

def calculate_effective_stress(total_stress, pore_pressure):
    return total_stress - pore_pressure

def calculate_shield_surface_area(tbm_properties):
    return math.pi * tbm_properties.diameter * tbm_properties.length

def calculate_normal_force(effective_stress, tbm_properties):
    shield_area = calculate_shield_surface_area(tbm_properties)
    return (effective_stress + tbm_properties.face_pressure) * shield_area

def calculate_shield_friction(normal_force, friction_coefficient):
    return friction_coefficient * normal_force

def calculate_total_resistance(shield_friction, tbm_properties):
    return shield_friction + tbm_properties.weight

def create_tbm_visualization(tbm_properties, depth, water_table_depth, vertical_stress, horizontal_stress, pore_pressure, shield_friction):
    fig = go.Figure()

    # Ground surface
    fig.add_trace(go.Scatter(x=[-tbm_properties.diameter, tbm_properties.diameter * 2], y=[0, 0],
                             mode='lines', name='Ground Surface', line=dict(color='brown', width=2)))

    # Water table
    fig.add_trace(go.Scatter(x=[-tbm_properties.diameter, tbm_properties.diameter * 2], y=[-water_table_depth, -water_table_depth],
                             mode='lines', name='Water Table', line=dict(color='blue', width=2, dash='dash')))

    # Soil
    fig.add_trace(go.Scatter(x=[-tbm_properties.diameter, tbm_properties.diameter * 2, tbm_properties.diameter * 2, -tbm_properties.diameter],
                             y=[0, 0, -depth, -depth],
                             fill='toself', fillcolor='tan', opacity=0.3, name='Soil', line=dict(color='tan')))

    # TBM
    fig.add_trace(go.Scatter(x=[0, tbm_properties.length, tbm_properties.length, 0],
                             y=[-depth - tbm_properties.diameter/2, -depth - tbm_properties.diameter/2,
                                -depth + tbm_properties.diameter/2, -depth + tbm_properties.diameter/2],
                             fill='toself', fillcolor='gray', name='TBM', line=dict(color='black')))

    # Stress arrows and labels
    arrow_length = tbm_properties.diameter / 4
    fig.add_annotation(x=tbm_properties.length/2, y=-depth,
                       ax=tbm_properties.length/2, ay=-depth - arrow_length,
                       text="", showarrow=True, arrowhead=2, arrowsize=1.5, arrowcolor="red", arrowwidth=2)
    fig.add_annotation(x=tbm_properties.length, y=-depth + tbm_properties.diameter/2,
                       ax=tbm_properties.length + arrow_length, ay=-depth + tbm_properties.diameter/2,
                       text="", showarrow=True, arrowhead=2, arrowsize=1.5, arrowcolor="red", arrowwidth=2)

    # Labels
    fig.add_annotation(x=tbm_properties.length/2, y=-depth + tbm_properties.diameter * 0.6,
                       text=f'Vertical Stress: {vertical_stress/1000:.2f} kPa',
                       showarrow=False, yshift=10)
    fig.add_annotation(x=tbm_properties.length * 1.1, y=-depth + tbm_properties.diameter/2,
                       text=f'Horizontal Stress: {horizontal_stress/1000:.2f} kPa',
                       showarrow=False, xshift=5)
    fig.add_annotation(x=0, y=-depth - tbm_properties.diameter * 0.6,
                       text=f'Shield Friction: {shield_friction/1000:.2f} kN',
                       showarrow=False, yshift=-10)

    # Pore pressure
    if depth > water_table_depth:
        pore_arrow_length = pore_pressure / (vertical_stress * 2) * tbm_properties.diameter
        fig.add_annotation(x=tbm_properties.length/2, y=-depth,
                           ax=tbm_properties.length/2, ay=-depth + pore_arrow_length,
                           text="", showarrow=True, arrowhead=2, arrowsize=1.5, arrowcolor="blue", arrowwidth=2)
        fig.add_annotation(x=tbm_properties.length/2, y=-depth + pore_arrow_length/2,
                           text=f'Pore Pressure: {pore_pressure/1000:.2f} kPa',
                           showarrow=False, font=dict(color="blue"))

    fig.update_layout(
        title='TBM Shield Friction Visualization',
        xaxis_title='Distance (m)',
        yaxis_title='Depth (m)',
        showlegend=False,
        yaxis_range=[-depth - tbm_properties.diameter, tbm_properties.diameter],
        xaxis_range=[-tbm_properties.diameter, tbm_properties.diameter * 2],
        height=600,
        width=800
    )

    return fig

def display_formulas():
    st.write("### Empirical Formulas for Shield Friction Calculation")
    
    st.latex(r"\text{Vertical Stress: } \sigma_v = \rho g h")
    st.write("Where:")
    st.write("- σv: Vertical stress")
    st.write("- ρ: Soil density")
    st.write("- g: Gravitational acceleration (9.81 m/s²)")
    st.write("- h: Depth")
    
    st.latex(r"\text{Horizontal Stress: } \sigma_h = K \sigma_v")
    st.write("Where K is:")
    st.latex(r"K_0 = \text{At Rest Earth Pressure Coefficient}")
    st.latex(r"K_a = \tan^2(45° - \phi/2) \text{ (Active)}")
    st.latex(r"K_p = \tan^2(45° + \phi/2) \text{ (Passive)}")
    st.write("φ: Soil friction angle")
    
    st.latex(r"\text{Pore Water Pressure: } u = \gamma_w (h - h_w)")
    st.write("Where:")
    st.write("- u: Pore water pressure")
    st.write("- γw: Unit weight of water")
    st.write("- hw: Water table depth")
    
    st.latex(r"\text{Effective Stress: } \sigma' = \sigma - u")
    
    st.latex(r"\text{Normal Force: } N = (\sigma' + P_f) A")
    st.write("Where:")
    st.write("- N: Normal force")
    st.write("- Pf: Face pressure")
    st.write("- A: Shield surface area")
    
    st.latex(r"\text{Shield Friction: } F_f = \mu N")
    st.write("Where:")
    st.write("- Ff: Shield friction")
    st.write("- μ: Friction coefficient")
    
    st.latex(r"\text{Total Resistance: } R = F_f + W")
    st.write("Where:")
    st.write("- R: Total resistance")
    st.write("- W: TBM weight")

def main():
    st.title("Advanced TBM Shield Friction Calculator with Visualization")

    st.sidebar.header("Input Parameters")
    
    depth = st.sidebar.number_input("Tunnel Depth (m)", value=10.0, step=0.1)
    water_table_depth = st.sidebar.number_input("Water Table Depth (m)", value=5.0, step=0.1)
    
    st.sidebar.subheader("Soil Properties")
    density = st.sidebar.number_input("Soil Density (kg/m³)", value=1800.0, step=10.0)
    cohesion = st.sidebar.number_input("Soil Cohesion (Pa)", value=5000.0, step=100.0)
    friction_angle = st.sidebar.number_input("Soil Friction Angle (degrees)", value=30.0, step=0.1)
    k0 = st.sidebar.number_input("Coefficient of Lateral Earth Pressure at Rest", value=0.5, step=0.01)
    
    soil_properties = SoilProperties(density, cohesion, friction_angle, k0)
    
    st.sidebar.subheader("TBM Properties")
    diameter = st.sidebar.number_input("TBM Diameter (m)", value=6.0, step=0.1)
    length = st.sidebar.number_input("TBM Shield Length (m)", value=10.0, step=0.1)
    weight = st.sidebar.number_input("TBM Weight (N)", value=5e6, step=1e5)
    face_pressure = st.sidebar.number_input("TBM Face Pressure (Pa)", value=2e5, step=1e4)
    
    tbm_properties = TBMProperties(diameter, length, weight, face_pressure)
    
    friction_coefficient = st.sidebar.number_input("Shield-Soil Friction Coefficient", value=0.3, step=0.01)
    stress_calculation_method = st.sidebar.selectbox("Stress Calculation Method", ['At Rest', 'Active', 'Passive'])

    if st.sidebar.button("Calculate and Visualize"):
        vertical_stress = calculate_vertical_stress(depth, soil_properties)
        horizontal_stress = calculate_horizontal_stress(vertical_stress, soil_properties, stress_calculation_method)
        pore_pressure = calculate_pore_pressure(depth, water_table_depth)
        effective_stress = calculate_effective_stress(horizontal_stress, pore_pressure)
        normal_force = calculate_normal_force(effective_stress, tbm_properties)
        shield_friction = calculate_shield_friction(normal_force, friction_coefficient)
        total_resistance = calculate_total_resistance(shield_friction, tbm_properties)

        st.write("### Results")
        st.write(f"Vertical Stress: {vertical_stress:.2f} Pa")
        st.write(f"Horizontal Stress: {horizontal_stress:.2f} Pa")
        st.write(f"Pore Water Pressure: {pore_pressure:.2f} Pa")
        st.write(f"Effective Stress: {effective_stress:.2f} Pa")
        st.write(f"Normal Force on Shield: {normal_force:.2f} N")
        st.write(f"Shield Friction: {shield_friction:.2f} N")
        st.write(f"Total Resistance (including TBM weight): {total_resistance:.2f} N")

        st.write("### TBM Shield Friction Visualization")
        fig = create_tbm_visualization(tbm_properties, depth, water_table_depth, vertical_stress, horizontal_stress, pore_pressure, shield_friction)
        st.plotly_chart(fig)

    display_formulas()

if __name__ == "__main__":
    main()
