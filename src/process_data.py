
import pandas as pd
import numpy as np

# Fix country naming inconsistencies
FIXES = {
    "The Bahamas": "Bahamas",
    "The Gambia": "Gambia",
    "Republic of the Congo": "Congo",
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
    "Ivory Coast": "Côte d'Ivoire",
    "Republic of Ireland": "Ireland",
    "East Timor": "Timor-Leste",
    "Federated States of Micronesia": "Micronesia, Federated States of",
    "Russia": "Russian Federation",
    "Iran": "Iran, Islamic Republic of",
    "Laos": "Lao People's Democratic Republic",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Vatican City": "Holy See (Vatican City State)",
    "Cape Verde": "Cabo Verde",
    "Palestinian National Authority": "Palestine, State of",
    "Moldova": "Moldova, Republic of",
    "Syria": "Syrian Arab Republic",
    "Tanzania": "Tanzania, United Republic of",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Bolivia": "Bolivia, Plurinational State of",
    "Vietnam": "Viet Nam",
    "Guinea0Bissau": "Guinea-Bissau",
    "Sï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿": "São Tomé and Príncipe",
    "Turkey": "Türkiye"
}

# Get iso3 for plotting
def to_iso3(name):
    """
    Convert data from "Countries and areas" feature of the global education dataframe into iso country codes
    
    Parameters
    ----------
    name: str
        Country name.
    
    Returns
    -------
    str
        The three character iso code    
    """
    if pd.isna(name):
        return None
    
    name = str(name).strip()
    name = FIXES.get(name, name)

    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        try:
            return pycountry.countries.search_fuzzy(name)[0].alpha_3
        except:
            return None

# Map countries to continents
region_map = {
    # Africa
    "Algeria": "Africa", "Angola": "Africa", "Benin": "Africa", "Botswana": "Africa",
    "Burkina Faso": "Africa", "Burundi": "Africa", "Cabo Verde": "Africa",
    "Cameroon": "Africa", "Central African Republic": "Africa", "Chad": "Africa",
    "Comoros": "Africa", "Republic of the Congo": "Africa",
    "Democratic Republic of the Congo": "Africa", "Djibouti": "Africa",
    "Egypt": "Africa", "Equatorial Guinea": "Africa", "Eritrea": "Africa",
    "Eswatini": "Africa", "Ethiopia": "Africa", "Gabon": "Africa",
    "The Gambia": "Africa", "Ghana": "Africa", "Guinea": "Africa",
    "Guinea0Bissau": "Africa", "Ivory Coast": "Africa", "Kenya": "Africa",
    "Lesotho": "Africa", "Liberia": "Africa", "Libya": "Africa",
    "Madagascar": "Africa", "Malawi": "Africa", "Mali": "Africa",
    "Mauritania": "Africa", "Mauritius": "Africa", "Morocco": "Africa",
    "Mozambique": "Africa", "Namibia": "Africa", "Niger": "Africa",
    "Nigeria": "Africa", "Rwanda": "Africa", "Sao Tome and Principe": "Africa",
    "Senegal": "Africa", "Seychelles": "Africa", "Sierra Leone": "Africa",
    "Somalia": "Africa", "South Africa": "Africa", "South Sudan": "Africa",
    "Sudan": "Africa", "Tanzania": "Africa", "Togo": "Africa",
    "Tunisia": "Africa", "Uganda": "Africa", "Zambia": "Africa",
    "Zimbabwe": "Africa", "Cape Verde": "Africa",

    # Asia
    "Afghanistan": "Asia", "Armenia": "Asia", "Azerbaijan": "Asia",
    "Bahrain": "Asia", "Bangladesh": "Asia", "Bhutan": "Asia",
    "Brunei": "Asia", "Cambodia": "Asia", "China": "Asia",
    "Cyprus": "Asia", "Georgia": "Asia", "India": "Asia",
    "Indonesia": "Asia", "Iran": "Asia", "Iraq": "Asia",
    "Israel": "Asia", "Japan": "Asia", "Jordan": "Asia",
    "Kazakhstan": "Asia", "Kuwait": "Asia", "Kyrgyzstan": "Asia",
    "Laos": "Asia", "Lebanon": "Asia", "Malaysia": "Asia",
    "Maldives": "Asia", "Mongolia": "Asia", "Myanmar": "Asia",
    "Nepal": "Asia", "North Korea": "Asia", "Oman": "Asia",
    "Pakistan": "Asia", "Palestinian National Authority": "Asia",
    "Philippines": "Asia", "Qatar": "Asia", "Saudi Arabia": "Asia",
    "Singapore": "Asia", "South Korea": "Asia", "Sri Lanka": "Asia",
    "Syria": "Asia", "Tajikistan": "Asia", "Thailand": "Asia",
    "East Timor": "Asia", "Turkey": "Asia", "Turkmenistan": "Asia",
    "United Arab Emirates": "Asia", "Uzbekistan": "Asia",
    "Vietnam": "Asia", "Yemen": "Asia",

    # Europe
    "Albania": "Europe", "Andorra": "Europe", "Austria": "Europe",
    "Belarus": "Europe", "Belgium": "Europe", "Bosnia and Herzegovina": "Europe",
    "Bulgaria": "Europe", "Croatia": "Europe", "Czech Republic": "Europe",
    "Denmark": "Europe", "Estonia": "Europe", "Finland": "Europe",
    "France": "Europe", "Germany": "Europe", "Greece": "Europe",
    "Hungary": "Europe", "Iceland": "Europe", "Ireland": "Europe",
    "Italy": "Europe", "Latvia": "Europe", "Liechtenstein": "Europe",
    "Lithuania": "Europe", "Luxembourg": "Europe", "Malta": "Europe",
    "Moldova": "Europe", "Monaco": "Europe", "Montenegro": "Europe",
    "Netherlands": "Europe", "North Macedonia": "Europe", "Norway": "Europe",
    "Poland": "Europe", "Portugal": "Europe", "Romania": "Europe",
    "Russia": "Europe", "San Marino": "Europe", "Serbia": "Europe",
    "Slovakia": "Europe", "Slovenia": "Europe", "Spain": "Europe",
    "Sweden": "Europe", "Switzerland": "Europe", "Ukraine": "Europe",
    "United Kingdom": "Europe", "Vatican City": "Europe", 
    "Republic of Ireland": "Europe",

    # North America
    "Antigua and Barbuda": "North America", "Bahamas": "North America",
    "Barbados": "North America", "Belize": "North America",
    "Canada": "North America", "Costa Rica": "North America",
    "Cuba": "North America", "Dominica": "North America",
    "Dominican Republic": "North America", "El Salvador": "North America",
    "Grenada": "North America", "Guatemala": "North America",
    "Haiti": "North America", "Honduras": "North America",
    "Jamaica": "North America", "Mexico": "North America",
    "Nicaragua": "North America", "Panama": "North America",
    "Saint Kitts and Nevis": "North America", "Saint Lucia": "North America",
    "Saint Vincent and the Grenadines": "North America",
    "Trinidad and Tobago": "North America", "United States": "North America",
    "Anguilla":"North America", "The Bahamas":"North America",
    "British Virgin Islands":"North America", "Montserrat":"North America",
    "Turks and Caicos Islands":"North America",

    # South America
    "Argentina": "South America", "Bolivia": "South America",
    "Brazil": "South America", "Chile": "South America",
    "Colombia": "South America", "Ecuador": "South America",
    "Guyana": "South America", "Paraguay": "South America",
    "Peru": "South America", "Suriname": "South America",
    "Uruguay": "South America", "Venezuela": "South America",

    # Oceania
    "Australia": "Oceania", "Fiji": "Oceania", "Kiribati": "Oceania",
    "Marshall Islands": "Oceania", "Micronesia": "Oceania",
    "Nauru": "Oceania", "New Zealand": "Oceania", "Palau": "Oceania",
    "Papua New Guinea": "Oceania", "Samoa": "Oceania",
    "Solomon Islands": "Oceania", "Tonga": "Oceania",
    "Tuvalu": "Oceania", "Vanuatu": "Oceania",
    "Cook Islands": "Oceania", "Federated States of Micronesia": "Oceania",
    "Niue": "Oceania", "Tokelau": "Oceania",
}

