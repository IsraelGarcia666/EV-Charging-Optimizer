# EV Charging Optimizer

## Project overview

EV Charging Optimizer is an individual Python data analytics project developed as part of my final assignment for the Basics of Programming course at Laurea University of Applied Sciences. The project follows the spirit of Option 1, where the goal is to develop a data analytics program.

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

## Excel model documentation

The calculation model was first developed and tested in Excel before being implemented in Python and Streamlit. The Excel model helped define the variables, formulas, and comparison logic used in the app.

- [Excel calculation model](docs/EV_Charging_Optimizer_Model.xlsx)
- [Model explanation document](docs/EV_Charging_Optimizer_Excel_Model_Explanation.docx)

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

## Current limitations

The current version is a working prototype, but it still has some limitations:

- Electricity prices are entered manually. The app does not yet fetch real hourly spot prices automatically from an API.
- Solar production is also entered manually. The app does not yet use hourly solar production data or solar forecast data.
- The daily simulation chart is simplified because it repeats the same solar production value across the day.
- The app compares charging now against a manually entered night electricity price, rather than automatically checking all future hours.
- Mobile layout works, but the app is currently more comfortable to use on desktop or tablet screens.
- Fixed monthly fees are not included in the hourly optimization model because they are paid regardless of charging time. They are better handled separately in a monthly cost estimate.

## Future development

Possible future improvements include:

- Connect the app to an electricity price API to fetch real hourly spot prices automatically.
- Add hourly solar production data or solar forecast data.
- Improve the daily simulation so it can identify the real best charging window automatically.
- Add a monthly cost estimate that includes fixed monthly fees separately from variable kWh-based costs.
- Improve the mobile layout for smaller screens.
- Add support for saving previous calculations.
- Add a JSON or database-based data input option to better match future data analytics use cases.
- Add clearer charts showing price, solar production, grid usage, and charging cost over time.

## What I learned

During this project, I learned how to turn a real-life problem into a working data analytics application. I first developed the calculation logic in Excel and then translated the model into Python and Streamlit.

I practiced working with:

- Python variables, formulas, and conditional logic
- Streamlit input widgets and dashboard layout
- pandas DataFrames for organizing simulation data
- matplotlib charts for visualizing price and grid usage
- Git and GitHub for version control
- Streamlit Community Cloud for deploying the app online
- HTML/CSS styling inside a Streamlit app

I also learned that building a useful app is not only about writing code. A large part of the work was understanding the real-world pricing logic, checking the formulas, improving the user interface, and explaining the model clearly.

One important learning outcome was the difference between fixed monthly fees and variable kWh-based costs. Fixed monthly fees are paid regardless of charging time, while variable costs affect the decision of whether charging now or later is cheaper.

Another important learning outcome was understanding partial solar coverage. Even when solar production does not fully cover EV charging demand, it can still reduce grid usage enough to make charging now cheaper than charging later at night.

## Use of AI assistance

AI tools were used during this project as a learning and development support tool. The main project idea, energy-cost logic, Excel model decisions, testing, and final implementation choices were developed and reviewed by me.

AI assistance was used for:

- debugging Python and Streamlit errors
- explaining code and formulas
- improving wording and documentation
- supporting layout and UX ideas
- generating a futuristic background image for the app
- helping structure the README and project explanation

The calculations, project direction, testing decisions, and final submitted work were reviewed and adapted by me. The app was built as an individual course project with teacher approval.
