# Workbook Architecture

```text
Annual reports / company results / market data / Companies House
                         |
                         v
              Power Query / Raw_Data
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
 Historical_FS / Ratio_Analysis      Power Pivot Analysis
        |
        v
 Operating_Drivers
        |
        v
 Forecast_Model (FY2026E-FY2030E)
        |
        +----------------------+-------------------+
        |                      |                   |
        v                      v                   v
       DCF             Comparable_Companies    Sensitivity
        |                      |                   |
        +----------------------+-------------------+
                         |
                         v
                      Dashboard
                         |
                         v
                       Checks
```

## Worksheet roles

- `Historical_FS` - historical reported/underlying financials and segment data.
- `Ratio_Analysis` - historical growth, profitability and cash-flow ratios.
- `Operating_Drivers` - segment revenue/margin drivers and forecast support assumptions.
- `Forecast_Model` - integrated group forecast and UFCF bridge.
- `DCF` - WACC, terminal value and implied share value.
- `Comparable_Companies` - peer-market data, multiples and implied valuation.
- `Sensitivity` - valuation sensitivity, Bear/Base/Bull and market-implied analyses.
- `Power_Pivot_Analysis` - Data Model output.
- `Checks` - model integrity/reconciliation tests.
- `Sources` - source register and methodology.
- `Raw_Data` - cached Power Query/source outputs.
- `Dashboard` - reviewer-facing summary.

## Audit trail

The model supports tracing a dashboard valuation back through:

```text
Dashboard -> DCF / Comps -> Forecast -> Operating Drivers
-> Historical financials / source extracts -> Sources
```

This separation is important for financial-model review because hardcoded assumptions, inter-sheet links and calculation outputs are not mixed into one opaque worksheet.