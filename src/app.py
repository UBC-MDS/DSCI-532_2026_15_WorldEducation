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
df = pd.read_csv("data/processed/processed_global_education.csv", encoding='latin-1', index_col=0)
world_avg_el_completion_rate = df[["Completion_Rate_Primary_Male", "Completion_Rate_Primary_Female",]].mean().mean()
table_feature_choices = df.columns.tolist()
region_choices = ["North America", "South America", "Europe", "Asia", "Africa", "Oceania"]
region_color_map = {
    "North America": "#66c2a5",
    "South America": "#fc8d62",
    "Europe": "#8da0cb",
    "Asia": "#e78ac3",
    "Africa": "#a6d854",
    "Oceania": "#ffd92f",
}
map_metric_choices = {
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
}

def kpi1_caption(rate):
    """Create caption for primary completion rate KPI"""

    rate_diff = rate - world_avg_el_completion_rate

    if rate_diff >= 0:
        caption_str = f"Completion rate is {rate_diff:.1f} % above world average {world_avg_el_completion_rate:.1f} %"
    else:
        caption_str = f"Completion rate is {-rate_diff:.1f} % below world average {world_avg_el_completion_rate:.1f} %"

    return ui.tags.div(
        ui.HTML(f'<strong style="opacity:0.9">{caption_str}</strong>'),
    )

