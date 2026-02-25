import pandas as pd
from shiny import App, ui, render, reactive
from shinywidgets import render_widget, output_widget
from pathlib import Path # for data reading
from matplotlib import pyplot as plt 
import plotly.express as px # for creating world map
from ipyleaflet import Map
import geopandas as gpd

# Load data
data_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "Global_education.csv"
df = pd.read_csv(data_path, encoding="latin-1")

region_map = {
    # Africa
        "Algeria": "Africa", "Angola": "Africa", "Benin": "Africa", "Botswana": "Africa",
        "Burkina Faso": "Africa", "Burundi": "Africa", "Cabo Verde": "Africa",
        "Cameroon": "Africa", "Central African Republic": "Africa", "Chad": "Africa",
        "Comoros": "Africa", "Republic of the Congo": "Africa",
        "Democratic Republic of the Congo": "Africa", "Djibouti": "Africa",
        "Egypt": "Africa", "Equatorial Guinea": "Africa", "Eritrea": "Africa",
        "Eswatini": "Africa", "Ethiopia": "Africa", "Gabon": "Africa",
        "The Gambia": "Africa", "Ghana": "Africa", "Guinea": "Africa",
        "Guinea0Bissau": "Africa", "Ivory Coast": "Africa", "Kenya": "Africa",
        "Lesotho": "Africa", "Liberia": "Africa", "Libya": "Africa",
        "Madagascar": "Africa", "Malawi": "Africa", "Mali": "Africa",
        "Mauritania": "Africa", "Mauritius": "Africa", "Morocco": "Africa",
        "Mozambique": "Africa", "Namibia": "Africa", "Niger": "Africa",
        "Nigeria": "Africa", "Rwanda": "Africa", "Sao Tome and Principe": "Africa",
        "Senegal": "Africa", "Seychelles": "Africa", "Sierra Leone": "Africa",
        "Somalia": "Africa", "South Africa": "Africa", "South Sudan": "Africa",
        "Sudan": "Africa", "Tanzania": "Africa", "Togo": "Africa",
        "Tunisia": "Africa", "Uganda": "Africa", "Zambia": "Africa",
        "Zimbabwe": "Africa", "Cape Verde": "Africa",

        # Asia
        "Afghanistan": "Asia", "Armenia": "Asia", "Azerbaijan": "Asia",
        "Bahrain": "Asia", "Bangladesh": "Asia", "Bhutan": "Asia",
        "Brunei": "Asia", "Cambodia": "Asia", "China": "Asia",
        "Cyprus": "Asia", "Georgia": "Asia", "India": "Asia",
        "Indonesia": "Asia", "Iran": "Asia", "Iraq": "Asia",
        "Israel": "Asia", "Japan": "Asia", "Jordan": "Asia",
        "Kazakhstan": "Asia", "Kuwait": "Asia", "Kyrgyzstan": "Asia",
        "Laos": "Asia", "Lebanon": "Asia", "Malaysia": "Asia",
        "Maldives": "Asia", "Mongolia": "Asia", "Myanmar": "Asia",
        "Nepal": "Asia", "North Korea": "Asia", "Oman": "Asia",
        "Pakistan": "Asia", "Palestinian National Authority": "Asia",
        "Philippines": "Asia", "Qatar": "Asia", "Saudi Arabia": "Asia",
        "Singapore": "Asia", "South Korea": "Asia", "Sri Lanka": "Asia",
        "Syria": "Asia", "Tajikistan": "Asia", "Thailand": "Asia",
        "East Timor": "Asia", "Turkey": "Asia", "Turkmenistan": "Asia",
        "United Arab Emirates": "Asia", "Uzbekistan": "Asia",
        "Vietnam": "Asia", "Yemen": "Asia",

        # Europe
        "Albania": "Europe", "Andorra": "Europe", "Austria": "Europe",
        "Belarus": "Europe", "Belgium": "Europe", "Bosnia and Herzegovina": "Europe",
        "Bulgaria": "Europe", "Croatia": "Europe", "Czech Republic": "Europe",
        "Denmark": "Europe", "Estonia": "Europe", "Finland": "Europe",
        "France": "Europe", "Germany": "Europe", "Greece": "Europe",
        "Hungary": "Europe", "Iceland": "Europe", "Ireland": "Europe",
        "Italy": "Europe", "Latvia": "Europe", "Liechtenstein": "Europe",
        "Lithuania": "Europe", "Luxembourg": "Europe", "Malta": "Europe",
        "Moldova": "Europe", "Monaco": "Europe", "Montenegro": "Europe",
        "Netherlands": "Europe", "North Macedonia": "Europe", "Norway": "Europe",
        "Poland": "Europe", "Portugal": "Europe", "Romania": "Europe",
        "Russia": "Europe", "San Marino": "Europe", "Serbia": "Europe",
        "Slovakia": "Europe", "Slovenia": "Europe", "Spain": "Europe",
        "Sweden": "Europe", "Switzerland": "Europe", "Ukraine": "Europe",
        "United Kingdom": "Europe", "Vatican City": "Europe", 
        "Republic of Ireland": "Europe",

        # North America
        "Antigua and Barbuda": "North America", "Bahamas": "North America",
        "Barbados": "North America", "Belize": "North America",
        "Canada": "North America", "Costa Rica": "North America",
        "Cuba": "North America", "Dominica": "North America",
        "Dominican Republic": "North America", "El Salvador": "North America",
        "Grenada": "North America", "Guatemala": "North America",
        "Haiti": "North America", "Honduras": "North America",
        "Jamaica": "North America", "Mexico": "North America",
        "Nicaragua": "North America", "Panama": "North America",
        "Saint Kitts and Nevis": "North America", "Saint Lucia": "North America",
        "Saint Vincent and the Grenadines": "North America",
        "Trinidad and Tobago": "North America", "United States": "North America",
        "Anguilla":"North America", "The Bahamas":"North America",
        "British Virgin Islands":"North America", "Montserrat":"North America",
        "Turks and Caicos Islands":"North America",

        # South America
        "Argentina": "South America", "Bolivia": "South America",
        "Brazil": "South America", "Chile": "South America",
        "Colombia": "South America", "Ecuador": "South America",
        "Guyana": "South America", "Paraguay": "South America",
        "Peru": "South America", "Suriname": "South America",
        "Uruguay": "South America", "Venezuela": "South America",

        # Oceania
        "Australia": "Oceania", "Fiji": "Oceania", "Kiribati": "Oceania",
        "Marshall Islands": "Oceania", "Micronesia": "Oceania",
        "Nauru": "Oceania", "New Zealand": "Oceania", "Palau": "Oceania",
        "Papua New Guinea": "Oceania", "Samoa": "Oceania",
        "Solomon Islands": "Oceania", "Tonga": "Oceania",
        "Tuvalu": "Oceania", "Vanuatu": "Oceania",
        "Cook Islands": "Oceania", "Federated States of Micronesia": "Oceania",
        "Niue": "Oceania", "Tokelau": "Oceania",
    }

