# Portfolio & Financial Risk Analytics Engine

Sistema integral de inteligencia financiera diseñado para automatizar la extracción de datos, modelado cuantitativo de riesgo y reportería ejecutiva para portafolios de inversión.

## 🏛️ Arquitectura del Pipeline

```mermaid
flowchart LR
    A[Interactive Brokers Flex API] -->|Extracción Diaria| B(GitHub Actions CI/CD)
    C[Yahoo Finance / Stooq API] -->|Benchmark SPY| B
    B -->|Ingesta Automatizada| D[Power Query M]
    D -->|Modelo Estrella| E[Modelo Semántico DAX]
    E -->|Analítica de Riesgo| F[Power BI Dashboard]
