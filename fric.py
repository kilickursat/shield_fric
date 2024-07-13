import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
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

def create_tbm_animation(tbm_properties, depth, water_table_depth, vertical_stress, horizontal_stress, pore_pressure, shield_friction):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-tbm_properties.diameter, tbm_properties.diameter * 2)
    ax.set_ylim(-tbm_properties.diameter, depth + tbm_properties.diameter)
    ax.set_aspect('equal')

    # Ground surface
    ax.axhline(y=0, color='brown', linewidth=2)
    
    # Water table
    ax.axhline(y=-water_table_depth, color='blue', linestyle='--', linewidth=1)
    ax.text(tbm_properties.diameter * 1.5, -water_table_depth, 'Water Table', color='blue', va='bottom')

    # Soil layers
    soil = patches.Rectangle((-tbm_properties.diameter, -depth), tbm_properties.diameter * 3, depth, 
                             facecolor='tan', edgecolor='none', alpha=0.3)
    ax.add_patch(soil)

    # TBM
    tbm = patches.Rectangle((0, -depth), tbm_properties.length, tbm_properties.diameter, 
                            facecolor='gray', edgecolor='black')
    ax.add_patch(tbm)

    # Stress arrows
    arrow_props = dict(arrowstyle='->', color='r', lw=2)
    ax.annotate('', xy=(tbm_properties.length/2, -depth + tbm_properties.diameter/2), 
                xytext=(tbm_properties.length/2 + tbm_properties.diameter/4, -depth + tbm_properties.diameter/2), 
                arrowprops=arrow_props)
    ax.annotate('', xy=(tbm_properties.length, -depth + tbm_properties.diameter/2), 
                xytext=(tbm_properties.length, -depth + tbm_properties.diameter/2 + tbm_properties.diameter/4), 
                arrowprops=arrow_props)

    # Labels
    ax.text(tbm_properties.length/2, -depth + tbm_properties.diameter * 1.1, f'Vertical Stress: {vertical_stress/1000:.2f} kPa', 
            ha='center', va='bottom')
    ax.text(tbm_properties.length * 1.1, -depth + tbm_properties.diameter/2, f'Horizontal Stress: {horizontal_stress/1000:.2f} kPa', 
            ha='left', va='center')
    ax.text(0, -depth - tbm_properties.diameter * 0.1, f'Shield Friction: {shield_friction/1000:.2f} kN', 
            ha='left', va='top')

    # Pore pressure
    if depth > water_table_depth:
        pore_arrow = patches.Arrow(tbm_properties.length/2, -depth, 0, pore_pressure/(vertical_stress*2), 
                                   width=tbm_properties.diameter/2, color='blue', alpha=0.5)
        ax.add_patch(pore_arrow)
        ax.text(tbm_properties.length/2, -depth + pore_pressure/(vertical_stress*4), 
                f'Pore Pressure: {pore_pressure/1000:.2f} kPa', ha='center', va='center', color='blue')

    ax.set_title('TBM Shield Friction Visualization')
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Depth (m)')

    # Animation function
    def animate(frame):
        tbm.set_x(frame * tbm_properties.length / 100)
        return tbm,

    anim = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
    return fig, anim

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
        fig, anim = create_tbm_animation(tbm_properties, depth, water_table_depth, vertical_stress, horizontal_stress, pore_pressure, shield_friction)
        st_animation = st.pyplot(fig)

        # Animate the plot
        for i in range(100):
            anim.event_source.start()
            plt.close(fig)
            st_animation.pyplot(fig)

    display_formulas()

if __name__ == "__main__":
    main()
