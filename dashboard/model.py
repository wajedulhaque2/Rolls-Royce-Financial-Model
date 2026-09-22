"""DCF sensitivity using workbook cash flows and discount conventions."""

from __future__ import annotations


def value_per_share(snapshot: dict, wacc: float, growth: float) -> tuple[float, float]:
    if wacc <= growth:
        raise ValueError("WACC must exceed terminal growth")
    pv_flows = sum(flow / (1 + wacc) ** period for flow, period in
                   zip(snapshot["cash_flows_m"], snapshot["discount_periods"]))
    terminal = snapshot["forecast"]["UFCF"][-1] * (1 + growth) / (wacc - growth)
    pv_terminal = terminal / (1 + wacc) ** snapshot["terminal_period"]
    enterprise = pv_flows + pv_terminal
    return (enterprise + snapshot["net_cash_m"]) / snapshot["shares_m"], pv_terminal / enterprise