def processed_df(df) -> pd.DataFrame:
    """Preprocess the dataframe.

    Processing:
    - Drop columns: Latitude, Longitude, OOSR_Pre0Primary_Age_Male, OOSR_Pre0Primary_Age_Female
    - Create columns: iso3, Region, Literacy_Gap, Literacy_Avg, Completion_Gap_{education_level},
    Completion_Avg_{education_level}, OOSR_Gap_{education_level}, OOSR_Avg_{education_level}
    - Fixed country names
    - Changed missing values to nan type

    Parameters
    ----------
    None

    Returns
    -------
    plotly.express.chorpleth
        Interactive world map figure.

    """
    processed = df.copy()

    # Drop unused columns (handle trailing space safely)
    cols_to_drop = ["Latitude ", "Longitude", "OOSR_Pre0Primary_Age_Male", "OOSR_Pre0Primary_Age_Female"]
    processed = processed.drop(columns=[c for c in cols_to_drop if c in processed.columns])

    # iso3
    processed["iso3"] = processed["Countries and areas"].apply(to_iso3)

    # Fix country name for STP
    processed.loc[processed["iso3"] == "STP", "Countries and areas"] = "Sao Tome and Principe"

    # Region mapping + remove Other
    processed["Region"] = processed["Countries and areas"].map(region_map).fillna("Other")
    processed = processed[processed["Region"] != "Other"].copy()

    # 0 -> NaN for numeric columns
    numeric_cols = processed.select_dtypes(include=["number"]).columns
    processed[numeric_cols] = processed[numeric_cols].replace(0, np.nan)

    # Literacy gap + average
    processed["Literacy_Gap"] = (
        processed["Youth_15_24_Literacy_Rate_Male"] - processed["Youth_15_24_Literacy_Rate_Female"]
    )
    processed["Literacy_Avg"] = processed[
        ["Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female"]
    ].mean(axis=1)

    # Completion + OOSR gaps/avgs
    levels = ["Primary", "Lower_Secondary", "Upper_Secondary"]
    for level in levels:
        processed[f"Completion_Gap_{level}"] = (
            processed[f"Completion_Rate_{level}_Male"] - processed[f"Completion_Rate_{level}_Female"]
        )
        processed[f"Completion_Avg_{level}"] = processed[
            [f"Completion_Rate_{level}_Male", f"Completion_Rate_{level}_Female"]
        ].mean(axis=1)

        processed[f"OOSR_Gap_{level}"] = (
            processed[f"OOSR_{level}_Age_Male"] - processed[f"OOSR_{level}_Age_Female"]
        )
        processed[f"OOSR_Avg_{level}"] = processed[
            [f"OOSR_{level}_Age_Male", f"OOSR_{level}_Age_Female"]
        ].mean(axis=1)

    return processed

if __name__ == "__main__":
    df = pd.read_csv('data/raw/Global_Education.csv', encoding='latin-1')
    pro_df = processed_df(df)
    pro_df.to_csv("data/processed/processed_global_education.csv")