# World Education Dashboard

## Motivation

Education systems vary dramatically across the world, and understanding which factors contribute to better educational outcomes is crucial for policymakers, researchers, and educators. This dashboard addresses the challenge of making sense of complex global education data by providing an interactive visualization tool that enables users to:

- Explore education indicators across 202 countries
- Compare regional performance and identify disparities
- Analyze gender gaps in education access and completion
- Make data-driven decisions to improve education systems globally

The dashboard leverages data from UNESCO Institute for Statistics, UNICEF, and UN Statistics Division to provide comprehensive insights into global education patterns.

## Demo

![Dashboard Demo](img/demo.gif)

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

## Live Dashboard

Access the deployed dashboard here:

- [World Education Dashboard (Production)](https://sapolraadnui-worldeducation.share.connect.posit.cloud)
- [World Education Dashboard (Development)](https://sapolraadnui-worldeducation-dev.share.connect.posit.cloud/)

## For Contributors

### Installation

#### Option 1: Using Conda (Recommended)

```bash
# Clone the repository
git clone https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation.git
cd DSCI-532_2026_15_WorldEducation

# Create and activate the conda environment
conda env create -f environment.yml
conda activate 532
```

#### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/UBC-MDS/DSCI-532_2026_15_WorldEducation.git
cd DSCI-532_2026_15_WorldEducation

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App Locally

```bash
# Make sure you're in the project root directory
# Run the Shiny app
shiny run src/app.py
```

The dashboard will be available at `http://localhost:8000` (or the port shown in your terminal).

**Optional — AI (Query with Chat) tab:** To use the "Query with Chat" tab, create a `.env` file in the project root with one of the following: `ANTHROPIC_API_KEY=your_key` for Anthropic, `USE_LOCAL_LLM=true` for a local Ollama instance, or `GITHUB_TOKEN=your_token` for a GitHub-backed LLM. Without any of these, the app runs normally but the chat tab will not have an active model.

### Project Structure

```
.
├── data/
│   ├── raw/                    # Original dataset
│   └── processed/              # Processed data for the app
├── notebooks/                  # Exploratory data analysis
├── src/
│   ├── app.py                  # Main Shiny application
│   ├── process_data.py         # Data processing scripts
│   ├── greeting.md             # Chat assistant greeting and suggestions
│   └── data_desc.md            # Data description for the AI chat (row-filtering only)
├── report/                     # Project documentation and specs
├── img/                        # Images and demo files
├── requirements.txt            # Python dependencies
├── environment.yml            # Conda environment specification
├── .env                        # Optional: API keys for Query with Chat (not in repo)
└── README.md                   # This file
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Data Source

The dataset is sourced from [Kaggle - World Educational Data](https://www.kaggle.com/datasets/nelgiriyewithana/world-educational-data/data), compiled from UNESCO Institute for Statistics, UNICEF, and UN Statistics Division.

## License

See [LICENSE](LICENSE) for details.

## Team

See [team.txt](team.txt) for team member information.


