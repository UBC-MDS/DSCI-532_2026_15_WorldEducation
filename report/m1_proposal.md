## Section 1: Motivation and Purpose

**Our role:** Data scientist for a non-profit organization

**Target audience:** Researchers, educators, and policy makers

**Problem & Solution**:

Different countries across the world have diverse education systems. If we could understand which factors lead to higher standards of education systems, they can be used by the researchers, educators, and policymakers to assess and improve education systems globally. To address this challenge, we propose building a dashboard where we can utilize this Kaggle dataset from UNESCO Institute for Statistics, UNICEF, and UN Statistics Division and visualize different features in order to obtain insights into education on a global scale. Our app will show distributions of different features on a world map in a heat map form and relationships between features using histograms, scatterplots, and bar charts. Users will be able to explore different features by filtering and re-ordering on different variables to do exploratory data analysis and see if any factors in particular contribute to different education systems across the world.

## Section 2: Description of the Data

We will be visualizing a dataset of 202 countries. Each country has 29 variables that describe characteristics such as out-of-school rates, completion rates, proficiency levels, literacy rates, birth rates, and enrollment figures in primary and tertiary education. Some of the features have separate data for male and female too. The detailed description can be found below.

> 1.  **Countries and Areas**: Name of the countries and areas.
>
> 2.  **Latitude**: Latitude coordinates of the geographical location.
>
> 3.  **Longitude**: Longitude coordinates of the geographical location.
>
> 4.  **OOSR_Pre0Primary_Age_Male**: Out-of-school rate for pre-primary age males.
>
> 5.  **OOSR_Pre0Primary_Age_Female**: Out-of-school rate for pre-primary age females.
>
> 6.  **OOSR_Primary_Age_Male**: Out-of-school rate for primary age males.
>
> 7.  **OOSR_Primary_Age_Female**: Out-of-school rate for primary age females.
>
> 8.  **OOSR_Lower_Secondary_Age_Male**: Out-of-school rate for lower secondary age males.
>
> 9.  **OOSR_Lower_Secondary_Age_Female**: Out-of-school rate for lower secondary age females.
>
> 10. **OOSR_Upper_Secondary_Age_Male**: Out-of-school rate for upper secondary age males.
>
> 11. **OOSR_Upper_Secondary_Age_Female**: Out-of-school rate for upper secondary age females.
>
> 12. **Completion_Rate_Primary_Male**: Completion rate for primary education among males.
>
> 13. **Completion_Rate_Primary_Female**: Completion rate for primary education among females.
>
> 14. **Completion_Rate_Lower_Secondary_Male**: Completion rate for lower secondary education among males.
>
> 15. **Completion_Rate_Lower_Secondary_Female**: Completion rate for lower secondary education among females.
>
> 16. **Completion_Rate_Upper_Secondary_Male**: Completion rate for upper secondary education among males.
>
> 17. **Completion_Rate_Upper_Secondary_Female**: Completion rate for upper secondary education among females.
>
> 18. **Grade_2_3_Proficiency_Reading**: Proficiency in reading for grade 2-3 students.
>
> 19. **Grade_2_3_Proficiency_Math**: Proficiency in math for grade 2-3 students.
>
> 20. **Primary_End_Proficiency_Reading**: Proficiency in reading at the end of primary education.
>
> 21. **Primary_End_Proficiency_Math**: Proficiency in math at the end of primary education.
>
> 22. **Lower_Secondary_End_Proficiency_Reading**: Proficiency in reading at the end of lower secondary education.
>
> 23. **Lower_Secondary_End_Proficiency_Math**: Proficiency in math at the end of lower secondary education.
>
> 24. **Youth_15_24_Literacy_Rate_Male**: Literacy rate among male youths aged 15-24.
>
> 25. **Youth_15_24_Literacy_Rate_Female**: Literacy rate among female youths aged 15-24.
>
> 26. **Birth_Rate**: Birth rate in the respective countries/areas.
>
> 27. **Gross_Primary_Education_Enrollment**: Gross enrollment in primary education.
>
> 28. **Gross_Tertiary_Education_Enrollment**: Gross enrollment in tertiary education.
>
> 29. **Unemployment_Rate**: Unemployment rate in the respective countries/areas

Using this data allows us to analyze and comprehend the dynamic nature of education systems worldwide. We can also compare and analyze if there are any trends or disparities between different countries, different continents, different genders, etc. to gain insights into education on a global scale.

