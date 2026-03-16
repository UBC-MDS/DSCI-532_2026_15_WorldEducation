
## App Specification (`reports/m4_spec.md`)

### 2.1 Updated Job Stories

| # | Job Story | Status | Notes |
|---|---|---|---|
| 1 | When I am evaluating the overall performance of education systems across countries, I want to compare key education indicators such as completion rates and literacy rates across regions, so I can identify which regions are lagging behind and require targeted policy attention. | ✅ Implemented | Implemented through region filtering, interactive bar charts and scatterplot, KPI cards, choropleth map, and data table. Users can also click chart elements to update selected regions. |
| 2 | When designing policies to bridge gender inequality in education, I want to compare different education variables separately for male and female students across different education levels, so I can identify gender-based disparities and design policies that promote equal access to education. | 🔄 Revised | Scoped to focus on literacy and completion indicators. Gender disparities are reflected through the literacy scatterplot and completion gap by region bar chart rather than a full male/female breakdown for every variable. |
| 3 | When I am reviewing large-scale global education data, I want to visualize education indicators on a choropleth, so I can quickly detect global patterns, trends, and outlier countries that require further investigation or policy intervention. | ✅ Implemented | Implemented with a choropleth map, grouped metric selector, KPI cards, and data coverage summaries. The map updates based on selected regions and selected metric. |
| 4 | When I am exploring regional patterns in education, I want to click on chart elements directly and have the rest of the dashboard update automatically, so I can interactively refine my analysis without relying only on sidebar filters. | ✅ Implemented | Advanced feature (Option D). Clicking bars or scatterplot points toggles region selection and updates the rest of the dashboard. Empty-state handling is included when no regions are selected. |

### 2.2 Component Inventory

| ID | Type | Shiny widget / renderer | Depends on | Job story |
|---|---|---|---|---|
| `input_region` | Input | `ui.input_checkbox_group()` | — | #1, #2, #3, #4 |
| `select_all_regions` | Input | `ui.input_action_button()` | — | #1, #3, #4 |
| `reset_regions` | Input | `ui.input_action_button()` | — | #1, #3, #4 |
| `input_map_metric` | Input | `ui.input_select()` | — | #3 |
| `input_table_features` | Input | `ui.input_selectize()` | — | #1, #3 |
| `filtered_table` | Reactive calc | `@reactive.Calc` | `education_table`, `input_region` | #1, #2, #3, #4 |
| `filtered_df` | Reactive calc | `@reactive.Calc` | `filtered_table` | #1, #2, #3, #4 |
| `selected_metric` | Reactive calc | `@reactive.Calc` | `input_map_metric` | #3 |
| `filtered_metric_series` | Reactive calc | `@reactive.Calc` | `filtered_df`, `selected_metric` | #3 |
| `global_metric_series` | Reactive calc | `@reactive.Calc` | `education_table`, `selected_metric` | #3 |
| `region_completion_rate_df` | Reactive calc | `@reactive.Calc` | `filtered_df` | #1, #2 |
| `completion_gap_by_region_df` | Reactive calc | `@reactive.Calc` | `filtered_df` | #2 |
| `no_region_selected` | Reactive calc | `@reactive.Calc` | `input_region` | #1, #3, #4 |
| `world_map` | Output | `@render_widget` | `filtered_df`, `input_map_metric` | #3, #4 |
| `literacy_scatterplot` | Output | `@render_plotly` | `filtered_df` | #1, #2, #4 |
| `completion_rate_gap_by_region_bar` | Output | `@render_plotly` | `completion_gap_by_region_df` | #2, #4 |
| `education_level_by_region_bar` | Output | `@render_plotly` | `region_completion_rate_df` | #1, #4 |
| `metric_average_box` | Output | `@render.ui` | `filtered_metric_series` | #3 |
| `metric_vs_world_box` | Output | `@render.ui` | `filtered_metric_series`, `global_metric_series` | #3 |
| `metric_coverage_box` | Output | `@render.ui` | `filtered_df` | #3 |
| `literacy_coverage_note` | Output | `@render.text` | `filtered_df` | #2 |
| `tbl` | Output | `@render.data_frame` | `filtered_df`, `input_table_features` | #1, #3, #4 |