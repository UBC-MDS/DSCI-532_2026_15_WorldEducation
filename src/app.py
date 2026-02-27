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
df = pd.read_csv("data/processed/processed_global_education.csv", encoding='latin-1')

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
                    ui.card_header("Bar plot"),
                    output_widget("education_level_by_gender_bar"),
                ),
                ui.card(
                    ui.card_header("Literacy Scatterplot"),
                    output_widget("literacy_scatterplot"),
                    full_screen=True,
                ),
                width=1/2,
            ),
            ui.card(
                ui.card_header("Data Table"),
                ui.output_data_frame("tbl"),
                ),
            width=1,
            heights_equal="row",
        ),
    ),
)


def server(input, output, session):

    # 1) Get dataframe
    @reactive.Calc
    def processed_df() -> pd.DataFrame:
        """Imports processed data frame

        Parameters
        ----------
        None

        Returns
        -------
        pd.Dataframe
            The processed world education dataframe

        """
        processed = df.copy()

        return processed

    # 2) Apply filters (triggered by click filter button)
    @reactive.Calc
    @reactive.event(input.apply_filters, ignore_none=False)
    def filtered_df():
        """Apply filters when triggered by click of "Apply Filters" button

        Filters included are:
        
        - selected regions
    
        Parameters
        ----------
        None

        Returns
        -------
        pd.Dataframe
            The filtered world education dataframe.
        """
        d = processed_df()
    
        selected_regions = input.input_region()
        if selected_regions:
            d = d[d["Region"].isin(selected_regions)].copy()
    
        return d
    
    @reactive.Calc
    def melted_completion_df():
        """Melt columns with data about education level completion.

        This makes it possible create education_level_by_gender_bar bar plot.
            
        Parameters
        ----------
        None

        Returns
        -------
        pd.Dataframe
            The melted dataframe
        """
        d = filtered_df().copy()
    
        d = d[[
                "Completion_Rate_Primary_Male",
                "Completion_Rate_Primary_Female",
                "Completion_Rate_Lower_Secondary_Male",
                "Completion_Rate_Lower_Secondary_Female",
                "Completion_Rate_Upper_Secondary_Male",
                "Completion_Rate_Upper_Secondary_Female",
                "Region",
                "iso3"
            ]]
        d = pd.melt(
            d, 
            id_vars=["Region", "iso3"], 
            value_vars=[
                "Completion_Rate_Primary_Male",
                "Completion_Rate_Primary_Female",
                "Completion_Rate_Lower_Secondary_Male",
                "Completion_Rate_Lower_Secondary_Female",
                "Completion_Rate_Upper_Secondary_Male",
                "Completion_Rate_Upper_Secondary_Female",
            ],
            value_name="Completion_Rate",
            var_name="Completion_Rate_Group",
            ignore_index=True
            )
        d["Sex"] = d["Completion_Rate_Group"].str.split("_").str[-1]
        d["Education_Level"] = d["Completion_Rate_Group"].str.split("_").str[2:-1].str.join(" ")
    
        d = (
            d[["Sex", "Education_Level", "Completion_Rate"]]
            .groupby(["Sex", "Education_Level"])
            .mean()
            .reset_index()
        )

        return d

    # 3) Create object to display
    @output
    @render_widget
    def world_map():
        """Create interactive world map figure.

        Parameters
        ----------
        None

        Returns
        -------
        plotly.express.chorpleth
            Interactive world map figure.
        """
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
    

    @output
    @render_plotly
    def literacy_scatterplot():
        """Create scatterplot of male vs female literacy rates by region.

        Parameters
        ----------
        None

        Returns
        -------
        plotly.express.scatter
            Scatterplot of male vs female literacy rate by region.
        """
        d = filtered_df()

        fig = px.scatter(
            d,
            x="Youth_15_24_Literacy_Rate_Male",
            y="Youth_15_24_Literacy_Rate_Female",
            color="Region",
            hover_name="Countries and areas",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={
                "Region": "Region",
                "Youth_15_24_Literacy_Rate_Male": " Male Literacy Rate",
                "Youth_15_24_Literacy_Rate_Female": "Female Literacy Rate",
            }
        )

        # Add 45-degree diagonal line (y = x)
        fig.add_shape(
            type="line",
            x0=0, y0=0,
            x1=100, y1=100,
            line=dict(color="black", dash="dash")
        )

        return fig

    @output
    @render.data_frame
    def tbl():
        """Create DataGrid object to be displayed

        Parameters
        ----------
        None

        Returns
        -------
        shiny.render.DataGrid
            Tabular data to be displayed.
        """
        d = filtered_df()
        metric = input.input_map_metric()
        cols = ["Countries and areas", "Region", "iso3", metric]
        cols = [c for c in cols if c in d.columns]

        return render.DataGrid(
            d[cols],
            selection_mode="rows",
            height="300px"
        )



    @output
    @render_plotly
    def education_level_by_gender_bar():
        """Create bar plot of education level completed separated by gender.

        Parameters
        ----------
        None

        Returns
        -------
        px.bar
            Plotly express bar plot object.
        
        """
        d = melted_completion_df()

        fig = px.bar(
            d,
            x = "Education_Level",
            y = "Completion_Rate",
            color = "Sex",
            barmode = "group",
            category_orders = {"Education_Level": ["Primary", "Lower Secondary", "Upper Secondary"]},
            labels={
                "Education_Level": "Education Level",
                "Completion_Rate": "Completion Rate (%)"
            }
        )

        return fig

    

app = App(app_ui, server)