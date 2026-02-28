# Changelog

All notable changes to the World Education Dashboard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-28

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

- [Document any bugs or issues that were resolved in this release]

### Known Issues

- [Document any known limitations or bugs that still exist]

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

## [0.1.0] - 2026-02-14

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

[0.2.0]: https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.2.0
[0.1.0]: https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation/releases/tag/v0.1.0
