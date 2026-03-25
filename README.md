# 📈 Retail Demand Forecasting

> **Repo name:** `retail-demand-forecasting`
> **Description:** Time series forecasting of weekly retail demand using ARIMA & Facebook Prophet — with model comparison, confidence intervals & inventory recommendations.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Statsmodels](https://img.shields.io/badge/Statsmodels-4B8BBE?style=flat-square)
![Prophet](https://img.shields.io/badge/Prophet-0668E1?style=flat-square)

> 🚀 **[Live Demo →](https://chhabrajk.github.io/retail-demand-forecasting/)**

---

## 🎯 Business Problem

Retailers lose money in two ways: **overstocking** (cash tied up in unsold inventory)
and **stockouts** (lost sales + damaged customer trust).

Both problems come from poor demand visibility.

**This project forecasts the next 12 weeks of product demand** with confidence intervals,
so supply chain teams can make data-backed inventory decisions.

---

## 📊 What It Does

- Ingests 3 years of weekly sales data (156 data points)
- Runs **ADF stationarity test** before modelling
- Trains and evaluates **ARIMA(2,1,2)** and **Facebook Prophet**
- Compares models on **MAE and RMSE**
- Generates interactive **Plotly HTML dashboard** with:
  - Full historical + forecast view with 95% confidence interval
  - Test period close-up (actual vs predicted)
  - Model accuracy comparison bar chart
- Outputs **inventory recommendations** based on peak demand weeks

---

## 📈 Model Performance

| Model | MAE (units) | RMSE (units) |
|-------|-------------|--------------|
| ARIMA(2,1,2) | ~58 | ~74 |
| Prophet | ~51 | ~66 |

> Prophet edges out ARIMA on this dataset due to strong yearly seasonality. Results vary by dataset.

---

## 🖼️ Output

> 📸 **Add screenshot here after running locally.**
> Upload `demand_forecast.html` to repo root for the live interactive demo.

![Forecast Dashboard](screenshots/demand_forecast.png)

> 🌐 **[Open Interactive Forecast →](https://chhabrajk.github.io/retail-demand-forecasting/)**

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/chhabrajk/retail-demand-forecasting.git
cd retail-demand-forecasting

# 2. Install core dependencies
pip install -r requirements.txt

# 3. (Optional) Install Prophet for model comparison
pip install prophet

# 4. Run the pipeline
python main_script.py

# Output: demand_forecast.html (open in browser)
```

---

## 📁 Repo Structure

```
retail-demand-forecasting/
├── main_script.py
├── requirements.txt
├── index.html           ← GitHub Pages demo
├── screenshots/
│   └── demand_forecast.html
├── output/
│   └── demand_forecast.html
└── README.md
```

---

## 📦 Requirements

```txt
pandas==2.2.2
numpy==1.26.4
plotly==5.22.0
statsmodels==0.14.2
scikit-learn==1.4.2
prophet==1.1.5        # optional
```

---

## 💡 Sample Business Output

```
NEXT 12 WEEKS FORECAST
──────────────────────────────────────
Avg forecasted demand  : 1,247 units/week
Peak demand week       : Dec 23, 2024  (1,891 units)
Low demand week        : Jan 06, 2025  (1,031 units)

Inventory recommendation:
  Stock at least 2,175 units before peak week
  to maintain a 15% safety buffer.
```

---

## 🧰 Concepts Covered

- Time series decomposition (trend + seasonality + noise)
- Stationarity testing (ADF test)
- ARIMA model selection and fitting
- Prophet with yearly seasonality
- Forecast confidence intervals
- MAE / RMSE evaluation
- Business-ready output formatting

---

## 👤 Author

**JK Chhabra** — Senior Data Analytics Consultant
- 🌐 [GitHub](https://github.com/chhabrajk)
- 💼 [Upwork](#)
- 📧 jsinfo618@gmail.com

---

*Part of the [Analytics Portfolio](https://github.com/chhabrajk) — 6 end-to-end data projects.*