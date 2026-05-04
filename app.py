import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt

# NOTE TO SELF:
# streamlit = builds the app interface
# base64 = allows local background image to be used in CSS
# pandas = creates tables/dataframes for charts
# matplotlib = creates custom charts with more control than st.line_chart

# ---------- PAGE CONFIG ----------
# NOTE TO SELF:
# This must be the first Streamlit command.
# "wide" gives the app more horizontal space, useful for dashboard layouts.
st.set_page_config(page_title="EV Charging Optimizer", layout="wide")


# ---------- BACKGROUND IMAGE ----------
# NOTE TO SELF:
# This function converts the local image file into base64 so the browser can use it as background.
def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()


img = get_base64_image("Background_2.png")


# ---------- CSS / VISUAL STYLE ----------
# NOTE TO SELF:
# This block controls the visual design:
# - background image
# - dark overlay
# - title colors
# - glass effect
# - forcing dashboard columns to stay side by side
st.markdown(
    f"""
    <style>

    /* Main app background */
    .stApp {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Dark overlay above background image */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.55);
        z-index: -1;
    }}

    /* Main page width */
    .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    /* Headings */

    /* Custom title styles */
    /* NOTE TO SELF:
       app-title controls the big main title.
       section-title controls the smaller dashboard box titles.
    */

    .app-title {{
        color: #ff6600 !important;
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        margin: 0;
    }}

    .section-title {{
        color: #ffd700 !important;
        text-align: center;
        font-size: 34px;
        font-weight: 800;
        margin: 0;
    }}

    label {{
        color: white !important;
        font-weight: 600 !important;
    }}

    /* Glass effect on Streamlit content boxes */
    div[data-testid="stVerticalBlock"] > div {{
        background: rgba(0, 0, 0, 0.38);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.18);
    }}

    /* Responsive dashboard layout */
/* NOTE TO SELF:
   Desktop: keep columns side by side.
   Mobile/tablet: allow columns to wrap so they don't get crushed.
*/

@media (min-width: 900px) {{
    div[data-testid="stHorizontalBlock"] {{
        flex-wrap: nowrap !important;
        gap: 1rem !important;
    }}

    div[data-testid="column"] {{
        min-width: 0 !important;
    }}
}}

@media (max-width: 899px) {{

    /* Force mobile dashboard into 2 columns instead of 1 */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.6rem !important;
    }}

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
        flex: 0 0 calc(50% - 0.6rem) !important;
        width: calc(50% - 0.6rem) !important;
        min-width: 0 !important;
    }}

    /* Make cards tighter on mobile */
    div[data-testid="stVerticalBlock"] > div {{
        padding: 12px !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
    }}

    /* Smaller mobile titles */
    .section-title {{
        font-size: 24px !important;
    }}

    .app-title {{
        font-size: 30px !important;
        line-height: 1.2 !important;
    }}

    /* Make number inputs fit better in narrow cards */
    div[data-testid="stNumberInput"] {{
        min-width: 0 !important;
        width: 100% !important;
    }}
}}

    /* Make text easier to read */
    p, span, div {{
        color: white;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ---------- TITLE CARD ----------
# NOTE TO SELF:
# This replaces st.title() so the title behaves more like a dashboard card.
st.markdown(
    """
    <div style="
        background: rgba(0,0,0,0.42);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 28px;
        backdrop-filter: blur(10px);
        text-align: center;
    ">
        <div class="app-title">EV Charging Optimizer</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- HOUR VALUE ----------
# NOTE TO SELF:
# The hour slider is visually shown later in the Controls box.
# But calculations need the hour earlier.
# session_state lets us read the last selected slider value before the slider appears.
hour = st.session_state.get("hour_slider", 12)


# ---------- ROW 1: MAIN DASHBOARD ----------
# NOTE TO SELF:
# input_col = user input values
# now_col = current charging / solar savings
# decision_col = night comparison and recommendation
input_col, now_col, decision_col = st.columns(3, gap="medium")


# ---------- INPUT CARD ----------
with input_col:
    st.markdown('<div class="section-title">Input Data</div>', unsafe_allow_html=True)

    solar = st.number_input(
        "Solar production (kW)",
        min_value=0.0,
        value=1.5,
        step=0.1
    )

    price = st.number_input(
        "Electricity price now (c/kWh)",
        min_value=-100.0,
        max_value=500.0,
        value=2.0,
        step=0.1
    )

    if price <= 0:
        st.success("⚡ Spot price is zero or negative")
    elif price > 100:
        st.warning("⚠️ Very high electricity price — avoid charging")

    demand = st.number_input(
        "Car demand (kW)",
        min_value=0.0,
        value=2.8,
        step=0.1
    )

    night_price_input = st.number_input(
        "Night electricity price (c/kWh)",
        min_value=-100.0,
        max_value=500.0,
        value=2.0,
        step=0.1
    )


# ---------- PRICE COMPONENTS ----------
# NOTE TO SELF:
# These are variable c/kWh costs used in the charging decision.
# Fixed monthly fees are NOT included here because they are paid regardless of charging time.

tax = 2.81              # c/kWh - Electricity tax 1
stockpile_fee = 0.02    # c/kWh - Strategic stockpile fee
margin = 0.6            # c/kWh - Electricity seller margin

# Fixed monthly fees are kept out of the hourly optimization.
# Network basic charge = 10.99 €/month
# Electricity seller basic fee = 4.96 €/month
fixed_monthly_fees = 10.99 + 4.96

# Day/night distribution based on selected hour
# NOTE TO SELF:
# 07:00–21:59 = daytime distribution
# 22:00–06:59 = night-time distribution
if 7 <= hour < 22:
    distribution = 3.3
else:
    distribution = 1.42

# Current all-in price
# NOTE TO SELF:
# This includes variable costs only:
# spot price + electricity tax + strategic stockpile fee + margin + distribution.
# Fixed monthly fees are shown separately and are not used in the timing decision.
real_price = price + tax + stockpile_fee + margin + distribution

# Current grid usage after solar
# NOTE TO SELF:
# If solar >= demand, grid becomes 0.
grid = max(0, demand - solar)

# What you pay now, after solar
cost = grid * real_price / 100

# What you would pay now without solar
full_grid_cost = demand * real_price / 100

# Savings created by solar power
solar_savings = full_grid_cost - cost

# Night scenario
# NOTE TO SELF:
# At night we assume no solar, so night_grid = full demand.
night_distribution = 1.42
night_price = night_price_input + tax + stockpile_fee + margin + night_distribution
night_grid = demand
night_cost = night_grid * night_price / 100

# Compare charging now vs charging at night
# Positive savings = charging now is better
# Negative savings = night is cheaper
savings = night_cost - cost

# Smart recommendation, copied from Excel logic
if grid == 0:
    recommendation = "BEST"
elif savings > 0:
    recommendation = "BEST"
elif abs(savings) < 0.01:
    recommendation = "GOOD"
else:
    recommendation = "WAIT"


# ---------- NOW / SOLAR CARD ----------
with now_col:
    st.markdown('<div class="section-title">Now</div>', unsafe_allow_html=True)

    st.write(f"Variable all-in price now: {real_price:.2f} c/kWh")
    st.write(f"Grid usage now: {grid:.2f} kW")

    st.write(
        f"Without solar, you would pay: "
        f"{full_grid_cost:.2f} € ({round(full_grid_cost * 100)} cents)"
    )

    st.write(
        f"With solar, you pay now: "
        f"{cost:.2f} € ({round(cost * 100)} cents)"
    )

    st.write(
        f"Savings from solar: "
        f"{solar_savings:.2f} € ({round(solar_savings * 100)} cents)"
    )


# ---------- DECISION CARD ----------
with decision_col:
    st.markdown('<div class="section-title">Decision</div>', unsafe_allow_html=True)

    st.write(
        f"Cost if you charge at night: "
        f"{night_cost:.2f} € ({round(night_cost * 100)} cents)"
    )

    st.write(
        f"Money saved by charging now: "
        f"{savings:.2f} € ({round(savings * 100)} cents)"
    )

    st.write(f"Fixed monthly fees excluded from timing decision: {fixed_monthly_fees:.2f} €/month")

    savings_cents = round(savings * 100)

    # NOTE TO SELF:
    # This block explains WHY the app recommends BEST / GOOD / WAIT.
    if recommendation == "BEST":
        if grid == 0:
            st.success("🟢 BEST — Charging fully with solar")
        elif savings > 0:
            st.success(
                f"🟢 BEST — Charging now saves {abs(savings_cents)} cents compared to night"
            )

    elif recommendation == "GOOD":
        st.info("🟡 GOOD — Cost is similar now and at night")

    else:
        st.error(f"🔴 WAIT — Night is cheaper by {abs(savings_cents)} cents")


# ---------- ROW 2: CHART + CONTROL AREA ----------
# NOTE TO SELF:
# chart_col = large chart area
# control_col = hour slider + best hour recommendation
chart_col, control_col = st.columns([2, 1], gap="medium")


# ---------- DAILY SIMULATION DATA ----------
# NOTE TO SELF:
# For now, the chart uses the same solar value for all hours.
# Later, replace this with hourly solar data from real production or forecast.

hours = list(range(24))
prices = []
grids = []
costs = []

for h in hours:
    # Day/night distribution logic
    # NOTE TO SELF:
    # 07:00–21:59 = daytime distribution
    # 22:00–06:59 = night-time distribution
    if 7 <= h < 22:
        dist = 3.3
    else:
        dist = 1.42

    hourly_real_price = price + tax + stockpile_fee + margin + dist
    hourly_grid = max(0, demand - solar)
    hourly_cost = hourly_grid * hourly_real_price / 100

    prices.append(hourly_real_price)
    grids.append(hourly_grid)
    costs.append(hourly_cost)

df = pd.DataFrame({
    "Hour": hours,
    "All-in price (c/kWh)": prices,
    "Grid usage (kW)": grids,
    "Cost (€)": costs
})


# ---------- FIND BEST HOUR ----------
# NOTE TO SELF:
# This is a simple best-hour calculation based on current inputs.
# Later this becomes more powerful when we use real hourly prices and hourly solar data.

best_hour = df.loc[df["Cost (€)"].idxmin(), "Hour"]
best_cost = df["Cost (€)"].min()


# ---------- CHART CARD ----------
with chart_col:
    st.markdown('<div class="section-title">Daily Simulation</div>', unsafe_allow_html=True)

    # NOTE TO SELF:
    # Matplotlib chart with two y-axes:
    # ax1 = all-in price
    # ax2 = grid usage
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Dark chart styling
    fig.patch.set_facecolor("#111111")
    ax1.set_facecolor("#111111")

    # Price line
    ax1.plot(
        df["Hour"],
        df["All-in price (c/kWh)"],
        marker="o",
        linewidth=2,
        label="All-in price (c/kWh)"
    )

    ax1.set_xlabel("Hour of day")
    ax1.set_ylabel("All-in price (c/kWh)")
    ax1.set_xticks(df["Hour"])
    ax1.grid(True, alpha=0.25)

    # Highlight selected hour
    ax1.axvline(hour, linestyle=":", linewidth=2, label="Selected hour")

    # Second axis for grid usage
    ax2 = ax1.twinx()

    ax2.plot(
        df["Hour"],
        df["Grid usage (kW)"],
        marker="s",
        linestyle="--",
        linewidth=2,
        label="Grid usage (kW)"
    )

    ax2.set_ylabel("Grid usage (kW)")

    # Text colors for dark background
    ax1.tick_params(colors="white")
    ax2.tick_params(colors="white")
    ax1.xaxis.label.set_color("white")
    ax1.yaxis.label.set_color("white")
    ax2.yaxis.label.set_color("white")
    ax1.title.set_color("white")

    plt.title("Daily Simulation: Price vs Grid Usage", color="white")

    # Combined legend
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    legend = ax1.legend(
        lines_1 + lines_2,
        labels_1 + labels_2,
        loc="upper left"
    )

    for text in legend.get_texts():
        text.set_color("white")

    legend.get_frame().set_facecolor("#222222")
    legend.get_frame().set_edgecolor("#555555")

    st.pyplot(fig)


# ---------- CONTROL CARD ----------
with control_col:
    st.markdown('<div class="section-title">Controls</div>', unsafe_allow_html=True)

    selected_hour = st.slider(
        "Select hour of day",
        0,
        23,
        hour,
        key="hour_slider"
    )

    st.write(f"Selected hour: {selected_hour}:00")

    st.success(
        f"💡 Best hour to charge today: {int(best_hour)}:00 "
        f"({best_cost:.2f} € / {round(best_cost * 100)} cents)"
    )

    st.write(
        "Note: best hour is currently based on the same solar value repeated for the whole day."
    )