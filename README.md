# PBL5_Illusion
Discovering the color effects on Rotating Snake

## Overview

This project investigates whether color contributes to the generation or amplify the motion illusions. 
The experiment involves showing participants both grayscale and colored patterns and asking them to find the rotation speed that cancels the illusion. The actual luminance values of the patterns are fixed to ensure consistency across trials.

## Project Structure

### Main Files and Directories

#### 4colorcombination
- **4colors.py**: Script for generating and displaying motion illusion patterns using four different colors.
- **4colorsresult.csv**: CSV file containing results from the 4-color combination experiments.

#### DisplayColorBlock
- **displaycolorLab.py**: Script for converting RGB colors to CIELab color space and visualizing the results.
- **displaycolorRGB.py**: Script for visualizing the RGB values of different colors used in the experiment.

#### SamedifferenceLevel
- **Color_samedifference**
  - **Color_fixeddifferenceLevel.py**: Script for conducting experiments with fixed differences in color levels.
  - **color_fixeddifference2.csv**: Cleaned CSV file containing results from the color same-difference level experiments.
- **Gray_samedifference**
  - **Gray_fixeddifferenceLevel.py**: Script for conducting experiments with fixed differences in grayscale levels.
  - **gray_fixeddifference2.csv**: Cleaned CSV file containing results from the grayscale same-difference level experiments.

### Experiment Workflow

1. **Data Collection**: Use the scripts in the `4colorcombination` and `SamedifferenceLevel` directories to collect data on motion illusions with different color and grayscale patterns.
2. **Data Analysis**: Analyze the cleaned data using the Jupyter notebooks file.

### Detailed File Descriptions

#### 4colorcombination/4colors.py
Generates and displays motion illusion patterns using four different colors. This script is used to run the experiment and collect data on how different color combinations affect the perception of motion illusions.

#### DisplayColorBlock/displaycolorLab.py
Converts RGB colors to CIELab color space and visualizes the results, to measure the actual luminance on display.

#### DisplayColorBlock/displaycolorRGB.py
Visualizes the RGB values of different colors used in the experiment, to measure the actual luminance on display.

#### SamedifferenceLevel/Color_samedifference/Color_fixeddifferenceLevel.py
Conducts experiments with fixed actual luminance differences in different color. 

#### SamedifferenceLevel/Gray_samedifference/Gray_fixeddifferenceLevel.py
Conducts experiments with fixed actual luminance differences in grayscale levels.

## Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook
- Required Python libraries: pandas, numpy, matplotlib, seaborn, cv2 (OpenCV), pygame

### Installation

1. Clone the repository:
2. 
   ```bash
   git clone https://github.com/yourusername/PBL5_ILLUSIONS_PROJECT.git
   cd PBL5_ILLUSIONS_PROJECT
   ```

3. Install the required Python libraries:
   
    ```
    pip install pandas numpy matplotlib seaborn opencv-python pygame
    ```
### Analyzing the Results
Run the Jupyter notebook for data analysis


