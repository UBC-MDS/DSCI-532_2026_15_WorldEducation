# **Global Education Metrics**

This dashboard explores **global education indicators** across world regions using data from international education datasets in 2021. It allows users to compare patterns in **education access, completion, and literacy outcomes** across countries. It addresses the challenge of making sense of complex global education data by providing an interactive visualization tool that enables users to:

- Explore education indicators across 202 countries
- Compare regional performance and identify disparities
- Analyze gender gaps in education access and completion
- Make data-driven decisions to improve education systems globally

#### How to use this dashboard

**Region filter (left sidebar)**
- Select one or more regions to update all charts, the map, and the data table.

**Overview tab**
- Explore a **world map of education indicators** by selecting different metrics.
- KPI cards summarize the average values, global comparison, and data coverage for the selected regions.

**Completion & Literacy tab**
- Compare regional patterns in:
  - average education completion levels
  - gender gaps in completion rates
  - male vs female youth literacy rates
- Click bars or scatterplot points to update the region selection.

**Data Table tab**
- Inspect the filtered **country-level dataset**.
- Choose which variables to display using the feature selector.

**Query with Chat**:
- Supports Anthropic, local Ollama, or GitHub-backed LLM; 
- Anthropic by default on Posit Connect, and optional setup via `.env` if your run the app locally.
- Use natural language to explore the dataset with an AI assistant.
- Ask questions like *"Show countries in Asia with high literacy rates"* to filter and visualize the data interactively.

## Limitations for this data set

- This data is only a snapshot of different metrics for countries with only single year record of 2021, so there is no year level filter/trend.
- Some indicators are **not available for all countries**, so certain charts may display fewer observations depending on the selected metric or region, and the filter and plots are delivered primarily by regional level of detail but not country level of detail.

**Original data can be accessed via this [link to Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/world-educational-data/data).**


