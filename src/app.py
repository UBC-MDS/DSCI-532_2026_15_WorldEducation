from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget, render_plotly
from shiny.ui import update_selectize

# libraries for data processing
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# libraries for visualization
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import plotly.express as px
import seaborn as sns
import scienceplots
import pycountry

# Load data
#data_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "Global_education.csv"
#df = pd.read_csv(data_path, encoding="latin-1")
df = pd.read_csv('data/raw/Global_Education.csv', encoding='latin-1')

# Fix country naming inconsistencies
FIXES = {
    "The Bahamas": "Bahamas",
    "The Gambia": "Gambia",
    "Republic of the Congo": "Congo",
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
    "Ivory Coast": "Côte d'Ivoire",
    "Republic of Ireland": "Ireland",
    "East Timor": "Timor-Leste",
    "Federated States of Micronesia": "Micronesia, Federated States of",
    "Russia": "Russian Federation",
    "Iran": "Iran, Islamic Republic of",
    "Laos": "Lao People's Democratic Republic",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Vatican City": "Holy See (Vatican City State)",
    "Cape Verde": "Cabo Verde",
    "Palestinian National Authority": "Palestine, State of",
    "Moldova": "Moldova, Republic of",
    "Syria": "Syrian Arab Republic",
    "Tanzania": "Tanzania, United Republic of",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Bolivia": "Bolivia, Plurinational State of",
    "Vietnam": "Viet Nam",
    "Guinea0Bissau": "Guinea-Bissau",
    "Sï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿": "São Tomé and Príncipe",
    "Turkey": "Türkiye"
}

# Get iso3 for plotting
def to_iso3(name):
    if pd.isna(name):
        return None
    
    name = str(name).strip()
    name = FIXES.get(name, name)

    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        try:
            return pycountry.countries.search_fuzzy(name)[0].alpha_3
        except:
            return None

# Map countries to continents
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

app_ui = ui.page_fluid(
    ui.h2("World Education Dashboard"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.card(
                ui.card_header("Filters"),
                ui.input_selectize(
                    "input_region",
                    "Select Region:",
                    choices=["North America", "South America", "Europe", "Asia", "Africa", "Oceania"],
                    multiple=True,
                ),
                ui.input_select(
                    "input_map_metric",
                    "Map metric",
                    {
                        "Access": {
                            "OOSR_Avg_Primary": "Out-of-school rate (Primary, avg)",
                            "OOSR_Avg_Lower_Secondary": "Out-of-school rate (Lower secondary, avg)",
                            "OOSR_Avg_Upper_Secondary": "Out-of-school rate (Upper secondary, avg)",
                            "OOSR_Gap_Primary": "Out-of-school rate gender gap (Primary)",
                            "OOSR_Gap_Lower_Secondary": "Out-of-school rate gender gap (Lower secondary)",
                            "OOSR_Gap_Upper_Secondary": "Out-of-school rate gender gap (Upper secondary)",
                            "Gross_Primary_Education_Enrollment": "Gross primary enrollment",
                            "Gross_Tertiary_Education_Enrollment": "Gross tertiary enrollment",
                        },
                        "Completion": {
                            "Completion_Avg_Primary": "Completion rate (Primary, avg)",
                            "Completion_Avg_Lower_Secondary": "Completion rate (Lower secondary, avg)",
                            "Completion_Avg_Upper_Secondary": "Completion rate (Upper secondary, avg)",
                            "Completion_Gap_Primary": "Completion rate gender gap (Primary)",
                            "Completion_Gap_Lower_Secondary": "Completion rate gender gap (Lower secondary)",
                            "Completion_Gap_Upper_Secondary": "Completion rate gender gap (Upper secondary)",
                        },
                        "Learning": {
                            "Grade_2_3_Proficiency_Reading": "Grade 2–3 proficiency (Reading)",
                            "Grade_2_3_Proficiency_Math": "Grade 2–3 proficiency (Math)",
                            "Primary_End_Proficiency_Reading": "Primary end proficiency (Reading)",
                            "Primary_End_Proficiency_Math": "Primary end proficiency (Math)",
                            "Lower_Secondary_End_Proficiency_Reading": "Lower secondary end proficiency (Reading)",
                            "Lower_Secondary_End_Proficiency_Math": "Lower secondary end proficiency (Math)",
                        },
                        "Context": {
                            "Youth_15_24_Literacy_Rate_Male": "Youth literacy rate (Male)",
                            "Youth_15_24_Literacy_Rate_Female": "Youth literacy rate (Female)",
                            "Literacy_Gap": "Youth literacy gender gap (Male - Female)",
                            "Birth_Rate": "Birth rate",
                            "Unemployment_Rate": "Unemployment rate",
                        },
                    },
                ),
                ui.input_checkbox_group(
                    "input_completion_levels",
                    "Completion Level",
                    choices={
                        "Primary": "Primary",
                        "Lower_Secondary": "Lower secondary",
                        "Upper_Secondary": "Upper secondary",
                    },
                    selected=["Primary", "Lower_Secondary", "Upper_Secondary"],
                ),
                ui.input_action_button("apply_filters", "Apply Filters", class_="btn-primary w-100"),
            ),
            width=300,
        ),

        ui.layout_column_wrap(
            ui.card(
                ui.card_header("Global Education Indicators Map"),
                output_widget("world_map")
            ),
            ui.layout_column_wrap(
                ui.card(
                    ui.card_header("Trend Analysis"),
                    ui.div("Plots will be displayed here"),
                ),
                ui.card(
                    ui.card_header("Bar plot"),
                    #ui.output_plot("bar"),
                    ui.div("Plots will be displayed here"),
                ),
                ui.card(
                    ui.card_header("Literacy Scatterplot"),
                    output_widget("scatterplot"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Data Table"),
                    ui.output_data_frame("tbl"),
                ),
                width=1/4,
            ),
            width=1,
            heights_equal="row",
        ),
    ),
)


