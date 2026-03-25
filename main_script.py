# ============================================================
# Retail Demand Forecasting — Time Series Analysis
# Author: Jagdish Chhabra | github.com/jagdish-chhabra
# Stack: Python, Pandas, Prophet, Statsmodels, Plotly
# Business Goal: Forecast next 12 weeks of product demand
# ============================================================

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os
import warnings
warnings.filterwarnings("ignore")

os.makedirs("screenshots", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Optional: Prophet (install separately if needed)
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("ℹ️  Prophet not installed. Run: pip install prophet")

print("=" * 60)
print("  RETAIL DEMAND FORECASTING PIPELINE")
print("  Author: Jagdish Chhabra")
print("=" * 60)

# ── 1. GENERATE REALISTIC SALES DATA ─────────────────────────
np.random.seed(42)
dates = pd.date_range("2021-01-04", periods=156, freq="W")  # 3 years weekly

# Realistic retail time series: trend + seasonality + noise
trend    = np.linspace(800, 1400, 156)
seasonal = 200 * np.sin(2 * np.pi * np.arange(156) / 52)   # yearly cycle
holiday  = np.zeros(156)
# Spike at Christmas weeks (weeks 51-52 each year)
for yr in range(3):
    holiday[52*yr + 50] = 400
    holiday[52*yr + 51] = 600
noise    = np.random.normal(0, 60, 156)

sales = (trend + seasonal + holiday + noise).clip(min=100).astype(int)

df = pd.DataFrame({"date": dates, "sales": sales})
df.set_index("date", inplace=True)

print(f"\n📊 Dataset: {len(df)} weekly observations (Jan 2021 – Dec 2023)")
print(f"   Mean Sales  : {df['sales'].mean():.0f} units/week")
print(f"   Min/Max     : {df['sales'].min()} / {df['sales'].max()} units")

# ── 2. STATIONARITY TEST ─────────────────────────────────────
adf_stat, p_val, *_ = adfuller(df["sales"])
print(f"\n📈 ADF Stationarity Test")
print(f"   ADF Statistic : {adf_stat:.4f}")
print(f"   p-value       : {p_val:.4f}")
print(f"   Series is {'stationary ✅' if p_val < 0.05 else 'non-stationary ⚠️ (differencing needed)'}")

# ── 3. TRAIN / TEST SPLIT ────────────────────────────────────
FORECAST_WEEKS = 12
train = df.iloc[:-FORECAST_WEEKS]
test  = df.iloc[-FORECAST_WEEKS:]
print(f"\n🔀 Train: {len(train)} weeks | Test: {FORECAST_WEEKS} weeks")

# ── 4A. ARIMA MODEL ──────────────────────────────────────────
print("\n🔄 Fitting ARIMA(2,1,2)...")
arima_model  = ARIMA(train["sales"], order=(2, 1, 2)).fit()
arima_fc     = arima_model.forecast(steps=FORECAST_WEEKS)
arima_conf   = arima_model.get_forecast(steps=FORECAST_WEEKS).conf_int().reset_index(drop=True)
arima_mae    = mean_absolute_error(test["sales"], arima_fc)
arima_rmse   = np.sqrt(mean_squared_error(test["sales"], arima_fc))
print(f"   ARIMA MAE  : {arima_mae:.1f} units")
print(f"   ARIMA RMSE : {arima_rmse:.1f} units")

# ── 4B. PROPHET MODEL ────────────────────────────────────────
prophet_fc, prophet_mae, prophet_rmse = None, None, None
if PROPHET_AVAILABLE:
    print("\n🔄 Fitting Prophet...")
    prophet_df = train.reset_index().rename(columns={"date": "ds", "sales": "y"})
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False,
                changepoint_prior_scale=0.3)
    m.fit(prophet_df)
    future      = m.make_future_dataframe(periods=FORECAST_WEEKS, freq="W")
    forecast_df = m.predict(future)
    prophet_fc  = forecast_df.tail(FORECAST_WEEKS)["yhat"].values
    prophet_mae = mean_absolute_error(test["sales"], prophet_fc)
    prophet_rmse= np.sqrt(mean_squared_error(test["sales"], prophet_fc))
    print(f"   Prophet MAE  : {prophet_mae:.1f} units")
    print(f"   Prophet RMSE : {prophet_rmse:.1f} units")

# ── 5. MODEL COMPARISON TABLE ────────────────────────────────
print("\n" + "─" * 40)
print(f"  {'Model':<20} {'MAE':>8} {'RMSE':>8}")
print("─" * 40)
print(f"  {'ARIMA(2,1,2)':<20} {arima_mae:>8.1f} {arima_rmse:>8.1f}")
if PROPHET_AVAILABLE:
    print(f"  {'Prophet':<20} {prophet_mae:>8.1f} {prophet_rmse:>8.1f}")
    best_model = "Prophet" if prophet_mae < arima_mae else "ARIMA"
    print(f"\n  ✅ Best: {best_model}")