def kpi2_caption(rate_diff):
    """Create caption for primary completion rate gender difference KPI"""

    if rate_diff < -2:
        caption_str = "Male completion rate is more than 2 percentage points below female"
    elif rate_diff < -1:
        caption_str = "Male completion rate is more than 1 percentage point below female"
    elif rate_diff < 1:
        caption_str = "Completion rates are within 1 percentage point"
    elif rate_diff < 2:
        caption_str = "Female completion rate is more than 1 percentage point below male"
    else:
        caption_str = "Female completion rate is more than 2 percentage points below male"

    return ui.tags.div(
        ui.HTML(f'<strong style="opacity:0.9">{caption_str}</strong>'),
    )

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.title("World Education Dashboard")
    ),
    ui.navset_tab(
        ui.nav_panel(
            "Main Dashboard",
            ui.h2("World Education Dashboard"),
            ui.layout_sidebar(
                ui.sidebar(
                    ui.card(
                        ui.card_header("Filters"),
                        ui.input_checkbox_group(
                            "input_region",
                            "Select Region:",
                            choices=region_choices,
                            selected=region_choices,
                        ),
                        ui.div(
                            ui.input_action_button(
                                "select_all_regions",
                                "Select All",
                                class_="btn-outline-primary btn-sm me-2"
                            ),
                            ui.input_action_button(
                                "reset_regions",
                                "Reset",
                                class_="btn-outline-secondary btn-sm"
                            ),
                        )
                    ),
                    width=300,
                ),

                ui.navset_tab(
                    ui.nav_panel(
                        "Overview",
                        ui.layout_column_wrap(
                            ui.card(
                                ui.card_header("Global Education Indicators Map"),
                                ui.input_select(
                                    "input_map_metric",
                                    "Map metric",
                                    map_metric_choices,
                                ),
                                output_widget("world_map"),
                            ),
                            ui.card(
                                ui.card_header("Primary School Completion"),
                                ui.layout_column_wrap(
                                    ui.output_ui("elementary_completion_box"),
                                    ui.output_ui("el_completion_rate_gender_difference_box"),
                                    fill=False,
                                    width=1,
                                ),
                            ),
                            width=1,
                        ),
                    ),
                    ui.nav_panel(
                        "Completion & Literacy",
                        ui.layout_column_wrap(
                            ui.card(
                                ui.card_header("Average Education Level by Region"),
                                output_widget("education_level_by_region_bar"),
                            ),
                            ui.card(
                                ui.card_header("Education Level by Sex"),
                                output_widget("completion_rate_gap_by_region_bar"),
                            ),
                            ui.card(
                                ui.card_header("Male vs Female Literacy Rate by Region"),
                                output_widget("literacy_scatterplot"),
                                full_screen=True,
                            ),
                            width=1/3,
                        ),
                    ),
                    ui.nav_panel(
                        "Data Table",
                        ui.card(
                            ui.card_header("Data Table"),
                            ui.input_selectize(
                                "input_table_features",
                                "Table features:",
                                choices=table_feature_choices,
                                selected=["Countries and areas", "Region"],
                                multiple=True,
                            ),
                            ui.output_data_frame("tbl"),
                        ),
                    ),
                ),
            ),
        ),
        ui.nav_panel(
            "Query with Chat",
            "LLM query and plots"
            # ADD LAYOUT HERE
        )
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

    # 2) Apply region filters reactively
    @reactive.Calc
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
    def sex_completion_rate_df():
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
    
    @reactive.Calc
    def region_completion_rate_df():
        """Melt columns with data about education level completion.

        This makes it possible create education_level_by_region_bar bar plot.
            
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
                "Completion_Avg_Primary",
                "Completion_Avg_Lower_Secondary",
                "Completion_Avg_Upper_Secondary",
                "Region",
                "iso3"
            ]]
        d = pd.melt(
            d, 
            id_vars=["Region", "iso3"], 
            value_vars=[
                "Completion_Avg_Primary",
                "Completion_Avg_Lower_Secondary",
                "Completion_Avg_Upper_Secondary",
            ],
            value_name="Completion_Rate",
            var_name="Completion_Rate_Group",
            ignore_index=True
            )

        d["Education_Level"] = d["Completion_Rate_Group"].str.split("_").str[2:].str.join(" ")
    
        d = (
            d[["Region", "Education_Level", "Completion_Rate"]]
            .groupby(["Region", "Education_Level"])
            .mean()
            .reset_index()
        )

        return d

    @reactive.Calc
    def completion_gap_by_region_df():
        """
        Create dataframe of completion rate gender gap by region and education level.
                
        Parameters
        ----------
        None

        Returns
        -------
        pd.Dataframe
            The melted dataframe
            
        """
        
        d = filtered_df().copy()
    
        d = d[
            [
                "Region",
                "Completion_Gap_Primary",
                "Completion_Gap_Lower_Secondary",
                "Completion_Gap_Upper_Secondary",
            ]
        ]
    
        d = pd.melt(
            d,
            id_vars=["Region"],
            value_vars=[
                "Completion_Gap_Primary",
                "Completion_Gap_Lower_Secondary",
                "Completion_Gap_Upper_Secondary",
            ],
            var_name="Gap_Group",
            value_name="Completion_Rate_Gap",
            ignore_index=True,
        )
    
        d["Education_Level"] = (
            d["Gap_Group"]
            .str.replace("Completion_Gap_", "", regex=False)
            .str.replace("_", " ", regex=False)
        )
    
        d = (
            d.groupby(["Region", "Education_Level"], as_index=False)["Completion_Rate_Gap"]
            .mean()
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
            color_discrete_map=region_color_map,
            category_orders={"Region": region_choices},
            labels={
                "Region": "Region",
                "Youth_15_24_Literacy_Rate_Male": " Male Literacy Rate (%)",
                "Youth_15_24_Literacy_Rate_Female": "Female Literacy Rate (%)",
            }
        )

        xy_min = d[["Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female"]].min().min() - 5
        xy_max = d[["Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female"]].max().max() + 5

        # Add 45-degree diagonal line (y = x)
        fig.add_shape(
            type="line",
            x0=-10, y0=-10,
            x1=110, y1=110,
            line=dict(color="black", dash="dash")
        )

        # Tidy axis
        axis_range = xy_max-xy_min
        if axis_range < 15:
            tick_size = 2
        elif axis_range < 40:
            tick_size = 5
        else:
            tick_size = 10
        fig.update_xaxes(dtick=tick_size)
        fig.update_yaxes(dtick=tick_size)
        fig.update_layout(
            xaxis=dict(range=[xy_min, xy_max]),  # x scale follows y
            yaxis=dict(range=[xy_min, xy_max])
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
        selected_cols = input.input_table_features()
    
        if not selected_cols:
            selected_cols = list(d.columns)
    
        cols = [c for c in selected_cols if c in d.columns]
    
        return render.DataGrid(
            d[cols],
            selection_mode="rows",
            height="300px"
        )

    @output
    @render_plotly
    def completion_rate_gap_by_region_bar():
        """Create bar plot of completion rate gender gap by region.

        Parameters
        ----------
        None

        Returns
        -------
        px.bar
            Plotly express bar plot object.
        
        """
        d = completion_gap_by_region_df()
    
        fig = px.bar(
            d,
            x="Education_Level",
            y="Completion_Rate_Gap",
            color="Region",
            color_discrete_map=region_color_map,
            barmode="group",
            category_orders={
                "Education_Level": ["Primary", "Lower Secondary", "Upper Secondary"],
                "Region": region_choices,
            },
            labels={
                "Education_Level": "Education Level",
                "Completion_Rate_Gap": "Completion Rate Gap (Male - Female, %)",
            },
        )
    
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        fig.update_yaxes(dtick=2)
    
        return fig
    
    @output
    @render_plotly
    def education_level_by_region_bar():
        """Create bar plot of education level completed separated by region.

        Parameters
        ----------
        None

        Returns
        -------
        px.bar
            Plotly express bar plot object.
        
        """
        d = region_completion_rate_df()
    
        fig = px.bar(
            d,
            x="Education_Level",
            y="Completion_Rate",
            color="Region",
            color_discrete_map=region_color_map,
            barmode="group",
            category_orders={
                "Education_Level": ["Primary", "Lower Secondary", "Upper Secondary"],
                "Region": region_choices,
            },
            labels={
                "Education_Level": "Education Level",
                "Completion_Rate": "Completion Rate (%)"
            },
            range_y=[0, 100]
        )
    
        fig.update_yaxes(dtick=20)
    
        return fig

    @render.ui
    def elementary_completion_box():
        avg_comp_rate = (
            sex_completion_rate_df()[["Education_Level", "Completion_Rate"]]
            .groupby(["Education_Level"])
            .mean()
            .loc["Primary"]
            .values[0]
        )

        if np.abs(avg_comp_rate) < 70:
            rate_theme = "danger"
        elif np.abs(avg_comp_rate) < 90:
            rate_theme = "warning"
        else:
            rate_theme = "success"

        return ui.value_box(
            "Average rate of all selected regions", 
            f"{avg_comp_rate:.1f} %", 
            kpi1_caption(avg_comp_rate),
            theme=rate_theme
        )
    
    @render.ui
    def el_completion_rate_gender_difference_box():
        df = sex_completion_rate_df().copy()
        male_comp_rate = (
            df[(df["Sex"]=="Male") & (df["Education_Level"]=="Primary")]
            .loc[:,"Completion_Rate"]
            .values[0]
        )
        female_comp_rate = (
            df[(df["Sex"]=="Female") & (df["Education_Level"]=="Primary")]
            .loc[:,"Completion_Rate"]
            .values[0]
        )
        comp_rate_diff = male_comp_rate - female_comp_rate

        if np.abs(comp_rate_diff) > 2:
            diff_theme = "danger"
        elif np.abs(comp_rate_diff) > 1:
            diff_theme = "warning"
        else:
            diff_theme = "success"

        return ui.value_box(
            "Difference between male rate and female rate", 
            f"{comp_rate_diff:.1f} %", 
            kpi2_caption(comp_rate_diff),
            theme=diff_theme
        )
    
    @reactive.effect
    @reactive.event(input.select_all_regions)
    def _select_all_regions():
        ui.update_checkbox_group(
            "input_region",
            selected=region_choices,
            session=session
        )

    @reactive.effect
    @reactive.event(input.reset_regions)
    def _reset_regions():
        ui.update_checkbox_group(
            "input_region",
            selected=region_choices,
            session=session
        )

app = App(app_ui, server)
