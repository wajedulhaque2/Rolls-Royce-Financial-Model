"""Source-backed dashboard for the cached Rolls-Royce Excel valuation model."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from model import value_per_share


ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Rolls-Royce | model review", page_icon="📈", layout="wide")
st.sidebar.title("Rolls-Royce model")
dark = st.sidebar.toggle("Dark mode", value=False)
BG, SURFACE, TEXT, MUTED, GRID, BORDER, TEAL, GOLD, BLUE = (
    ("#101C2A", "#1D2C3C", "#F6F8FB", "#B5C7D5", "#34495A", "#3A5062", "#42C0BD", "#FFC45C", "#86AFFF")
    if dark else
    ("#F5F8FA", "#FFFFFF", "#173348", "#556B7B", "#E2EAEE", "#DCE5EA", "#168A84", "#C98526", "#426D9C")
)
st.markdown(f"""
<style>
.stApp {{background:{BG};color:{TEXT};}}
[data-testid="stHeader"] {{background:{BG};}}
[data-testid="stSidebar"] {{background:{SURFACE};border-right:1px solid {BORDER};color:{TEXT};}}
.stApp h1,.stApp h2,.stApp h3,.stApp p,.stApp label,[data-testid="stSidebar"] h1,[data-testid="stSidebar"] label {{color:{TEXT};}}
.stApp [data-testid="stCaptionContainer"] p,[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{color:{MUTED};}}
[data-testid="stMetric"],[data-testid="stPlotlyChart"],[data-testid="stDataFrame"] {{background:{SURFACE};border:1px solid {BORDER};border-radius:9px;}}
[data-testid="stMetric"] {{padding:.85rem 1rem;min-height:115px;}}
[data-testid="stMetric"] label,[data-testid="stMetricValue"] {{color:{TEXT};}}
[data-testid="stPlotlyChart"],[data-testid="stDataFrame"] {{padding:.3rem;}}
.scope {{background:{'#263E49' if dark else '#E7F2F1'};border-left:4px solid {TEAL};padding:.75rem 1rem;margin:.4rem 0 1rem;color:{TEXT};}}
[data-baseweb="select"] > div,[data-baseweb="input"] > div {{background:{SURFACE};color:{TEXT};border-color:{BORDER};}}
[data-baseweb="select"] *,[data-baseweb="input"] input,[data-baseweb="popover"] li {{color:{TEXT};}}
[data-baseweb="popover"],[data-baseweb="popover"] li {{background:{SURFACE};}}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load() -> dict:
    return json.loads((ROOT / "data" / "snapshot.json").read_text(encoding="utf-8"))


def plot(fig: go.Figure, height: int = 420, bottom: int = 55) -> None:
    fig.update_layout(template="plotly_dark" if dark else "plotly_white", height=height,
                      paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
                      font={"family": "Arial", "color": TEXT, "size": 12},
                      title={"x": .025, "xanchor": "left", "font": {"size": 18}},
                      margin={"l": 55, "r": 38, "t": 65, "b": bottom},
                      hoverlabel={"font": {"family": "Arial"}})
    fig.update_xaxes(gridcolor=GRID, zeroline=False, automargin=True)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, automargin=True)
    st.plotly_chart(fig, width="stretch", theme=None, config={"displayModeBar": False})


data = load()
st.sidebar.caption("Cached Excel valuation · historic reference")
view = st.sidebar.radio("View", ["Valuation overview", "Operating forecast", "DCF sensitivity", "Sources & checks"])
st.sidebar.divider()
st.sidebar.caption(f"Reference share price dated {data['reference_date']}")

st.title({"Valuation overview": "Valuation overview", "Operating forecast": "Operating forecast",
          "DCF sensitivity": "DCF sensitivity", "Sources & checks": "Sources and model checks"}[view])
st.caption("Rolls-Royce Holdings plc · cached workbook values in GBP · not a live market feed")
st.markdown(f'<div class="scope">Reference price: 30 Jun 2026 · Model incorporates H1 2026 results published 30 Jul 2026</div>',
            unsafe_allow_html=True)

if view == "Valuation overview":
    cards = st.columns(4)
    cards[0].metric("DCF value / share", f"£{data['cached_dcf']:.2f}")
    cards[1].metric("Comps midpoint / share", f"£{data['cached_comps']:.2f}")
    cards[2].metric("Reference share price", f"£{data['reference_price']:.2f}")
    cards[3].metric("Terminal value share of EV", f"{data['terminal_ev_share']:.1%}")
    st.caption("The price is the workbook's dated reference, not today's quote. Its 30 June date precedes publication of the H1 results incorporated into the model.")

    values = pd.DataFrame({"Basis": ["Bear scenario", "DCF base", "Bull scenario", "Comps midpoint", "Reference price"],
                           "£ per share": [data["scenario_values"]["Bear"], data["cached_dcf"],
                                           data["scenario_values"]["Bull"], data["cached_comps"], data["reference_price"]]})
    values["Colour"] = [BLUE, TEAL, GOLD, BLUE, MUTED]
    values = values.sort_values("£ per share")
    fig = px.bar(values, x="£ per share", y="Basis", orientation="h", text="£ per share")
    fig.update_traces(marker_color=values["Colour"].tolist(), texttemplate="£%{x:.2f}",
                      textposition="outside", cliponaxis=False)
    fig.update_layout(title="Cached valuation approaches and dated reference price", showlegend=False)
    fig.update_yaxes(title=None, showgrid=False)
    fig.update_xaxes(range=[0, data["reference_price"] * 1.14])
    plot(fig, 440)

    years = data["years"][1:]
    flow = pd.DataFrame({"Year": years, "UFCF (£m)": data["forecast"]["UFCF"][1:]})
    fig = px.line(flow, x="Year", y="UFCF (£m)", markers=True, text="UFCF (£m)")
    fig.update_traces(line={"color": TEAL, "width": 3}, marker={"size": 9}, texttemplate="£%{y:,.0f}m",
                      textposition="top center", cliponaxis=False)
    fig.update_layout(title="Forecast unlevered free cash flow")
    fig.update_xaxes(type="category", title=None)
    plot(fig, 390)

