# EV Charging Optimizer

## Project overview

EV Charging Optimizer is an individual Python data analytics project developed as part of my course final assignment. The project follows the spirit of Option 1, where the goal is to develop a data analytics program.

Instead of analyzing a static JSON dataset, this project analyzes EV charging cost scenarios using user-provided electricity price, solar production, and charging demand values. The result is an interactive Streamlit dashboard that helps compare charging an electric vehicle now versus charging later at night.

The project was completed individually with the teacher's approval.

## Live application

Streamlit app:

https://ev-charging-optimizer.streamlit.app/

## GitHub repository

https://github.com/IsraelGarcia666/EV-Charging-Optimizer

## Problem and motivation

Electric vehicle charging costs can be difficult to understand because the final cost depends on several variables:

- electricity spot price
- solar production
- EV charging demand
- grid usage after solar production
- day and night distribution fees
- electricity tax
- strategic stockpile fee
- electricity seller margin

The purpose of this app is to make these calculations easier to understand and to support better charging decisions.

## Core idea of the model

The main idea of this project is not only to check whether solar production fully covers the EV charging demand. Full solar coverage is easy to understand: if solar production is equal to or higher than the car demand, the grid usage becomes zero and charging is clearly optimal.

However, the more interesting situation happens when solar production only covers part of the EV demand. For example, in the morning or evening, solar production may be 1.0 kW while the car demand is 2.8 kW. In that case, the car still needs electricity from the grid, but less than it would need without solar.

The app compares this partial-solar scenario against charging later at night. Night charging may have a lower distribution fee, but it normally assumes no solar production. Therefore, the decision is not always obvious.

The model asks:

````text
Is charging now with partial solar production cheaper than charging later at night with full grid usage?

## Main features

The app allows the user to enter:

- solar production in kW
- current electricity price in c/kWh
- EV charging demand in kW
- night electricity price in c/kWh
- selected hour of the day

The app calculates:

- variable all-in electricity price now
- grid usage after solar production
- cost without solar
- cost with solar
- savings from solar
- night charging cost
- money saved by charging now
- charging recommendation: BEST, GOOD, or WAIT

## Technologies used

- Python
- Streamlit
- pandas
- matplotlib
- HTML/CSS for custom styling
- Excel for the initial calculation model
- Git and GitHub
- Streamlit Community Cloud

## How to run locally

Install the required packages:

```bash
pip install -r requirements.txt
````