df["Region"] = df["Countries and areas"].map(region_map).fillna("Other")
df = df[df["Region"] != "Other"] # Remove other region
df.columns = df.columns.str.strip()

# Numeric columns for plots
numeric_cols = [ 
    "Completion_Rate_Primary_Male", 
    "Completion_Rate_Primary_Female", 
    "Completion_Rate_Lower_Secondary_Male", 
    "Completion_Rate_Lower_Secondary_Female", 
    "Birth_Rate", 
    "Gross_Primary_Education_Enrollment", 
    "Unemployment_Rate"
]

app_ui = ui.page_fluid(
    ui.h2("World Education Dashboard"),
    ui.layout_sidebar(
        # Left sidebar with filters
        ui.sidebar(
            ui.card(
                ui.card_header("Filters"),
                ui.input_select(
                    "region",
                    "Select Region:",
                    choices=["All"] + sorted(df["Region"].unique())
                ),
                ui.input_selectize(
                    "country",
                    "Select Country:",
                    choices=sorted(df["Countries and areas"].unique()),
                    multiple=True
                ),
                ui.input_select(
                    "education_level",
                    "Education Level:",
                    choices=["Primary", "Lower Secondary", "Upper Secondary"]
                ),
                ui.input_select(
                    "var",
                    "Select Variable for Histogram:",
                    choices=numeric_cols
                ),
                ui.input_slider(
                    "birth_rate_range",
                    "Birth Rate Range:",
                    min=int(df["Birth_Rate"].min()),
                    max=int(df["Birth_Rate"].max()),
                    value=[int(df["Birth_Rate"].min()), int(df["Birth_Rate"].max())]
                ),
                ui.input_checkbox_group(
                    "gender",
                    "Gender:",
                    choices=["Male", "Female"],
                    selected=["Male", "Female"]
                ),
                ui.input_action_button("apply_filters", "Apply Filters", class_="btn-primary w-100")
            ),
            width=300
        ),

# Main content area with three cards
        ui.layout_column_wrap(
            # World Map Card (full width)
            ui.card(
                ui.card_header("Global Education Indicators Map"),
                output_widget("world_map")
                #ui.div("World map will be displayed here", style="padding: 20px; text-align: center; color: #888;")
            ),
            
            # Plots and Data Table side by side
            ui.layout_column_wrap(
                # Plots Card
                ui.card(
                    ui.card_header("Trend Analysis"),
                    ui.output_plot("hist"),  # histogram output
                    #ui.div("Plots will be displayed here", style="padding: 20px; text-align: center; color: #888;")
                ),
                
                # Data Table Card
                ui.card(
                    ui.card_header("Country Data"),
                    ui.output_plot("bar"),  # barplot output
                    #ui.div("Data table will be displayed here", style="padding: 20px; text-align: center; color: #888;")
                ),
                
                width=1/2
            ),
            
            width=1,
            heights_equal="row"
        )
    )
)

