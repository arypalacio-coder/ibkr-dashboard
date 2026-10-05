# Portfolio & Financial Risk Analytics Engine

End-to-end financial intelligence system designed to automate data extraction, quantitative risk modeling, and executive reporting for investment portfolios.

---

## Arquitectura del Pipeline

```mermaid
flowchart LR
    A[Interactive Brokers Flex API] -->|Daily Extraction| B(GitHub Actions CI/CD)
    C[Yahoo Finance API] -->|Benchmark SPY| B
    B -->|Automated Ingestion| D[Data Lake / CSV Datasets]
    D -->|Star Schema| E[Semantic Model DAX]
    E -->|Risk Analytics| F[Power BI Executive Dashboard]
Modelo Relacional (Esquema Estrella)
Tablas de Hechos (Fact Tables):

Fact_PortfolioDaily: Valor liquidativo diario (NAV), flujos de efectivo y saldo Mark-to-Market.

Fact_Trades: Registro atomico de ejecuciones, tamano de ordenes, PnL realizado y comisiones.

Fact_Dividends: Dividendos brutos, retenciones fiscales (Withholding Tax) y pagos netos.

Fact_Benchmark_SPY: Precios de cierre ajustados y retornos diarios del S&P 500.

Tablas de Dimensiones (Dim Tables):

Dim_Calendario: Eje temporal maestro continuo.

Dim_Asset: Clasificacion dinamica por clase de activo (Renta Variable, Renta Fija, Materias Primas, Liquidez).

Dim_CambioNAV: Jerarquia contable para la conciliacion de variacion patrimonial.

Metricas Cuantitativas de Riesgo
Annualized Sharpe Ratio: Rendimiento excedente ponderado por unidad de volatilidad total (Rf configurable).

Maximum Drawdown (MDD): Perdida maxima acumulada pico a valle a lo largo de la serie temporal.

Portfolio Beta: Sensibilidad sistematica del portafolio frente a los movimientos del benchmark (SPY).

Jensen Alpha: Generacion de retorno anormal ajustado por riesgo bajo el modelo CAPM.

Stack Tecnologico
Data Engineering & Automation: Python 3.11 (pandas, requests, yfinance), Interactive Brokers Flex Web Service API.

CI/CD Pipeline: GitHub Actions (extraccion programada Martes a Sabado post-cierre de mercado).

Modeling & Analytics: Power BI, DAX cuantitativo, Star Schema Dimensional Modeling.
