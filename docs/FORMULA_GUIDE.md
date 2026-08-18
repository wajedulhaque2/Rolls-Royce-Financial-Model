# Formula, Query & Model Guide

## 1. Power Query and Data Model

The workbook contains Power Query connections including:

```text
CH_Accounts_Document_Metadata
CH_Accounts_Filing_History
Dim_Concept
Dim_Period
Merge1
PQ_Balance_Sheet
PQ_Cash_Flow
PQ_Fact_Financials
PQ_Income_Statement
ThisWorkbookDataModel
```

The `Raw_Data` sheet contains cached query outputs used by the historical statements and Data Model.

## 2. Operating forecast

### Group revenue

The forecast model links directly to segment revenue built on `Operating_Drivers`:

```excel
=Operating_Drivers!L17
```

Later years flow through the segment forecasts and reconcile back to group revenue.

### Revenue growth

```excel
=C9/B9-1
```

The first forecast-year group revenue growth is approximately 18.1%, before moderating through FY2030E.

### Group operating profit

```excel
=Operating_Drivers!L32
```

### EBIT margin

```excel
=Group_Underlying_Operating_Profit / Group_Underlying_Revenue
```

In the workbook this links through the `Operating_Drivers` margin build.

### NOPAT and UFCF bridge

The forecast cash-flow section separates operating profit, tax, D&A/non-cash add-backs, capital expenditure and working-capital cash impact:

```text
EBIT
- Operating tax
= NOPAT
+ D&A / non-cash add-backs
- Capital expenditure
+ Working-capital cash impact
= Unlevered Free Cash Flow
```

## 3. WACC

### Cost of equity

```excel
=Risk_Free_Rate + Beta * Equity_Risk_Premium
```

Workbook formula:

```excel
=B8+B9*B10
```

### Pre-tax cost of debt

```excel
=(H1_Interest_Payable*2)/AVERAGE(Debt_Dec_2025,Debt_Jun_2026)
```

### After-tax cost of debt

```excel
=Pre_Tax_Cost_of_Debt*(1-Normalised_Tax_Rate)
```

### Capital weights

```excel
Equity Weight = Market Value of Equity / (Market Value of Equity + Debt)
Debt Weight   = Debt / (Market Value of Equity + Debt)
```

### WACC

```excel
=Equity_Weight*Cost_of_Equity + Debt_Weight*After_Tax_Cost_of_Debt
```

Cached WACC: **9.62%**.

## 4. DCF valuation

### FY2026 stub cash flow

```excel
=FY2026_Full_Year_UFCF - H1_2026_UFCF
```

### Discount factor

```excel
=1/(1+$B$26)^Discount_Period
```

### PV of UFCF

```excel
=DCF_Cash_Flow*Discount_Factor
```

### Terminal value

```excel
=FY2030_UFCF*(1+Terminal_Growth)/(WACC-Terminal_Growth)
```

Workbook formula:

```excel
=B52*(1+B53)/(B54-B53)
```

### PV of terminal value

```excel
=Terminal_Value/(1+WACC)^4.5
```

### Enterprise value

```excel
=SUM(PV_of_Forecast_UFCF)+PV_of_Terminal_Value
```

### Equity value

```excel
=Enterprise_Value+Net_Cash
```

### Implied value per share

```excel
=Equity_Value/Diluted_Shares
```

Cached DCF value: **£8.195/share**.

### Upside / downside

```excel
=Implied_Value_per_Share/Reference_Share_Price-1
```

Cached result: approximately **-43.3%**.

## 5. Comparable-company valuation

Peer enterprise value is calculated from market capitalisation plus net debt / (cash):

```excel
Market Cap = Share Price * Shares Outstanding
Enterprise Value = Market Cap + Net Debt
```

The workbook calculates peer multiples:

```excel
EV/Revenue = Enterprise Value / Revenue
EV/EBIT    = Enterprise Value / EBIT
```

It then uses peer medians:

```excel
=MEDIAN(I6:I10)   // EV/Revenue
=MEDIAN(J6:J10)   // EV/EBIT
```

Implied enterprise values are:

```excel
Peer Median Multiple * Rolls-Royce FY2025 Metric
```

Implied equity value adds net cash, then divides by diluted shares.

The workbook averages the EV/Revenue and EV/EBIT per-share outputs:

```excel
=AVERAGE(B35:C35)
```

Cached comps midpoint: **£9.273/share**.

## 6. Market-data formulas

The comparable-company sheet uses `STOCKHISTORY` for the 30 June 2026 reference date, for example:

```excel
=STOCKHISTORY("XLON:RR.",DATE(2026,6,30),DATE(2026,6,30),0,0,1)
```

The cached portfolio workbook preserves the returned market values so viewers do not need live connectivity simply to inspect the model.

## 7. Sensitivity and scenario analysis

The saved Bear/Base/Bull framework adjusts:

```text
Revenue growth
EBIT margin
WACC
Terminal growth
```

Base-case reconciliation links the scenario valuation back to the DCF per-share value. Cached outputs are:

```text
Bear: £6.57/share
Base: £8.20/share
Bull: £10.43/share
```

The sensitivity sheet also contains market-implied growth / margin analyses that solve for operating assumptions consistent with the reference share price.

## 8. Model checks

Representative integrity checks include:

### WACC weights

```excel
=DCF!B24+DCF!B25-1
```

### DCF enterprise-value reconciliation

```excel
=DCF!B60-(SUM(DCF!B48:F48)+DCF!B57)
```

### DCF equity-value reconciliation

```excel
=DCF!B62-(DCF!B60+DCF!B61)
```

### Per-share reconciliation

```excel
=DCF!B64-(DCF!B62/DCF!B63)
```

### WACC > terminal growth

```excel
=DCF!B26-DCF!B27
```

### Overall status

```excel
=IF(COUNTIF(C6:C18,"FAIL")=0,"PASS","FAIL")
```

The cached overall model status is **PASS**.