def server(input, output, session):
    # Add your server logic here
    @reactive.Calc
    def filtered_df():
        d = df.copy()

        # Filter by region if not "All"
        if input.region() != "All":
            d = d[d["Region"] == input.region()]
        
        if len(input.country()) > 0: 
            d = d[d["Countries and areas"].isin(input.country())]

        br_min, br_max = input.birth_rate_range() 
        d = d[(d["Birth_Rate"] >= br_min) & (d["Birth_Rate"] <= br_max)]

        return d


    @output
    @render_widget
    def world_map():
        d = filtered_df()
        col = input.var()

        fig = px.scatter_geo(
            d,
            lat="Latitude",
            lon="Longitude",
            hover_name="Countries and areas",
            color=col,
            color_continuous_scale="Viridis",
            projection="natural earth",
            size_max=10
        )

        fig.update_layout(
            title=f"World Map — {col}",
            margin=dict(l=0, r=0, t=30, b=0)
        )

        return fig

    @output
    @render.plot
    def hist():
        col = input.var()
        d = filtered_df()

        fig, ax = plt.subplots(figsize=(7, 4))

        # If no country selected, show all countries in one histogram
        if len(input.country()) == 0:
            ax.hist(d[col].dropna(), bins=20, color="skyblue", edgecolor="black")
            ax.set_title(f"Histogram of {col} (All Countries)")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            return fig

        # Otherwise, plot one histogram per selected country
        for country in input.country():
            subset = d[d["Countries and areas"] == country][col].dropna()
            if len(subset) > 0:
                ax.hist(subset, bins=20, alpha=0.5, label=country)

        ax.set_title(f"Histogram of {col} by Country")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        ax.legend(title="Country")

        return fig

    @output
    @render.plot
    def bar():
        col = input.var()
        d = filtered_df()

        # If no country selected, show all countries
        if len(input.country()) == 0:
            d = d.copy()
        else:
            d = d[d["Countries and areas"].isin(input.country())]

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            d["Countries and areas"],
            d[col],
            color=plt.cm.tab20.colors[: len(d)]
        )

        ax.set_title(f"{col} by Country")
        ax.set_xlabel("Country")
        ax.set_ylabel(col)
        ax.tick_params(axis="x", rotation=90)

        return fig



app = App(app_ui, server)