print("─" * 40)

# ── 6. VISUALIZATIONS ────────────────────────────────────────
cols    = 2 if PROPHET_AVAILABLE else 1
fig     = make_subplots(
    rows=2, cols=cols,
    subplot_titles=(
        "Historical Sales + ARIMA Forecast",
        "Prophet Forecast" if PROPHET_AVAILABLE else "",
        "ARIMA Forecast vs Actual (Test Period)",
        "Forecast Accuracy by Model" if PROPHET_AVAILABLE else "",
    ),
    vertical_spacing=0.15
)

# Plot 1 — Full series + ARIMA forecast
fig.add_trace(go.Scatter(x=df.index, y=df["sales"],
                          name="Actual Sales", line=dict(color="#4361ee", width=1.5)),
              row=1, col=1)
fc_dates = pd.date_range(test.index[-1] + pd.Timedelta(weeks=1),
                          periods=FORECAST_WEEKS, freq="W")
fig.add_trace(go.Scatter(x=test.index, y=arima_fc.values,
                          name="ARIMA Forecast", line=dict(color="#d62828", dash="dash", width=2)),
              row=1, col=1)
fig.add_trace(go.Scatter(
    x=list(test.index) + list(reversed(test.index)),
    y=list(arima_conf.iloc[:, 1]) + list(reversed(arima_conf.iloc[:, 0])),
    fill="toself", fillcolor="rgba(214,40,40,0.1)", line=dict(color="rgba(255,255,255,0)"),
    name="95% CI", showlegend=True), row=1, col=1)

# Plot 2 — Prophet (if available)
if PROPHET_AVAILABLE:
    fig.add_trace(go.Scatter(x=df.index, y=df["sales"],
                              name="Actual (Prophet)", line=dict(color="#4361ee", width=1.5)),
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=test.index, y=prophet_fc,
                              name="Prophet Forecast",
                              line=dict(color="#3f8600", dash="dash", width=2)),
                  row=1, col=2)

# Plot 3 — Test period close-up
fig.add_trace(go.Scatter(x=test.index, y=test["sales"],
                          name="Actual (Test)", line=dict(color="#4361ee", width=2)),
              row=2, col=1)
fig.add_trace(go.Scatter(x=test.index, y=arima_fc.values,
                          name="ARIMA", line=dict(color="#d62828", dash="dot", width=2)),
              row=2, col=1)
if PROPHET_AVAILABLE:
    fig.add_trace(go.Scatter(x=test.index, y=prophet_fc,
                              name="Prophet", line=dict(color="#3f8600", dash="dot", width=2)),
                  row=2, col=1)

# Plot 4 — Bar comparison
if PROPHET_AVAILABLE:
    fig.add_trace(go.Bar(
        x=["ARIMA", "Prophet"],
        y=[arima_mae, prophet_mae],
        marker_color=["#d62828", "#3f8600"],
        text=[f"{arima_mae:.1f}", f"{prophet_mae:.1f}"],
        textposition="outside",
        name="MAE Comparison"
    ), row=2, col=2)

fig.update_layout(
    title=dict(text="Retail Demand Forecasting Dashboard<br><sup>Jagdish Chhabra — Analytics Portfolio</sup>",
               font=dict(size=16)),
    height=700, template="plotly_white",
    legend=dict(orientation="h", y=-0.1)
)
fig.write_html("screenshots/demand_forecast.html")
fig.write_html("output/demand_forecast.html")

# Save static screenshot hint
print("\n💾 Saved: screenshots/demand_forecast.html")
print("💾 Saved: output/demand_forecast.html")
fig.show()

# ── 7. BUSINESS SUMMARY ──────────────────────────────────────
best_fc  = arima_fc.values
avg_fc   = best_fc.mean()
peak_wk  = test.index[np.argmax(best_fc)]
low_wk   = test.index[np.argmin(best_fc)]

print("\n" + "=" * 60)
print("  BUSINESS INSIGHTS — NEXT 12 WEEKS FORECAST")
print("=" * 60)
print(f"  📦 Avg forecasted demand : {avg_fc:.0f} units/week")
print(f"  📈 Peak demand week      : {peak_wk.strftime('%b %d, %Y')} ({max(best_fc):.0f} units)")
print(f"  📉 Low demand week       : {low_wk.strftime('%b %d, %Y')} ({min(best_fc):.0f} units)")
print(f"  💡 Inventory recommendation:")
print(f"     Stock at least {max(best_fc)*1.15:.0f} units before peak week")
print(f"     to maintain a 15% safety buffer.")
print("=" * 60)

# ── HOW TO RUN ───────────────────────────────────────────────
# pip install pandas numpy plotly statsmodels scikit-learn
# pip install prophet   (optional, requires pystan)
# python demand_forecasting.py