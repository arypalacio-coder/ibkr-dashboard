# Portfolio & Financial Risk Analytics Engine

Production-grade financial engineering pipeline and intelligence system automating data ingestion from Interactive Brokers, quantitative risk modeling, and executive reporting.

---

## Pipeline Architecture

`mermaid
flowchart LR
    A[Interactive Brokers Flex API] -->|Daily Extraction| B(GitHub Actions CI/CD)
    C[Yahoo Finance API] -->|Benchmark SPY| B
    B -->|Automated Ingestion| D[Data Lake / CSV Datasets]
    D -->|Star Schema| E[Semantic Model DAX]
    E -->|Risk Analytics| F[Power BI Executive Dashboard]
`

---

## Relational Model (Star Schema)

* **Fact Tables:**
  * Fact_PortfolioDaily: Daily Net Asset Value (NAV), cash flows, and Mark-to-Market valuation.
  * Fact_Trades: Atomic execution logs, trade sizing, realized PnL, and broker commissions.
  * Fact_Dividends: Gross dividend cashflows, withholding tax withholding, and net settlements.
  * Fact_Benchmark_SPY: S&P 500 adjusted close prices and daily benchmark returns.
* **Dimension Tables:**
  * Dim_Calendario: Continuous master calendar hierarchy.
  * Dim_Asset: Dynamic classification by asset class (Equities, Fixed Income, Commodities, Cash).
  * Dim_CambioNAV: Accounting hierarchy for equity variation reconciliation.

---

## Quantitative Risk Metrics

* **Annualized Sharpe Ratio:** Excess return per unit of total portfolio volatility (configurable Rf).
* **Maximum Drawdown (MDD):** Peak-to-trough maximum observed cumulative portfolio loss.
* **Portfolio Beta:** Systematic risk exposure relative to benchmark movements (SPY).
* **Jensen Alpha:** Risk-adjusted abnormal return generation modeled under CAPM.

---

## Technical Stack

* **Data Engineering & Automation:** Python 3.11 (pandas, requests, yfinance), Interactive Brokers Flex Web Service API.
* **CI/CD Pipeline:** GitHub Actions (scheduled automated runs Tuesday to Saturday post market close).
* **Modeling & Analytics:** Power BI, Quantitative DAX, Star Schema Dimensional Modeling.
