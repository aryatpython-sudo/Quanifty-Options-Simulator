# Quanifty Options Basket Simulator

A desktop application for building and simulating multi-leg options strategies on Indian indices (NIFTY, BANKNIFTY). The goal is to let traders construct a strategy visually and immediately see the theoretical payoff — before committing to a real position.

---

## Overview

Options strategies often involve multiple legs (buy call, sell put, etc.) and it can be hard to reason about the combined risk/reward without doing the math manually. This tool provides an options chain view, a basket builder, and a payoff graph — all in one place.

Built entirely in Python with a focus on keeping the interface clean and fast.

---

## Current State

**Options Chain**

Loads options data from a JSON file (structured like a real NSE options chain) and renders it in a scrollable table showing Call LTP, Strike Price, and Put LTP. Hovering over a row reveals inline Buy and Sell buttons for both the Call and Put side, so adding a leg to the basket is a single click.

**Basket**

Legs selected from the chain are stored in a shared basket list. Each entry captures the LTP, strike, position direction (BUY/SELL), and option type (CALL/PUT).

**Payoff Graph**

An embedded matplotlib chart with a dark theme matching the rest of the UI. Hovering over the chart shows live coordinates (price on X, P&L on Y) with a vertical crosshair. The chart area is ready — the payoff math is the next piece to wire in.

---

## Roadmap

- [ ] Calculate the combined payoff curve from the basket and plot it on the chart
- [ ] Derive and display key metrics: max profit, max loss, and breakeven point(s)
- [ ] Add a basket panel to the UI for reviewing and removing individual legs
- [ ] Replace the static JSON data source with a live API (NSE / broker feed)
- [ ] Add expiry date selection to the options chain view
- [ ] Compute and display option Greeks per leg

---

## Stack

| Layer | Library |
|---|---|
| GUI | `customtkinter`, `CTkTable` |
| Charting | `matplotlib` |
| Language | Python 3 |

---

## Getting Started

Install dependencies:

```bash
pip install customtkinter CTkTable matplotlib
```

Run the app:

```bash
python gui.py
```

The app expects `options_data.json` in the same directory. The JSON should follow the NSE options chain structure with `strike_price`, `CE.ltp`, and `PE.ltp` fields per row.

---

## Project Structure

```
.
├── gui.py              # Application entry point, layout, and graph setup
├── makeTableData.py    # Options chain parsing, table rendering, button logic
├── basketList.py       # Shared basket state
├── graphMath.py        # Payoff calculation (in progress)
└── options_data.json   # Sample options chain data
```
