# **Global Education Metrics**

This dashboard addresses the challenge of making sense of complex global education data by providing an interactive visualization tool that enables users to:

- Explore education indicators across 202 countries
- Compare regional performance and identify disparities
- Analyze gender gaps in education access and completion
- Make data-driven decisions to improve education systems globally

## Features

The dashboard is organized into two main tabs:

**Main Dashboard** (with sub-tabs):

- **Overview**: Interactive world map (choropleth) for any selected education metric; KPI cards that update to match the chosen map metric (average, vs world, coverage)
- **Completion & Literacy**: Education level by region bar chart; completion rate gap by region; male vs female literacy scatter by region
- **Data Table**: Country-level data with configurable columns, filtered by selected regions

**Query with Chat**:

- AI-powered row filtering of the dataset (e.g., “Show only Asian countries”, “Filter to regions with Primary Completion above 90%”). Supports Anthropic, local Ollama, or GitHub-backed LLM; optional setup via `.env`.

Additional capabilities:

- **Regional Filtering**: Focus on specific continents; filters apply to map, KPIs, charts, and table
- **Map Metric Selection**: Choose from grouped metrics (Access, Completion, Learning, Context) for the choropleth
- **KPI Cards**: Reflect the currently selected map metric for quick context

## Limitations for this data set

- This data is only a snapshot of different metrics for each country without multiple years of records, so there is no year level filter/trend.
- There are missing data across some metrics and countries including developing and developed countries, so the filter and plots are delivered by regional level of detail but not country level of detail.

**Original data can be accessed via this [link to Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/world-educational-data/data).**