elif view == "Operating forecast":
    frame = pd.DataFrame({"Year": data["years"], "Revenue (£m)": data["forecast"]["Revenue"],
                          "Operating profit (£m)": data["forecast"]["Operating profit"],
                          "EBIT margin": data["forecast"]["EBIT margin"]})
    long = frame.melt(id_vars="Year", value_vars=["Revenue (£m)", "Operating profit (£m)"],
                      var_name="Measure", value_name="£m")
    fig = px.bar(long, x="Year", y="£m", color="Measure", barmode="group",
                 color_discrete_map={"Revenue (£m)": BLUE, "Operating profit (£m)": TEAL})
    fig.update_layout(title="Revenue and underlying operating profit", legend_title=None,
                      legend={"orientation": "h", "y": -0.26, "x": 0})
    fig.update_xaxes(title=None, type="category")
    plot(fig, 420, 95)
    fig = px.line(frame, x="Year", y="EBIT margin", markers=True, text="EBIT margin")
    fig.update_traces(line={"color": GOLD, "width": 3}, marker={"size": 9},
                      texttemplate="%{y:.1%}", textposition="top center", cliponaxis=False)
    fig.update_layout(title="Underlying EBIT margin")
    fig.update_yaxes(tickformat=".0%", range=[0, .27])
    fig.update_xaxes(title=None, type="category")
    plot(fig, 360)
    st.dataframe(frame.style.format({"Revenue (£m)": "£{:,.0f}", "Operating profit (£m)": "£{:,.0f}",
                                   "EBIT margin": "{:.1%}"}), width="stretch", hide_index=True)
    st.caption("FY2025A is historical; FY2026E–FY2030E are workbook forecasts. Money figures are £m.")

elif view == "DCF sensitivity":
    inputs = st.columns(2)
    wacc_pct = inputs[0].number_input("WACC (%)", min_value=5.0, max_value=20.0,
                                     value=float(data["base_wacc"] * 100), step=.1, format="%.2f")
    growth_pct = inputs[1].number_input("Terminal growth (%)", min_value=0.0, max_value=6.0,
                                       value=float(data["base_growth"] * 100), step=.1, format="%.2f")
    if wacc_pct <= growth_pct:
        st.error("WACC must exceed terminal growth for the terminal-value calculation.")
    else:
        value, terminal_share = value_per_share(data, wacc_pct / 100, growth_pct / 100)
        cards = st.columns(3)
        cards[0].metric("Selected DCF value / share", f"£{value:.2f}")
        cards[1].metric("Versus dated reference", f"{value / data['reference_price'] - 1:+.1%}")
        cards[2].metric("Terminal value share of EV", f"{terminal_share:.1%}")
    rows = []
    for growth in (1.5, 2, 2.5, 3, 3.5):
        for wacc in (8, 8.5, 9, 9.5, 10, 10.5, 11):
            v, _ = value_per_share(data, wacc / 100, growth / 100)
            rows.append({"WACC": f"{wacc:.1f}%", "Growth": f"{growth:.1f}%", "Value": v})
    matrix = pd.DataFrame(rows).pivot(index="Growth", columns="WACC", values="Value")
    fig = go.Figure(go.Heatmap(z=matrix.values, x=matrix.columns, y=matrix.index,
                               colorscale=[[0, "#315B83"], [.5, "#E9F1EE"], [1, "#B77B2B"]],
                               text=matrix.values, texttemplate="£%{text:.2f}",
                               hovertemplate="WACC %{x}<br>Growth %{y}<br>£%{z:.2f}/share<extra></extra>"))
    fig.update_layout(title="DCF value / share across WACC and terminal growth", xaxis_title="WACC", yaxis_title="Terminal growth")
    plot(fig, 460)
    st.caption("The heatmap shows a fixed comparison grid. The input controls above calculate their exact selected values from the same cash flows; the workbook base WACC is 9.6194%.")

else:
    st.markdown("""
### Source and timing
The dashboard extracts cached values from `workbook/Rolls_Royce_Financial_Model_Portfolio.xlsx`. The workbook documents FY2025 results, H1 2026 results, a **30 June 2026** share-price reference and forecast assumptions through FY2030E. [Rolls-Royce published its H1 2026 results on 30 July 2026](https://www.rolls-royce.com/media/press-releases/2026/30-07-2026-rr-holdings-plc-2026-half-year-results.aspx), after the share-price reference date. Treat this as a review of the saved workbook assumptions, not a contemporaneous 30 June valuation or a live price comparison.

### DCF calculation
The selected WACC and terminal-growth controls rediscount the five saved DCF cash flows. FY2026 is a post-H1 stub; the terminal value applies FY2030 UFCF, a 4.5-year discount period, £2,136m net cash and 8,368m diluted shares. The valuation is particularly sensitive to terminal assumptions. Peer figures and Bear/Base/Bull outputs remain the workbook's cached values.
""")
    st.subheader("Model integrity checks")
    st.dataframe(pd.DataFrame(data["checks"]).rename(columns={"name": "Workbook check", "status": "Saved status"}),
                 width="stretch", hide_index=True)
    st.caption("All 13 cached workbook checks read PASS. This reproduces their saved status; it does not refresh external data or independently audit the original financial statements.")
