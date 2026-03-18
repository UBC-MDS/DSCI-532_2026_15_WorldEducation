# Changelog

All notable changes to the World Education Dashboard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0](https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.4.0) - 2026-03-17

### Added

- Unit test and whole app test with `playwright` (`#72`)
- Interactive click has been implemented as the advanced feature. Users can click regions to deselect regions (`#77`)
- Added a drop-down dashboard description in main page, and included the year of the data in the dashboard description. (`#68`,`#69`,`#77`)
- DuckDB lazy loading via Ibis + Parquet, replacing eager pandas CSV loading (`#73`)
- `convert_to_parquet.py` script to convert processed CSV to Parquet format (`#73`)
- Updated demo gif to reflect M4 changes

### Changed
- Dashboard theme (`#77`)
- Data loading pipeline migrated from pandas CSV to Ibis + DuckDB backed by Parquet for lazy evaluation — all filtering now happens at the database level before data enters memory (`#73`)
- World map out of school metrics has reversed color representation, so positive meanings are in yellow (out of school metrics when low, other metrics when high), and negative meanings are in blue (out of school metrics when high, other metrics when low) (`#70`).
- Scatter plot data points display size has increased. (`#70`).
- Bar plots have vertical dash lines to separate categories for easier read. (`#69`).
- Data table drop-down menu added metric grouping so viewers can select metrics in an organized way (`#70`).

### Fixed
- "Select All" and "Reset" filters now have different functions. Reset is now set to no regions selected. (`#68`,`#71`,`#77`)
- **Feature prioritization issue link:** (`#63`).

### Known Issues

- No known issues at the time of this release.

### Release Highlight: Interactive region selection (Component Click Event Interaction)

This dashboard focuses on regional comparison, so Option D was chosen to make exploration more interactive. Instead of relying solely on the sidebar filters on the left, users can now click regions directly in the bar charts or scatterplot. Once they click them, these regions are excluded from all the plots and table.
- **Option chosen:** D (Component Click Event Interaction)
- **PR:** (`#77`).
- **Why this option over the others:** We have chosen this option since the other options were too complex to be implemented and were not as useful as option D where users could click on the plots to filter out regions. Therefore, we have decided to implement option D since it was the most useful for users.
- **Feature prioritization issue link:** (`#63`).

### Collaboration

<!-- Summary of workflow or collaboration improvements made since M3. -->

- **CONTRIBUTING.md:** (`#82`).
- **M3 retrospective:** After M3 feedback, we recognized that although the team was effective at dividing work and completing features on time, our workflow still had some weaknesses. In particular, PRs were often too large, review quality varied, documentation was not always updated alongside implementation, and responsibilities around releases and submissions were not always clearly communicated. We also noticed that coding and writing contributions were somewhat uneven across team members.
- **M4:** This milestone, we focused on improving collaboration by aiming for smaller and more manageable PRs, requiring at least one meaningful review before merging, and making sure reviewers were ideally not the feature author. We also committed to updating specifications before or alongside coding, writing clearer PR descriptions, and checking in more frequently to keep responsibilities and progress aligned.

### Reflections

- Testing

Four tests were added. One unit test to  confirm that the dataframe operations need to achieve the correct data format for the bar chart that shows education level completion by gender is correctly done. This test is needed otherwise the displayed data may not be accurate. And three full app tests. 1) Test that the displayed dataframe has the correct size. This test is needed to ensure the loaded data is correct and therefore the data for all plots has the correct starting starting point. Without this test we can't be sure any of the displayed plots are correct. 2) Test that the regional filters are operating correctly. Without this a user may believe they are observing region specific data but actually are not. 3) Test the reset filter button. Without this test we can't be sure users are able to reset the dashboard. They may believe they are looking at unfiltered data but are not.

- What the dashboard does well: The region-based design keeps the analysis focused and easy to interpret. The coordinated views including the choropleth map, KPI cards, bar charts, scatterplot, and data table work together to provide both high-level summaries and detailed exploration. The addition of interactive filtering (clicking on charts to update selected regions) makes the workflow more intuitive and supports exploratory analysis without relying solely on sidebar controls. The use of Ibis for lazy loading also improves performance when working with the full dataset.

- Current Limitations: While the dashboard is interactive, some charts still overlap in the insights they provide. Also, the comparison can only be done on regional level, instead of country level. 

- Tradeoffs: Priority was given to implementing the advanced interactive filtering (click-based selection across charts) and ensuring consistent reactivity across all components. This meant less time was available for refining visual differentiation between charts and improving the integration of the AI Assistant.

- Most useful:
The Shiny reactivity model and lecture materials were particularly helpful for structuring the dashboard logic, especially when implementing linked interactions across multiple components. The AI Assistant resources were also valuable in enabling the integration of the QueryChat feature, even though further refinement is still needed to fully align it with the dashboard’s analytical flow.


## [0.3.0](https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.3.0) - 2026-03-08

### Added

