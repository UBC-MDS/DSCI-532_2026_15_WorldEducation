from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget, render_plotly
import pandas as pd
import numpy as np
import plotly.express as px
import os
import chatlas as clt
from pathlib import Path
from dotenv import load_dotenv
from querychat import QueryChat
import ibis
from ibis import _

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# ==========================================
#   SETUP & DATA LOADING
# ==========================================
# Connect to parquet file using ibis + DuckDB
con = ibis.duckdb.connect()
education_table = con.read_parquet("data/processed/processed_global_education.parquet")

# Load a small sample for metadata (column names, choices, etc.)
df_sample = education_table.limit(1000).execute()

# Grab all columns except the junk index column
raw_cols = [c for c in df_sample.columns.tolist() if c != "Unnamed: 0"]

# Automatically group the columns using list comprehensions
table_feature_choices = {
    "Identifiers": {
        "Countries and areas": "Countries and areas",
        "Region": "Region",
        "iso3": "iso3"
    },
    "Access (Out of School & Enrollment)": {c: c for c in raw_cols if "OOSR" in c or "Enrollment" in c},
    "Completion": {c: c for c in raw_cols if "Completion" in c},
    "Learning (Proficiency)": {c: c for c in raw_cols if "Proficiency" in c},
    "Context & Literacy": {c: c for c in raw_cols if "Literacy" in c or c in ["Birth_Rate", "Unemployment_Rate"]}
}

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
def metric_label(metric_key):
    """Return a human-readable label for a metric key.

    Parameters
    ----------
    metric_key : str
        The internal metric column name used in the dataset.

    Returns
    -------
    str
        A user-friendly label for the metric if found in
        ``map_metric_choices``; otherwise returns the original key.
    """
    for group in map_metric_choices.values():
        if metric_key in group:
            return group[metric_key]
    return metric_key

# Initialize the correct Chatlas Client inside the server so it's safe for multi-users
# Note: QueryChat requires a valid client, so we'll skip QueryChat initialization if no API key is available
if os.environ.get("USE_LOCAL_LLM", "False").lower() == "true":
    llm_client = clt.ChatOllama(model="qwen3.5")
    ACTIVE_MODEL = "Local: Ollama (Qwen 3.5)"
    
elif os.environ.get("GITHUB_TOKEN"):
    llm_client = clt.ChatGithub(model="gpt-4o-mini")
    ACTIVE_MODEL = "Cloud: GitHub (GPT-4o-Mini)"
    
elif os.environ.get("ANTHROPIC_API_KEY"):
    llm_client = clt.ChatAnthropic(model="claude-haiku-4-5-20251001") 
    ACTIVE_MODEL = "Cloud: Anthropic (Claude Haiku 4.5)"

else:
    llm_client = None
    ACTIVE_MODEL = "NONE (No API keys or Local LLM found)"

# Print in terminal to see LLM successfully loaded
print(f"\n---> LLM Status: {ACTIVE_MODEL} <---\n")

# QueryChat Setup
# Read greeting
greeting_path = Path(__file__).parent / "greeting.md"
GREETING = greeting_path.read_text(encoding="utf-8")

# Read data description
data_desc_path = Path(__file__).parent / "data_desc.md"
DATA_DESC = data_desc_path.read_text(encoding="utf-8")

# Add drop-down dashboard description
dashboard_description = Path("src/dashboard_description.md").read_text(encoding="utf-8")

# Load full dataset for QueryChat (it needs pandas DataFrame)
df_for_querychat = education_table.execute()

# Only initialize QueryChat if we have a valid LLM client
if llm_client is not None:
    qc = QueryChat(
        df_for_querychat.copy(),
        "global_education",
        greeting=GREETING,
        data_description=DATA_DESC,
        client=llm_client,
    )
else:
    # Create a minimal placeholder - QueryChat tab won't work but app will load
    qc = None
    print("⚠️  Warning: QueryChat disabled - no LLM client configured")

# Refactor out functions for unit testing

def create_sex_completion_rate_df(d):
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

