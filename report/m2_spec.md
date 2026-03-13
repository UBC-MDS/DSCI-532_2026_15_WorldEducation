## Phase 2: App Specification (`reports/m2_spec.md`)

### 2.1 Updated Job Stories

| #   | Job Story                                                                                                                                                   | Status         | Notes                                                              |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------ |
| 1   | When I am evaluating the overall performance of education systems across countries, I want to compare key education indicators such as completion rates and literacy rates across regions, so I can identify which regions are lagging behind and require targeted policy attention.     | 🔄 Revised | Due to complexity of comparing between countries, we decided to limit it to regional filtering instead (continent level). This is supported through region filtering, literacy scatter plot, completion bar chart, and output data table.|
| 2   | When designing policies to bridge gender inequality in education, I want to compare different education variables separately for male and female students across different education levels, so I can identify gender-based disparities and design policies that promote equal access to education.                | 🔄 Revised | We narrowed this down to focus on completion rates and literacy rates. Also, we added KPI cards to reflect disparities from genders more clearly.   |
| 3   | When I am reviewing large-scale global education data, I want to visualize education indicators on a choropleth, so I can quickly detect global patterns, trends, and outlier countries that require further investigation or policy intervention.   | ✅ Implemented | Fully implemented. What could be implement in milestone 3 would be color scaling options and map-based filtering interactions if time allows. |

### 2.2 Component Inventory

| ID | Type | Shiny widget / renderer | Depends on | Job story |
|----|------|--------------------------|------------|-----------|
| `input_region` | Input | `ui.input_checkbox_group()` | — | #1, #2, #3 |
| `apply_filters` | Input | `ui.input_action_button("Apply Filters")` | — | #1, #2, #3 |
| `input_map_metric` | Input | `ui.input_select()` (grouped by theme) | — | #3 |
| `processed_df` | Reactive calc | `@reactive.Calc` | — | #1, #2, #3 |
| `filtered_df` | Reactive calc | `@reactive.Calc` + `@reactive.event(input.apply_filters)` | `processed_df`, `input_region`, `apply_filters` | #1, #2, #3 |
| `sex_completion_rate_df` | Reactive calc | `@reactive.Calc` (melt + group mean by Sex & Education_Level) | `filtered_df` | #1, #2 |
| `world_map` | Output | `@render_widget` (Plotly choropleth) | `filtered_df`, `input_map_metric` | #3 |
| `literacy_scatterplot` | Output | `@render_plotly` (scatter plot) | `filtered_df` | #1, #2 |
| `education_level_by_gender_bar` | Output | `@render_plotly` (grouped bar chart) | `sex_completion_rate_df` | #1, #2 |
| `elementary_completion_box` | Output | `@render.ui` (value_box KPI) | `sex_completion_rate_df` | #1, #2 |
| `el_completion_rate_gender_difference_box` | Output | `@render.ui` (value_box KPI) | `sex_completion_rate_df` | #2 |
| `tbl` | Output | `@render.data_frame` (DataGrid) | `filtered_df`, `input_map_metric` | #1, #2, #3 |

### 2.3 Reactivity Diagram

```mermaid
flowchart TD
    A[input_region] --> C{{filtered_df}}
    B[apply_filters] --> C
    D{{processed_df}} --> C

    C --> E{{sex_completion_rate_df}}

    F[input_map_metric] --> G([world_map])
    C --> G

    C --> H([literacy_scatterplot])

    E --> I([education_level_by_gender_bar])
    E --> J([elementary_completion_box])
    E --> K([el_completion_rate_gender_difference_box])

    F --> L([tbl])
    C --> L
```

### 2.4 Calculation Details

1.  **processed_df**

	•	Inputs: none (uses the globally loaded df)

	•	Transformation: returns a copy of the processed dataset (df.copy()), no additional derived columns created in this step in the current code.

	•	Consumed by: filtered_df

3.  **filtered_df**

	•	Inputs: processed_df, input_region, and event trigger apply_filters

	•	Transformation: on clicking “Apply Filters”, filters rows to Region values selected in input_region. If no regions selected, returns the unfiltered dataset.

	•	Consumed by: world_map, literacy_scatterplot, tbl, sex_completion_rate_df

5.  **sex_completion_rate_df**

	•	Inputs: filtered_df

	•	Transformation: selects completion rate columns by sex and education level, melts into long format, extracts Sex and Education_Level, and groups by (Sex, Education_Level) and computes mean completion rate

	•	Consumed by: education_level_by_gender_bar, elementary_completion_box, el_completion_rate_gender_difference_box

### Testing

- 4 tests will be added
  - 1 unit test
    - This test will confirm that the dataframe operations need to achieve the correct data format for the bar chart that shows education level completion by gender is correctly done. This test is needed otherwise the displayed data may not be accurate.
  - 3 full app tests
    - Test that the displayed dataframe has the correct size. This test is needed to ensure the loaded data is correct and therefore the data for all plots has the correct starting starting point. Without this test we can't be sure any of the displayed plots are correct.
    - Test that the regional filters are operating correctly. Without this a user may believe they are observing region specific data but actually are not.
    - Test the reset filter button. Without this test we can't be sure users are able to reset the dashboard. They may believe they are looking at unfiltered data but are not.