def server(input, output, session):

    # 1) All data wrangling here
    @reactive.Calc
    def processed_df() -> pd.DataFrame:
        processed = df.copy()

        # Drop unused columns (handle trailing space safely)
        cols_to_drop = ["Latitude ", "Longitude", "OOSR_Pre0Primary_Age_Male", "OOSR_Pre0Primary_Age_Female"]
        processed = processed.drop(columns=[c for c in cols_to_drop if c in processed.columns])

        # iso3
        processed["iso3"] = processed["Countries and areas"].apply(to_iso3)

        # Fix country name for STP
        processed.loc[processed["iso3"] == "STP", "Countries and areas"] = "Sao Tome and Principe"

        # Region mapping + remove Other
        processed["Region"] = processed["Countries and areas"].map(region_map).fillna("Other")
        processed = processed[processed["Region"] != "Other"].copy()

        # 0 -> NaN for numeric columns
        numeric_cols = processed.select_dtypes(include=["number"]).columns
        processed[numeric_cols] = processed[numeric_cols].replace(0, np.nan)

        # Literacy gap + average
        processed["Literacy_Gap"] = (
            processed["Youth_15_24_Literacy_Rate_Male"] - processed["Youth_15_24_Literacy_Rate_Female"]
        )
        processed["Literacy_Avg"] = processed[
            ["Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female"]
        ].mean(axis=1)

        # Completion + OOSR gaps/avgs
        levels = ["Primary", "Lower_Secondary", "Upper_Secondary"]
        for level in levels:
            processed[f"Completion_Gap_{level}"] = (
                processed[f"Completion_Rate_{level}_Male"] - processed[f"Completion_Rate_{level}_Female"]
            )
            processed[f"Completion_Avg_{level}"] = processed[
                [f"Completion_Rate_{level}_Male", f"Completion_Rate_{level}_Female"]
            ].mean(axis=1)

            processed[f"OOSR_Gap_{level}"] = (
                processed[f"OOSR_{level}_Age_Male"] - processed[f"OOSR_{level}_Age_Female"]
            )
            processed[f"OOSR_Avg_{level}"] = processed[
                [f"OOSR_{level}_Age_Male", f"OOSR_{level}_Age_Female"]
            ].mean(axis=1)

        return processed

    # 2) Apply filters (triggered by click filter button)
    @reactive.Calc
    @reactive.event(input.apply_filters, ignore_none=False)
    def filtered_df():
        d = processed_df()
    
        selected_regions = input.input_region()
        if selected_regions:
            d = d[d["Region"].isin(selected_regions)].copy()
    
        return d

    @output
    @render_widget
    def world_map():
        d = filtered_df()
        metric = input.input_map_metric()
        fig = px.choropleth(
            d, 
            locations="iso3", 
            hover_name="Countries and areas",
            color=metric,
            color_continuous_scale="viridis",
            projection="natural earth"
        )

        fig.update_geos(
            showcoastlines=True,
            showcountries=True,
            showframe=False
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0) 
        )

        return fig
    
    @render_plotly
    def scatterplot():
        d = filtered_df()
        
        return px.scatter(
            d,
            x="Youth_15_24_Literacy_Rate_Male",
            y="Youth_15_24_Literacy_Rate_Female",
            color="Region",
            hover_name="Countries and areas",
            color_discrete_sequence=px.colors.qualitative.Set2,
            trendline="ols",
            labels={
                "Region": "Region",
                "Youth_15_24_Literacy_Rate_Male": "Literacy Rate (Male)",
                "Youth_15_24_Literacy_Rate_Female": "Literacy Rate (Female)",
            }
        )
    
    @output
    @render.data_frame
    def tbl():
        d = filtered_df()
        metric = input.input_map_metric()
        cols = ["Countries and areas", "Region", "iso3", metric]
        cols = [c for c in cols if c in d.columns]

        return render.DataGrid(
            d[cols],
            selection_mode="rows",
            height="300px"
        )

app = App(app_ui, server)