- Tabbed layout: Overview, Completion & Literacy, and Data Table under Main Dashboard (`#48`, `#52`).
- "Query with Chat" tab with AI-powered data filtering (QueryChat + Chatlas; Anthropic, Ollama, GitHub) (`#53`).
- Education level by region bar chart and completion rate gap by region bar chart (`#50`, `#52`).
- KPI cards that update to reflect the selected map metric (`#52`).
- Data description and greeting content for the chat assistant (`#53`).
- Website title "World Education Dashboard" in the UI (`#40`).
- Shiny 1.5.1, anthropic, querychat, chatlas, python-dotenv in requirements and environment (`#54`, `#53`).

### Changed

- Bar chart changed from completion by gender/level to completion rate gap by region (`#52`, `#50`).
- Filters cleaned up; region filter applies consistently to map, KPIs, charts, and table; filter rule to avoid dropping columns (`#52`).
- Map metric selector moved into the Overview tab (`#52`).
- Literacy plot renamed, formatting improved (colors, ticks), dynamic axis range, and % on axis label (`#50`).
- KPI card wording updated (`#50`).

### Fixed

- Anthropic API key handling in the app (`#54`, `#55`).
- Extra nav panel lines in the UI (`#53`).
- Minor typo and package/environment setup for LLM (`#53`).

### Known Issues

- Data description for the chat may be loaded from the wrong file (greeting.md vs data_desc.md) in app.py — verify and fix if intentional.

### Reflection

The dashboard now delivers on all three job stories with a cleaner, more structured interface. The tabbed layout (Overview, Completion & Literacy, Data Table) keeps the user experience focused and reduces cognitive load compared to the single-page M2 design. The new AI-powered "Query with Chat" tab is a significant addition, enabling natural-language row filtering for users who want to explore the data beyond the predefined filters. The dynamic KPI cards and improved chart formatting (color consistency, axis labels, dynamic ranges) make the dashboard more polished and informative.

Current limitations include the lack of time-series data, all indicators represent a single snapshot in time, which restricts trend analysis. The AI chat is constrained to row filtering only and cannot generate new visualizations or perform statistical analysis. The choropleth map relies on exact country name matching with Plotly, which may silently drop some countries. Planned improvements include fixing the data description file path for the chat assistant, adding tooltips to charts, and exploring a year-over-year comparison if data permits. No intentional deviations from DSCI 531 visualization best practices were made in this milestone.

## [0.2.0](https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.2.0) - 2026-02-28

### Added

- Interactive choropleth world map for visualizing education indicators globally
- Regional filtering by continent with "Apply Filters" button
- Literacy rate scatter plot for comparing male and female youth literacy
- Completion rate bar chart grouped by gender and education level
- KPI cards showing elementary completion rates and gender differences
- Data table with filtered results for detailed inspection
- Grouped metric selection for map visualization (by education theme)

### Changed

- Narrowed gender comparison focus to completion rates and literacy rates
- Limited country comparison to regional filtering at continent level for reduced complexity

### Fixed

- No bugs were resolved in this release.

### Known Issues

- No known issues at the time of this release.

### Reflection

#### Job Story Implementation Status

**Job Story #1** (Regional comparison of education indicators): **Fully Implemented**

- Regional filtering allows users to focus on specific continents
- Literacy scatter plot enables comparison across regions
- Completion bar chart shows performance by education level
- Data table provides detailed country-level inspection
- Users can successfully identify lagging regions requiring policy attention

**Job Story #2** (Gender inequality analysis): **Fully Implemented**

- Completion rates are visualized separately for male and female students across education levels
- Literacy scatter plot compares male vs. female youth literacy rates
- KPI cards highlight gender disparities in elementary completion rates
- Users can identify gender-based gaps and design targeted policies

**Job Story #3** (Global pattern visualization): **Fully Implemented**

- Choropleth map displays education indicators across all countries
- Color-coded visualization enables quick identification of patterns and outliers
- Grouped metric selection allows exploration of different education themes
- Users can detect global trends requiring further investigation

#### Layout Comparison

The final implementation closely follows the M1 sketch and M2 spec with the following alignment:

- **Map placement**: Choropleth map positioned prominently at the top as designed
- **Filter panel**: Regional filters implemented on the left side as specified
- **Comparative visualizations**: Scatter plot and bar chart placed below the map for deeper analysis
- **Data table**: Scrollable table included at the bottom for transparency
- **KPI cards**: Added to provide quick insights into key metrics and gender disparities

All components from the M2 spec component inventory have been implemented, and the reactivity diagram accurately reflects the final application structure.

## [0.1.0](https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.1.0) - 2026-02-14

### Added

- Initial project setup and repository structure
- Data processing pipeline for Global Education dataset from Kaggle
- Exploratory Data Analysis (EDA) notebook
- Project proposal (m1_proposal.md) with motivation, data description, and usage scenarios
- App specification (m2_spec.md) with component inventory and reactivity diagram
- Basic dashboard sketch and design mockups
- Dataset with 202 countries and 29 education-related variables
- Support for analyzing out-of-school rates, completion rates, proficiency levels, literacy rates, and enrollment figures

### Documentation

- README with project overview and dashboard links
- CODE_OF_CONDUCT.md
- CONTRIBUTING.md
- LICENSE
- Team information

[0.3.0]: https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.3.0
[0.2.0]: https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.2.0
[0.1.0]: https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.1.0
