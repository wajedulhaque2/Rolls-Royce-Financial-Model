# Data Sources

The workbook's `Sources` sheet documents the source set used for the historical model and valuation.

## Company reporting

- Rolls-Royce annual reports FY2016-FY2024
- Rolls-Royce FY2025 Full Year Results
- Rolls-Royce H1 2026 Results
- Rolls-Royce FY2025 Full-Year Results web page used by Power Query

## Regulatory / structured data

- Companies House filing-history API and document metadata
- Company number referenced in the workbook: **07524813**

## Market / valuation inputs

| Input | Workbook date / basis | Cached value / use |
|---|---|---|
| Rolls-Royce share price | 30 Jun 2026 | £14.45 reference price |
| UK 10-year government bond yield | 30 Jun 2026 | 4.83% risk-free rate |
| Equity risk premium | Valuation assumption | 4.17% |
| Comparable-company market data | FY2025 / 30 Jun 2026 | GE Aerospace, Safran, RTX, MTU Aero Engines, BAE Systems |

## Refresh note

Power Query and `STOCKHISTORY` can require internet access and Excel connectivity. The portfolio workbook is therefore provided with cached values so a reviewer can inspect the model without re-running external data requests.

Market-data and valuation inputs are date-specific and should not be described as current beyond the workbook's stated valuation date.