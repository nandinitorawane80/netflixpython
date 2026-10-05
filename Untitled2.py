#!/usr/bin/env python
# coding: utf-8

import base64
import mimetypes
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "netflix.csv"
PLAN_ORDER = ["Basic", "Standard", "Premium"]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
CHART_COLORS = {
    "red": "#E50914",
    "dark_red": "#B20710",
    "deep_red": "#67070C",
    "ink": "#202020",
    "muted": "#666666",
    "grid": "#E4E4E4",
}


def find_image(*stems: str) -> Path | None:
    wanted_stems = {stem.casefold() for stem in stems}
    for path in APP_DIR.iterdir():
        if path.is_file() and path.stem.casefold() in wanted_stems and path.suffix.lower() in IMAGE_EXTENSIONS:
            return path
    return None


def image_data_uri(path: Path | None) -> str | None:
    if path is None:
        return None
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded_image = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded_image}"


LOGO_URI = image_data_uri(find_image("image"))
BACKGROUND_URI = image_data_uri(find_image("bg image", "bg_image", "bg-image", "background"))

st.set_page_config(
    page_title="Netflix Audience Dashboard",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background: #ffffff;
            color: #202020;
        }
        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e4e4e4;
        }
        @media (min-width: 768px) {
            [data-testid="stSidebar"] {
                width: 280px !important;
                min-width: 280px !important;
                max-width: 280px !important;
            }
        }
        [data-testid="stSidebar"] * {
            color: #202020;
        }
        header[data-testid="stHeader"] {
            background: #ffffff;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #fff5f5;
            border: 1px solid #e50914;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] input {
            color: #202020 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="tag"] {
            background: #e50914;
        }
        [data-testid="stSidebar"] [data-baseweb="tag"] * {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] [data-baseweb="input"] {
            background: #fff5f5;
            border-color: #e50914;
        }
        [data-testid="stSidebar"] [data-baseweb="input"] input {
            color: #202020 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="input"] svg {
            fill: #e50914;
        }
        [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[role="group"] {
            background: #fff5f5 !important;
            border: 1px solid #e50914 !important;
        }
        [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] {
            background: #e50914 !important;
            border-color: #e50914 !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] * {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] [data-testid="stDateInputField"] {
            background: #fff5f5 !important;
            border: 1px solid #e50914 !important;
        }
        [data-testid="stSidebar"] [data-testid="stDateInputField"] [role="spinbutton"],
        [data-testid="stSidebar"] [data-testid="stDateInputField"] [data-type="literal"] {
            color: #202020 !important;
        }
        .block-container {
            max-width: 1440px;
            padding: 2rem 2rem 3rem;
        }
        h1, h2, h3 {
            font-family: Georgia, "Times New Roman", serif;
            letter-spacing: 0;
            color: #202020;
        }
        .hero-banner {
            min-height: 230px;
            display: flex;
            align-items: center;
            padding: 2rem 3rem;
            margin: 0 0 1.5rem;
            border-left: 5px solid #e50914;
            background-color: #161616;
            background-position: center 38%;
            background-size: cover;
            position: relative;
            overflow: hidden;
        }
        .hero-content {
            position: relative;
            z-index: 1;
        }
        .hero-logo {
            display: block;
            width: min(260px, 65vw);
            max-height: 100px;
            object-fit: contain;
            object-position: left center;
            margin-bottom: 0.75rem;
        }
        .hero-wordmark {
            display: block;
            color: #e50914;
            font-family: Arial, sans-serif;
            font-size: 3.25rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 0.75rem;
        }
        .hero-kicker {
            color: #f5f5f1;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .hero-caption {
            color: #e0e0e0;
            font-size: 1rem;
            margin: 0.55rem 0 0;
        }
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e4e4e4;
            border-top: 3px solid #e50914;
            padding: 0.8rem 0.65rem;
            border-radius: 4px;
        }
        [data-testid="stMetricLabel"] {
            color: #666666;
            font-size: 0.85rem;
        }
        [data-testid="stMetricValue"] {
            color: #202020;
            font-size: 1.2rem;
        }
        [data-testid="stDataFrame"] {
            border: 1px solid #e4e4e4;
        }
        hr {
            border-color: #e4e4e4;
        }
        @media (max-width: 640px) {
            .hero-banner {
                min-height: 180px;
                padding: 1.5rem;
            }
            .hero-wordmark {
                font-size: 2.5rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Loading viewing data...")
def load_data(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    data = data.drop_duplicates().copy()
    data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
    for column in ("Rating", "Watch_Count", "Watch_Time_Minutes", "Monthly_Revenue"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data


try:
    netflix = load_data(str(DATA_PATH))
except FileNotFoundError:
    st.error(f"Could not find the dataset at {DATA_PATH}.")
    st.stop()

if netflix.empty or netflix["Watch_Date"].dropna().empty:
    st.error("The dataset has no rows with valid watch dates to display.")
    st.stop()

st.sidebar.markdown("## Viewing report")
st.sidebar.caption("Filter the audience data")

regions = sorted(netflix["Region"].dropna().unique().tolist())
plans = [plan for plan in PLAN_ORDER if plan in netflix["Subscription_Plan"].dropna().unique()]
categories = sorted(netflix["Category"].dropna().unique().tolist())
valid_dates = netflix["Watch_Date"].dropna()
min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_plans = st.sidebar.multiselect("Subscription plan", plans, default=plans)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
selected_dates = st.sidebar.date_input(
    "Watch date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif len(selected_dates) == 1:
        start_date = end_date = selected_dates[0]
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = end_date = selected_dates

filtered = netflix.loc[
    netflix["Region"].isin(selected_regions)
    & netflix["Subscription_Plan"].isin(selected_plans)
    & netflix["Category"].isin(selected_categories)
    & netflix["Watch_Date"].dt.date.between(start_date, end_date)
].copy()

logo_markup = (
    f'<img class="hero-logo" src="{LOGO_URI}" alt="Netflix">'
    if LOGO_URI
    else '<span class="hero-wordmark">NETFLIX</span>'
)
hero_background = (
    f"background-image: linear-gradient(90deg, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.25)), url('{BACKGROUND_URI}');"
    if BACKGROUND_URI
    else "background-image: linear-gradient(100deg, #260306, #111 72%);"
)
st.markdown(
    f"""
    <section class="hero-banner" style="{hero_background}">
        <div class="hero-content">
            {logo_markup}
            <div class="hero-kicker">Audience intelligence / 2026</div>
            <p class="hero-caption">Revenue, ratings and viewing activity</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No viewing records match these filters. Adjust the selections in the sidebar.")
    st.stop()

total_revenue = filtered["Monthly_Revenue"].sum()
customer_count = filtered["Customer_ID"].nunique()
average_rating = filtered["Rating"].mean()
watch_hours = filtered["Watch_Time_Minutes"].sum() / 60

metric_columns = st.columns(4)
metric_columns[0].metric("Revenue", f"₹{total_revenue:,.0f}")
metric_columns[1].metric("Customers", f"{customer_count:,}")
metric_columns[2].metric("Rating / 5", f"{average_rating:.2f} / 5")
metric_columns[3].metric("Watch time", f"{watch_hours:,.0f} hrs")

st.markdown("### Performance at a glance")
chart_columns = st.columns(2, gap="large")


def style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor("#ffffff")
    axis.figure.set_facecolor("#ffffff")
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_visible(False)
    axis.spines["bottom"].set_color(CHART_COLORS["grid"])
    axis.tick_params(colors=CHART_COLORS["muted"], labelsize=9)
    axis.grid(axis="x", color=CHART_COLORS["grid"], linewidth=0.8)
    axis.set_axisbelow(True)


with chart_columns[0]:
    region_revenue = (
        filtered.groupby("Region")["Monthly_Revenue"].sum().sort_values(ascending=True)
    )
    fig, axis = plt.subplots(figsize=(7, 3.8))
    bars = axis.barh(region_revenue.index, region_revenue.values, color=CHART_COLORS["red"], height=0.58)
    style_axis(axis)
    axis.set_title("Revenue by region", loc="left", pad=14, fontsize=14, color=CHART_COLORS["ink"])
    axis.set_xlabel("Revenue (₹)", color=CHART_COLORS["muted"], fontsize=9)
    axis.bar_label(bars, labels=[f"₹{value / 1000:.1f}k" for value in region_revenue], padding=5, fontsize=8)
    axis.set_xlim(0, max(region_revenue.max() * 1.18, 1))
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with chart_columns[1]:
    plan_rating = (
        filtered.groupby("Subscription_Plan")["Rating"].mean().reindex(PLAN_ORDER).dropna()
    )
    fig, axis = plt.subplots(figsize=(7, 3.8))
    bars = axis.bar(
        plan_rating.index,
        plan_rating.values,
        color=[CHART_COLORS["deep_red"], CHART_COLORS["dark_red"], CHART_COLORS["red"]][: len(plan_rating)],
        width=0.55,
    )
    style_axis(axis)
    axis.set_title("Average rating by plan", loc="left", pad=14, fontsize=14, color=CHART_COLORS["ink"])
    axis.set_ylabel("Rating (out of 5)", color=CHART_COLORS["muted"], fontsize=9)
    axis.set_ylim(0, 5.8)
    axis.set_yticks(range(0, 6))
    axis.grid(axis="y", color=CHART_COLORS["grid"], linewidth=0.8)
    axis.grid(axis="x", visible=False)
    axis.bar_label(bars, labels=[f"{value:.2f}" for value in plan_rating], padding=4, fontsize=9)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with chart_columns[0]:
    category_revenue = (
        filtered.groupby("Category")["Monthly_Revenue"].sum().sort_values(ascending=True)
    )
    fig, axis = plt.subplots(figsize=(7, 4.2))
    bars = axis.barh(category_revenue.index, category_revenue.values, color=CHART_COLORS["dark_red"], height=0.58)
    style_axis(axis)
    axis.set_title("Revenue by category", loc="left", pad=14, fontsize=14, color=CHART_COLORS["ink"])
    axis.set_xlabel("Revenue (₹)", color=CHART_COLORS["muted"], fontsize=9)
    axis.bar_label(bars, labels=[f"₹{value / 1000:.1f}k" for value in category_revenue], padding=5, fontsize=8)
    axis.set_xlim(0, max(category_revenue.max() * 1.2, 1))
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with chart_columns[1]:
    monthly_revenue = (
        filtered.assign(Month=filtered["Watch_Date"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month")["Monthly_Revenue"]
        .sum()
        .sort_index()
    )
    fig, axis = plt.subplots(figsize=(7, 4.2))
    axis.plot(
        monthly_revenue.index,
        monthly_revenue.values,
        color=CHART_COLORS["red"],
        marker="o",
        markersize=6,
        linewidth=2.5,
    )
    style_axis(axis)
    axis.set_title("Revenue by month", loc="left", pad=14, fontsize=14, color=CHART_COLORS["ink"])
    axis.set_ylabel("Revenue (₹)", color=CHART_COLORS["muted"], fontsize=9)
    axis.tick_params(axis="x", rotation=0)
    axis.set_xticks(monthly_revenue.index)
    axis.set_xticklabels(monthly_revenue.index.strftime("%b %Y"))
    axis.grid(axis="y", color=CHART_COLORS["grid"], linewidth=0.8)
    axis.grid(axis="x", visible=False)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

st.divider()
with st.expander("Explore filtered records", expanded=False):
    st.caption(
        f"Showing {len(filtered):,} of {len(netflix):,} records after filters. "
        f"{len(netflix) - len(netflix.drop_duplicates()):,} duplicate rows removed during loading."
    )
    st.dataframe(filtered, width="stretch", hide_index=True)