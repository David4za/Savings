# Wealth Planner

A small Streamlit app I built to explore personal savings scenarios — no login, no database, just numbers and charts.

Use it to answer three practical questions:

1. **If I save like this, where could I end up?**
2. **How much do I need to save each month to hit a target?**
3. **If I retire with this pot, how long does it last?**

It is a planning tool, not financial advice. Returns are smoothed averages, not real market swings.

---

## Run it locally

**Requirements:** Python 3.11+

```bash
# with uv (recommended)
uv sync
uv run streamlit run main.py

# or with pip
pip install -r requirements.txt
streamlit run main.py
```

The app opens in your browser. Use the sidebar to switch pages.

---

## What each page does

### Fixed Income Plan *(default)*

Forward-looking savings projection.

- Set **monthly saving**, **expected return**, **time horizon**, and **inflation**
- Optionally add **one-off lump sums** (e.g. a bonus or inheritance in year 10)
- Click **Calculate** to see summary cards and a chart of growth over time

You get total savings, what you put in, interest earned, and an inflation-adjusted figure so you can compare future money to today's purchasing power.

### Reverse engineering a plan

Works backwards from a goal.

- Enter a **target amount**, **return**, and **years**
- Click **Analyse** to see the **fixed monthly saving** needed to get there

Useful when you know the destination but not the monthly habit.

### Withdraw Plan

Drawdown simulation for retirement or decumulation.

- Set **starting savings**, **monthly withdrawal**, **return**, and **inflation**
- Click **Calculate** to see how long the money lasts and a balance-over-time chart

The chart shows both the nominal balance and an inflation-adjusted view.

### How the math works *(Reference)*

Plain-language walkthrough of the formulas and assumptions behind the calculators. Good if you want to sanity-check the logic without reading Python.

---

## How it is put together

```
main.py                 # App entry + sidebar navigation
pages/
  input_plan.py         # Fixed Income Plan UI
  reverse_plan.py       # Reverse calculator UI
  withdraw.py           # Withdraw Plan UI
  math_overview.py      # Formula reference page
  calculations/         # Business logic (kept out of the UI)
  charts/               # Plotly chart builders
  components/           # Reusable UI (summary cards, input styling)
```

**Stack:** Streamlit, Pandas, Plotly, Millify

Calculations live in `pages/calculations/` so the pages mostly handle inputs and display. That keeps the math testable and separate from the UI.

---

## Assumptions worth knowing

- Returns compound **monthly** from an effective annual rate
- Monthly savings are deposited at **month-end**
- Markets are modelled as steady — no volatility, fees, or taxes
- Inflation is a simple average rate, not a year-by-year forecast

For the full detail, open **How the math works** in the app.

---

## Who this is for

- **Anyone** curious about long-term saving or withdrawal timelines
- **Business / product folks** who want a quick what-if model without a spreadsheet
- **Junior devs** looking for a small Streamlit example with separated calculation logic

If something looks off or you want a new scenario type, open an issue or tweak the inputs and compare with the math page.