# ==========================================
#   UI DEFINITION
# ==========================================
app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.title("World Education Dashboard"),
        # Change the dashboard theme here
        ui.tags.style("""
            body {
                background: linear-gradient(180deg, #f8fbff 0%, #eef4f9 100%);
                color: #243447;
            }
        
            .card {
                border: none;
                border-radius: 16px;
                box-shadow: 0 6px 18px rgba(31, 59, 91, 0.10);
                background-color: #ffffff;
                overflow: hidden;
            }
        
            .card-header {
                background-color: #f7fbff !important;
                border-bottom: 1px solid #e6eef5 !important;
                font-weight: 600;
                color: #1f3b5b;
            }
        
            h2 {
                font-weight: 700;
                color: #1f3b5b;
                margin-bottom: 1rem;
            }
        
            .accordion-button {
                font-weight: 600;
                background-color: #f7fbff;
            }
        
            .accordion-body {
                background-color: #ffffff;
            }
        
            .form-check-input:checked {
                background-color: #4c78a8;
                border-color: #4c78a8;
            }
        
            .btn-outline-primary {
                border-radius: 10px;
            }
        
            .btn-outline-secondary {
                border-radius: 10px;
            }
        """)
    ),
    ui.navset_tab(
        # --- Tab 1: Main Dashboard ---
        ui.nav_panel(
            "Main Dashboard",
            ui.h2("World Education Dashboard"),
            ui.accordion(
                ui.accordion_panel(
                    "Click to learn more about this dashboard.",
                    ui.card(
                        ui.markdown(dashboard_description)
                    ),
                ),
                open=False
            ),
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
                        ),
                        ui.p(
                            "The selected regions apply to the map and KPI cards in the Overview tab, charts in the Completion & Literacy tab, and the table in the Data Table tab.",
                            class_="text-muted small mt-2"
                        ),
                    ),
                    width=300,
                ),
                ui.navset_tab(
                    ui.nav_panel(
                        "Overview",
                        ui.layout_columns(
                            ui.card(
                                ui.card_header("Global Education Indicators Map"),
                                ui.p(
                                    "Select a metric to map across the chosen regions. The region filter also updates the KPI cards.",
                                    class_="text-muted small"
                                ),
                                ui.input_select(
                                    "input_map_metric",
                                    "Map metric",
                                    map_metric_choices,
                                ),
                                output_widget("world_map"),
                            ),
                            ui.layout_column_wrap(
                                ui.output_ui("metric_average_box"),
                                ui.output_ui("metric_vs_world_box"),
                                ui.output_ui("metric_coverage_box"),
                                width=1,
                                fill=False,
                            ),
                            col_widths=(8, 4),
                        ),
                    ),
                    ui.nav_panel(
                        "Completion & Literacy",
                        ui.layout_column_wrap(
                            ui.card(
                                ui.card_header("Average Education Level by Region"),
                                ui.p(
                                    "Compare regional patterns in average education level",
                                    class_="text-muted small"
                                ),
                                output_widget("education_level_by_region_bar"),
                            ),
                            ui.card(
                                ui.card_header("Completion Rate Gap by Region"),
                                ui.p(
                                    "Compare regional patterns in completion rate gap between genders",
                                    class_="text-muted small"
                                ),
                                output_widget("completion_rate_gap_by_region_bar"),
                            ),
                            ui.card(
                                ui.card_header("Male vs Female Literacy Rate by Region"),
                                ui.p(
                                    "Compare regional patterns in gender disparities in literacy rates",
                                    class_="text-muted small"
                                ),
                                ui.div(
                                    output_widget("literacy_scatterplot"),
                                    ui.div(
                                        ui.output_text("literacy_coverage_note"),
                                        class_="text-muted small fst-italic mt-2"
                                    ),
                                ),
                                full_screen=True,
                            ),
                            width=1/3,
                        ),
                    ),
                    ui.nav_panel(
                        "Data Table",
                        ui.card(
                            ui.card_header("Data Table"),
                            ui.p(
                                "Inspect the filtered country-level data and choose which features to display",
                                class_="text-muted"
                            ),
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
        # --- Tab 2: Query with Chat ---
        ui.nav_panel(
            "Query with Chat",
            # Show actived model name into the header!
            ui.h2(f"AI-Powered Data Filtering (Powered by {ACTIVE_MODEL})"),
            ui.layout_sidebar(
                qc.sidebar() if qc else ui.sidebar(
                    ui.card(
                        ui.card_header("LLM Not Configured"),
                        ui.p("To use the Query with Chat feature, configure an LLM client in your .env file:"),
                        ui.tags.ul(
                            ui.tags.li("Set ANTHROPIC_API_KEY for Claude"),
                            ui.tags.li("Set GITHUB_TOKEN for GitHub Models"),
                            ui.tags.li("Set USE_LOCAL_LLM=true for Ollama"),
                        ),
                    )
                ),
                ui.layout_column_wrap(
                    ui.card(
                        ui.card_header(
                            ui.output_text("chat_title"),
                            ui.download_button("download_chat_data", "Download CSV", class_="btn-success btn-sm") if qc else ui.div(),
                                class_="d-flex justify-content-between align-items-center"
                        ),
                        ui.output_data_frame("chat_tbl"),
                    ),
                    ui.layout_column_wrap(
                        ui.card(
                            ui.card_header("Literacy Rate Scatterplot (Filtered)"),
                            output_widget("chat_scatter"),
                        ),
                        ui.card(
                            ui.card_header("Avg Education Level by Region (Filtered)"),
                            output_widget("chat_bar"),
                        ),
                        width=1/2
                    ),
                    width=1,
                    heights_equal="row"
                ),
                # Set layout to a fixed height,
                height="80vh" 
            )
        )
    ),
)

# ==========================================
#   SERVER LOGIC
# ==========================================
def server(input, output, session):    
    def toggle_region(region):
        """Toggle a region selection in the checkbox group.

        If the given region is currently selected, it is removed.
        Otherwise, it is added to the current selection.
    
        Parameters
        ----------
        region : str
            The name of the region to toggle.
    
        Returns
        -------
        None
        """
        current = list(input.input_region())
    
        if region in current:
            current.remove(region)
        else:
            current.append(region)
        
        ui.update_checkbox_group(
            "input_region",
            selected=current,
            session=session
        )

    # ----------------------------------------
    # TAB 1 LOGIC (Main Dashboard)
    # ----------------------------------------
    # 1) Get filtered ibis table (lazy - no data loaded yet)
    
    @reactive.Calc
    def filtered_table():
        """Apply region filters at the database level using ibis.
        
        Returns an ibis table expression (lazy - not executed until .execute() is called).
        All filtering happens before data enters memory.
        
        Returns
        -------
        ibis.Table
            Lazy ibis table expression with filters applied
        """
        table = education_table
        
        selected_regions = input.input_region()
        if selected_regions:
            table = table.filter(table["Region"].isin(selected_regions))
        else:
            table = table.filter(table["Region"] == "__NO_MATCH__")
    
        return table
    
    # 2) Materialize filtered data only when needed
    @reactive.Calc
    def filtered_df():
        """Execute the lazy query and return pandas DataFrame.
        
        This is called only when the data is actually needed for visualization.
        
        Returns
        -------
        pd.DataFrame
            The filtered world education dataframe
        """
        return filtered_table().execute()
        
    @render.text
    def literacy_coverage_note():
        d = filtered_df()
    
        if d.empty:
            return "Please select at least one region to display data."
    
        required_cols = [
            "Youth_15_24_Literacy_Rate_Male",
            "Youth_15_24_Literacy_Rate_Female",
        ]
    
        shown = d.dropna(subset=required_cols).shape[0]
        total = len(d)
    
        return f"Showing {shown} of {total} countries with available literacy data"
        
    @reactive.Calc
    def selected_metric():
        return input.input_map_metric()
    
    @reactive.Calc
    def filtered_metric_series():
        """Return non-missing values of the selected metric for filtered data.

        Returns
        -------
        pd.Series
            A pandas Series containing non-null values of the currently
            selected metric for the region-filtered dataset.
        """
        d = filtered_df()
        metric = selected_metric()
        return d[metric].dropna()
    
    @reactive.Calc
    def global_metric_series():
        """Get global metric values using lazy query."""
        metric = selected_metric()
        # Query only the needed column from the full dataset
        global_data = education_table.select(metric).execute()
        return global_data[metric].dropna()
    
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
    
        return create_sex_completion_rate_df(d)
    
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
        
    @reactive.Calc
    def no_region_selected():
        """Check whether no regions are currently selected.

        Returns
        -------
        bool
            True if no region is selected, otherwise False.
        """
        return len(input.input_region()) == 0

    # 3) Create object to display
    @output
    @render_widget
    def world_map():
        """Create interactive world map figure.

        Returns
        -------
        plotly.express.chorpleth
            Interactive world map figure.
        """
        if no_region_selected():
            fig = px.choropleth(title="Please select at least one region to display data")
            fig.update_layout(height=450)
            return fig

        d = filtered_df()
        metric = input.input_map_metric()
        clean_label = metric_label(metric)
        
        # DYNAMIC COLOR SCALE: Reverse the colors for negative metrics (OOSR)
        if metric.startswith("OOSR_"):
            map_colors = "viridis_r"  # Reversed: High is dark/blue, Low is bright/yellow
        else:
            map_colors = "viridis"

        fig = px.choropleth(
            d, 
            locations="iso3", 
            hover_name="Countries and areas",
            color=metric,
            color_continuous_scale=map_colors,
            projection="natural earth",
            labels={metric: clean_label}
        )

        fig.update_geos(
            showcoastlines=True,
            showcountries=True,
            showframe=False
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=90),
            height=450,
            coloraxis_colorbar=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.22,
                yanchor="top",
                len=0.75,
                thickness=14
            )
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
        if no_region_selected():
            fig = px.scatter(title="Please select at least one region to display data")
            return fig
            
        d = filtered_df()
        plot_df = d.dropna(subset=[
            "Youth_15_24_Literacy_Rate_Male",
            "Youth_15_24_Literacy_Rate_Female",
        ])
        
        if plot_df.empty:
            fig = px.scatter(title="No literacy data available for the selected region(s)").update_layout(title_font_size=12)
            return fig

        fig = px.scatter(
            plot_df,
            x="Youth_15_24_Literacy_Rate_Male",
            y="Youth_15_24_Literacy_Rate_Female",
            color="Region",
            hover_name="Countries and areas",
            custom_data=["Region"],
            color_discrete_map=region_color_map,
            category_orders={"Region": region_choices},
            labels={
                "Region": "Region",
                "Youth_15_24_Literacy_Rate_Male": " Male Literacy Rate (%)",
                "Youth_15_24_Literacy_Rate_Female": "Female Literacy Rate (%)",
            }
        )

        xy_min = plot_df[["Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female"]].min().min() - 5
        xy_max = plot_df[["Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female"]].max().max() + 5

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
        fig.update_traces(marker_size=8) # make marker point size larger

        return fig

    @reactive.effect
    def _capture_scatter_click():
        fig = literacy_scatterplot.widget
        if fig is None:
            return
    
        for trace in fig.data:
            trace._click_callbacks.clear()
    
            def handle_click(trace, points, state):
                if not points.point_inds:
                    return
                if trace.customdata is None:
                    return
            
                idx = points.point_inds[0]
                region = trace.customdata[idx][0]
                toggle_region(region)
    
            trace.on_click(handle_click)
        
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
        if d.empty:
            return render.DataGrid(
                pd.DataFrame({"Message": ["Please select at least one region to display data"]}),
                selection_mode="none",
                height="300px"
            )
            
        selected_cols = input.input_table_features()
    
        if not selected_cols:
            selected_cols = list(d.columns)
    
        cols = [c for c in selected_cols if c in d.columns]
        
        # Filter to only show the selected columns
        d_display = d[cols].copy()
        
        # Identify which columns are numeric/data columns (not identifiers)
        # We want to filter based on these, not on Country/Region names
        identifier_cols = ["Countries and areas", "Region", "iso3"]
        data_cols = [c for c in cols if c not in identifier_cols]
        
        # Drop rows where ALL data columns are empty/null
        # This keeps rows that have at least one non-null value in the data columns
        if data_cols:  # Only filter if there are data columns selected
            d_display = d_display.dropna(subset=data_cols, how='all')
        
        # Optional: Drop rows where ANY data column is empty/null
        # Uncomment the line below if you want stricter filtering
        # if data_cols:
        #     d_display = d_display.dropna(subset=data_cols, how='any')
    
        return render.DataGrid(
            d_display,
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
        if no_region_selected():
            fig = px.bar(title="Please select at least one region to display data").update_layout(title_font_size=12)
            return fig
            
        d = completion_gap_by_region_df()
    
        fig = px.bar(
            d,
            x="Education_Level",
            y="Completion_Rate_Gap",
            color="Region",
            custom_data=["Region"],
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

        # ADD THESE TWO LINES: Vertical separators between categories
        fig.add_vline(x=0.5, line_width=1, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=1.5, line_width=1, line_dash="dash", line_color="gray", opacity=0.5)

        fig.update_yaxes(dtick=2)
    
        return fig
        
    @reactive.effect
    def _capture_gap_bar_click():
        fig = completion_rate_gap_by_region_bar.widget
        if fig is None:
            return
    
        for trace in fig.data:
            trace._click_callbacks.clear()
    
            def handle_click(trace, points, state):
                if not points.point_inds:
                    return
                if trace.customdata is None:
                    return
            
                idx = points.point_inds[0]
                region = trace.customdata[idx][0]
                toggle_region(region)
    
            trace.on_click(handle_click)
    
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
        if no_region_selected():
            fig = px.bar(title="Please select at least one region to display data")
            return fig
            
        d = region_completion_rate_df()
    
        fig = px.bar(
            d,
            x="Education_Level",
            y="Completion_Rate",
            color="Region",
            custom_data=["Region"],
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

        # ADD THESE TWO LINES: Vertical separators between categories
        fig.add_vline(x=0.5, line_width=1, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=1.5, line_width=1, line_dash="dash", line_color="gray", opacity=0.5)
    
        fig.update_yaxes(dtick=20)
    
        return fig

    @reactive.effect
    def _capture_completion_bar_click():
        fig = education_level_by_region_bar.widget
        if fig is None:
            return
    
        for trace in fig.data:
            trace._click_callbacks.clear()
    
            def handle_click(trace, points, state):
                if not points.point_inds:
                    return
                if trace.customdata is None:
                    return
            
                idx = points.point_inds[0]
                region = trace.customdata[idx][0]
                toggle_region(region)
    
            trace.on_click(handle_click)
    
    # KPI 1
    @render.ui
    def metric_average_box():
        metric = selected_metric()
        label = metric_label(metric)
        values = filtered_metric_series()
    
        if len(values) == 0:
            return ui.value_box(
                f"Average: {label}",
                "No data",
                theme="secondary"
            )
    
        avg_value = values.mean()
    
        return ui.value_box(
            f"Average: {label}",
            f"{avg_value:.1f}",
            ui.HTML("<strong style='opacity:0.9'>Across selected regions</strong>"),
            theme="primary"
        )
    #KPI Card 2
    @render.ui
    def metric_vs_world_box():
        metric = selected_metric()
        label = metric_label(metric)
        filtered_values = filtered_metric_series()
        global_values = global_metric_series()
    
        if len(filtered_values) == 0 or len(global_values) == 0:
            return ui.value_box(
                f"Vs world average: {label}",
                "No data",
                theme="secondary"
            )
    
        filtered_avg = filtered_values.mean()
        global_avg = global_values.mean()
        diff = filtered_avg - global_avg
    
        if diff >= 0:
            caption = f"{diff:.1f} above world average ({global_avg:.1f})"
        else:
            caption = f"{-diff:.1f} below world average ({global_avg:.1f})"
    
        theme = "success" if abs(diff) < 1 else "warning"
    
        return ui.value_box(
            f"Vs world average: {label}",
            f"{diff:+.1f}",
            ui.HTML(f"<strong style='opacity:0.9'>{caption}</strong>"),
            theme=theme
        )
    # KPI Card 3
    @render.ui
    def metric_coverage_box():
        metric = selected_metric()
        label = metric_label(metric)
        d = filtered_df()
    
        n_available = d[metric].notna().sum()
        n_total = len(d)
    
        if n_total == 0:
            return ui.value_box(
                f"Data coverage: {label}",
                "No data",
                theme="secondary"
            )
    
        pct = 100 * n_available / n_total
    
        return ui.value_box(
            f"Data coverage: {label}",
            f"{n_available}/{n_total}",
            ui.HTML(f"<strong style='opacity:0.9'>{pct:.0f}% of selected countries have data</strong>"),
            theme="info"
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
            selected=[],
            session=session
        )

    # ----------------------------------------
    # TAB 2 LOGIC (QueryChat)
    # ----------------------------------------
    if qc is not None:
        qc_vals = qc.server()

        @render.text
        def chat_title():
            return qc_vals.title() or "Global Education Dataset"

        @output
        @render.data_frame
        def chat_tbl():
            d = qc_vals.df()

            # Drop the unwanted index column
            d = d.drop(columns=["Unnamed: 0"], errors="ignore")
            
            # Define categorical columns
            cat_cols = ["Countries and areas", "Region", "iso3"]
            
            # Grab all the remaining numerical columns
            num_cols = [c for c in d.columns if c not in cat_cols]
            
            # Combine the lists to create final display order
            final_order = cat_cols + num_cols

            # Apply the order to the dataframe
            valid_cols = [c for c in final_order if c in d.columns]
            
            return render.DataGrid(
                d[valid_cols], 
                selection_mode="rows", 
                height="250px"
            )
    else:
        # Placeholder functions when QueryChat is not available
        @render.text
        def chat_title():
            return "LLM Not Configured"

        @output
        @render.data_frame
        def chat_tbl():
            return render.DataGrid(
                pd.DataFrame({"Message": ["Configure an LLM client to use this feature"]}),
                height="250px"
            )

    # Chat plots - work for both cases
    @output
    @render_plotly
    def chat_scatter():
        """
        Create scatterplot of male vs female literacy rates by region,
        and filtered by user feed AI commands.

        Parameters
        ----------
        None

        Returns
        -------
        plotly.express.scatter
            Scatterplot of male vs female literacy rate by region.
        """
        if qc is None:
            return px.scatter(title="LLM Not Configured")
            
        d = qc_vals.df()
        if d.empty:
            return px.scatter(title="No Data Available for this query")
            
        fig = px.scatter(
            d, 
            x="Youth_15_24_Literacy_Rate_Male", 
            y="Youth_15_24_Literacy_Rate_Female",
            color="Region", 
            hover_name="Countries and areas", 
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={
                "Region": "Region", 
                "Youth_15_24_Literacy_Rate_Male": " Male Literacy Rate (%)", 
                "Youth_15_24_Literacy_Rate_Female": "Female Literacy Rate (%)"
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

        fig.update_traces(marker_size=8) # make marker point size larger

        return fig

    @output
    @render_plotly
    def chat_bar():
        """
        Create bar plot of education level completed separated by region,
        and filtered by user feed AI command.

        Parameters
        ----------
        None

        Returns
        -------
        px.bar
            Plotly express bar plot object.
        """
        if qc is None:
            return px.bar(title="LLM Not Configured")
            
        d = qc_vals.df()
        if d.empty:
            return px.bar(title="No Data Available for this query")
            
        d_melt = d[[
            "Completion_Avg_Primary", 
            "Completion_Avg_Lower_Secondary",
            "Completion_Avg_Upper_Secondary", 
            "Region", 
            "iso3"
        ]].copy()
        
        d_melt = pd.melt(
            d_melt, 
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
        d_melt["Education_Level"] = d_melt["Completion_Rate_Group"].str.split("_").str[2:].str.join(" ")
        
        d_grouped = d_melt[["Region", "Education_Level", "Completion_Rate"]].groupby(["Region", "Education_Level"]).mean().reset_index()

        fig = px.bar(
            d_grouped, 
            x="Education_Level", 
            y="Completion_Rate", 
            color="Region",
            color_discrete_sequence=px.colors.qualitative.Set2, barmode="group",
            category_orders={"Education_Level": ["Primary", "Lower Secondary", "Upper Secondary"]},
            labels={"Education_Level": "Education Level", "Completion_Rate": "Completion Rate (%)"},
            range_y=[0,100]
        )

        return fig

    if qc is not None:
        @render.download(filename="global_education_filtered.csv")
        def download_chat_data():
            yield qc_vals.df().to_csv(index=False).encode("utf-8")


app = App(app_ui, server)
