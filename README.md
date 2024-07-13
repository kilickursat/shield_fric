# TBM Shield Friction Calculator
Kursat Kilic reserves all the rights, please get in touch with me to use the app.
## Overview

The TBM Shield Friction Calculator is an interactive web application designed to calculate and visualize the shield friction of a Tunnel Boring Machine (TBM). This tool is valuable for engineers, researchers, and students working in the field of tunneling and geotechnical engineering.

## Features

- Calculate TBM shield friction based on various soil and machine parameters
- Interactive input of soil properties, TBM characteristics, and environmental conditions
- Real-time calculation and display of results
- Dynamic visualization of the TBM and acting forces
- Display of relevant empirical formulas used in calculations

## Installation

To set up the TBM Shield Friction Calculator on your local machine, follow these steps:

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/tbm-shield-friction-calculator.git
   cd tbm-shield-friction-calculator
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application:

1. Ensure you're in the project directory and your virtual environment is activated (if you're using one).

2. Run the Streamlit app:
   ```
   streamlit run tbm_shield_friction_app.py
   ```

3. Your default web browser should open automatically with the application. If it doesn't, you can access the app by navigating to the URL displayed in your terminal (usually `http://localhost:8501`).

4. Use the sidebar to input parameters for your calculation.

5. Click the "Calculate and Visualize" button to see the results and visualization.

## Input Parameters

- **Tunnel Depth**: Depth of the tunnel (m)
- **Water Table Depth**: Depth of the water table (m)
- **Soil Properties**:
  - Density (kg/m³)
  - Cohesion (Pa)
  - Friction Angle (degrees)
  - Coefficient of Lateral Earth Pressure at Rest
- **TBM Properties**:
  - Diameter (m)
  - Shield Length (m)
  - Weight (N)
  - Face Pressure (Pa)
- **Shield-Soil Friction Coefficient**
- **Stress Calculation Method**: Choose between At Rest, Active, or Passive earth pressure theories

## Output

The calculator provides the following outputs:

- Vertical Stress (Pa)
- Horizontal Stress (Pa)
- Pore Water Pressure (Pa)
- Effective Stress (Pa)
- Normal Force on Shield (N)
- Shield Friction (N)
- Total Resistance (including TBM weight) (N)
- Visual representation of the TBM and acting forces

## Contributing

Contributions to improve the TBM Shield Friction Calculator are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was inspired by the need for accessible tools in tunnel engineering education and practice.