## Section 3: Research Questions & Usage Scenarios

### Usage Scenario

Jessica is a policy maker at the Ministry of Education and she has to come up with new policies to further improve education systems on a national scale. She frequently collaborates with researchers and international organizations and has to justify policy decisions using data. However, she is often overwhelmed by the amount of data across countries.

In order to do that, she first needs to understand what factors contribute to better education systems globally. She wants to explore a World education dataset to compare the effects of different variables and identify which of these variables affect education systems across the world the most and better create policies with the focus on these variables.

When Jessica logs on to our "World Education app", she will see an overview of all the available variables in the dataset, categorized by education level, gender, and socioeconomic factors. Then, she can select one of these variables such as out-of-school rates for lower secondary education to display on a global heat map and identify regions with particularly high rates.

Next, she compares this variable with other variables such as completion rates and youth literacy rates by using scatter plots and sees if there are any strong correlations between them. If she is interested in certain countries/ regions, she can filter data points to be those from countries of interest for more detailed analysis.

She can also compare the gender effects on several variables as well. For some regions where gender plays an important role in education, dropout rates might be higher for female students. By comparing these trends with birth rates and unemployment rates, she gains insight into how demographic and economic pressures may influence educational participation.

Based on her findings from using our app, Jessica hypothesizes that secondary completion rates, gender gaps, and youth literacy are strongly correlated with successful education systems across the world. These insights allow her to make data-driven policies such as policies to encourage students to stay in school or policies to help bridge gender gaps.

### User Stories

**User Story 1:** As a **policy maker**, I want to filter and compare education indicators across countries and regions to identify geographic disparities in education outcomes.

**User Story 2:** As a **policy maker**, I want to analyze education indicators by gender to determine whether male and female students experience unequal access to education systems.

**User Story 3:** As a policy maker, I want to visualize education indicators on a world map and through comparative charts in order to quickly identify global patterns, trends, and outliers.

### Jobs to Be Done

**JTBD 1:**

**Situation:** When I am evaluating the overall performance of education systems across countries,

**Motivation:** I want to compare key education indicators such as completion rates and literacy rates across regions,

**Outcome:** so I can identify which regions are lagging behind and require targeted policy attention.

**JTBD 2:** **Situation:** When designing policies to bridge gender inequality in education,

**Motivation:** I want to compare different education variables separately for male and female students across different education levels

**Outcome:** so I can identify gender-based disparities and design policies that promote equal access to education.

**JTBD 3:**

**Situation:** When I am reviewing large-scale global education data,

**Motivation:** I want to visualize education indicators on a global heat map,

**Outcome:** so I can quickly detect global patterns, trends, and outlier countries that require further investigation or policy intervention.

## Section 4: Exploratory Data Analysis

JTBD 1:

Situation: When I am evaluating the overall performance of education systems across countries,

Motivation: I want to compare key education indicators such as completion rates and literacy rates across regions,

Outcome: so I can identify which regions are lagging behind and require targeted policy attention.

**Analysis:** The bar chart in `notebooks/EDA.ipynb` reveals critical patterns in global education performance across levels and genders. Completion rates show a progressive decline from primary (\~41-42%) to upper secondary (\~22-23%), indicating significant student attrition as education levels advance. Gender parity is largely maintained within each education level, with minimal differences between male and female completion rates. Youth literacy rates remain high and gender-balanced (\~35-36%), suggesting foundational literacy skills are being achieved despite lower completion rates at higher education levels. These findings highlight that while access to basic education is relatively equitable, retention through secondary education remains a major challenge requiring targeted interventions to reduce dropout rates.

## Section 5: App Sketch & Description

![Sketch](../img/sketch.png)

The dashboard opens with a global heat map that provides an overview of selected education indicators across countries. Countries are color-coded based on the chosen metric, and hovering over a country reveals its exact value. This allows users to quickly identify global patterns and outliers while still accessing information for each country individually.

A filter panel on the left enables users to refine the view by region, education level, indicator type, value range, and gender. Filters are applied intentionally to update all visual components together. The interface also supports a multipanel layout, allowing users to compare different indicators side by side.

Below the map, bar charts and scatter plots provide deeper comparative insights across regions, education levels, or gender. A scrollable data table displays the filtered dataset for transparency and detailed inspection. Overall, the dashboard is designed to move from global overview to targeted comparison in a structured and intuitive way.
