# Documentation of Bonaire Spatial Analysis


## Overview
In recent years, there has been a global call to increase physical activity levels, especially among vulnerable population groups. Incorporating physical activities such as walking and cycling into daily routines can significantly benefit public and planetary health. This need is particularly pressing in the Caribbean, where physical activity levels are low, and obesity, mortality, and morbidity rates are high. The Caribbean Dutch municipality of Bonaire is no exception, with data indicating that 60% of its residents suffer from overweight, obesity, and other preventable health conditions.

Bonaire is a small island with a population of approximately 25,000, located 80km from the coast of Venezuela. In 2024, the Urban Cycling Institute initiated a project, supported by the Netherlands' Ministry of Public Health, aimed at increasing physical activity levels on Bonaire through active mobility. This four-year project involves a multidisciplinary team of researchers from the Urban Cycling Institute, staff from the Ministry of Health, Welfare, and Sports, and local stakeholders from various sectors on the island. A key player in this project is Rita Gemerts of Ray-Action, who acts as an embedded citizen scientist providing context-specific knowledge, stakeholder networks, and local programs and interventions.

## Project Goals
The project will culminate in the development of a suite of evidence-based policy recommendations designed to increase physical activity among the population of Bonaire. Central to the project is community-based participatory research, which involves local stakeholders and citizens throughout the entire process. This approach ensures that the policy actions developed are tailored specifically for Bonaire by Bonaireans.

## Contact Information
For any inquiries regarding the datasets used in the porject, how they were computed and the function of the application, please contact:
**Desmond Lartey**
Researcher at Urban Cycling Institute
Email: desmond@urbancyclinginstitute.org

## Applications Created and Their Objectives

### Facilities App
- **Objective:** To monitor and analyze the physical activity levels of Bonaire residents, focusing on walking and cycling with key faciclities and roadnetwroks as benchmarks. Also to show various locations of facilities and where they are.
- **Description:** This app provides a map of key facilities such as parks, health centers, and recreational areas, helping residents find places to engage in physical activity. It also computes service area netwrok analysis for major faccilities. From this app, we know which areas have high and low accebitlity with =in specific dsitances and how do they compare per neighborhoods.

### Population Analysis App
- **Objective:** To visualize the population distribution and changes over time in Bonaire.
- **Description:** This app uses data visualizations like treemaps and scatter plots to display population data by year, neighborhood, and demographic characteristics.

### Demographic Analysis App
- **Objective:** To analyze the population by sex and age cohorts across neighborhoods.
- **Description:** This app includes choropleth maps and bar charts to display the distribution of population demographics, providing insights into the needs of different groups.

### Field Survey and Observation Analysis App
- **Objective:** To analyze data from field surveys and observations.
- **Description:** This app offers various analyses such as correlation, distribution, and Sankey diagrams to understand mobility patterns and preferences from survey data.

### Policy Insights
- **Objective:** To support policymakers in developing evidence-based strategies for increasing physical activity.
- **Description:** There is a reflection on the data collected and analysed as well as what actionable policy recommendations necessary for enhancing active mobility in Bonaire.

## Datasets Descriptions

### Dataset Description

| Dataset Name          | Description                                                                                   | Creation Method                                                                                  |
|-----------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Population            | Contains demographic information of Bonaire residents including age, gender, and occupation.  | Collected from the GPWv4.11 Population Count ImageCollection in Google Earth Engine (GEE). [GPWv4.11](https://code.earthengine.google.com/?scriptPath=Examples:Datasets/CIESIN/GPWv411/GPW_Population_Count) |
| Sex                   | Gender distribution data used for analyzing activity level differences between men and women. | Extracted from the WorldPop dataset for 2020 in GEE, aggregated and exported as CSV and GeoTIFF files. [WorldPop](https://code.earthengine.google.com/?scriptPath=Examples:Datasets/WorldPop/GP/100m/pop_age_sex) |
| Neighborhood          | Spatial data on different neighborhoods in Bonaire, including infrastructure and amenities.   | Created using GIS tools, including QGIS for hexagon grid creation and GEE for population distribution. [Zonal Stats](https://code.earthengine.google.com/?scriptPath=Examples:Datasets/JRC_GHSL_P2023A_GHS_BUILT_C) |
| Activity Levels       | Data on walking and cycling activities of residents across different neighborhoods.            | Computed in QGIS using the Network Analysis tool to determine service areas for facilities. Zonal statistics were calculated for each facility's service area at 15 and 30 minutes walking distances. |
| Field Surveys and Observations | Data on mobility patterns, vehicle use, and demographic characteristics.              | Collected through structured field surveys and observations, analyzed using statistical and visualization techniques. |
| Health Metrics        | **(In Progress)** Health indicators such as BMI, blood pressure, and chronic conditions prevalence. | Data to be obtained from local health departments and anonymized for research purposes.                     |


### Methodology for Data Collection and Analysis

#### Hexagon Grid Creation
We used QGIS to compute 1250-meter hexagons for the entire area of Bonaire. This breaks the whole country into neighborhoods that represent a 15-minute walk. These hexagons are used as the basis for many of our spatial analyses, including service area and population statistics.

#### Population Data Collection
The population data from 2000-2020 was collected and grouped by neighborhood. The Global Population of the World (CIESIN/GPWv411/GPW_Population_Count) dataset from CIESIN was used to extract population counts. The data was processed in Google Earth Engine (GEE) to calculate zonal statistics for each hexagon.

#### Age and Sex Data Collection
We used the WorldPop/GP/100m/pop_age_sex dataset to gather population data by age and sex. The data was filtered and processed to create a comprehensive demographic profile for each neighborhood. The processed data was then exported as GeoTIFF and CSV files for further analysis.

#### Survey and Observation Data
Field surveys and observations were conducted to gather data on mobility patterns, vehicle use, and demographic characteristics. This data was analyzed using various statistical and visualization techniques to provide insights into the factors influencing mobility in Bonaire.

### Preliminary Spatial Analysis: Service Area

#### Introduction
The service area analysis aimed to assess the accessibility of various facilities on Bonaire within 15 and 30-minute walking distances. This analysis helps to identify the population served by each facility and evaluate the overall coverage of essential services.

#### Methodology
1. **Data Collection:** The analysis used population data from the GPWv4.11 Population Count ImageCollection and the WorldPop dataset, processed in Google Earth Engine (GEE). Hexagon grids of 1250, and 2500 meters were created using QGIS to represent neighborhoods that are within a 15-minute walk.
   
2. **Network Analysis:** Conducted in QGIS using the Network Analysis tool. Facilities such as medical centers, supermarkets, community centers, schools, and cycling paths were selected as focal points. The service areas for these facilities were calculated for both 15-minute and 30-minute walking distances.
   
3. **Zonal Statistics:** Population data for each service area was computed using zonal statistics. This allowed for the calculation of the number of people served by each facility within the specified walking distances.

#### Key Findings

| Facility               | Time (min) Walking | Population Covered |
|------------------------|--------------------|--------------------|
| Access to Cycling Path | 15                 | 4,880              |
| Access to Cycling Path | 30                 | 11,207             |
| Medical Center Rincon  | 15                 | 838                |
| Medical Center Rincon  | 30                 | 873                |
| Medical Center South   | 15                 | 889                |
| Medical Center South   | 30                 | 4,618              |
| Super Market Rincon    | 15                 | 793                |
| Super Market Rincon    | 30                 | 873                |
| Super Market South     | 15                 | 3,319              |
| Super Market South     | 30                 | 10,207             |
| Community Center South | 15                 | 2,316              |
| Community Center South | 30                 | 8,764              |
| Community Center Rincon| 15                 | 756                |
| Community Center Rincon| 30                 | 863                |
| School Rincon          | 15                 | 627                |
| School Rincon          | 30                 | 863                |
| School South           | 15                 | 1,878              |
| School South           | 30                 | 9,527              |

#### Coverage Ratios
- **15-minute Coverage:** Approximately 67.6% of Bonaire's population is covered within a 15-minute walking distance to at least one facility.
- **30-minute Coverage:** The coverage ratio exceeds 100% (198.4%), indicating that facilities are accessible to the entire population within a 30-minute walking distance.

#### Insights
- **Cycling Paths:** Show a significant increase in population coverage when the access time extends from 15 to 30 minutes.
- **Medical Centers:** Rincon and South centers have a relatively small population coverage at 15 minutes but increase significantly at 30 minutes.
- **Super Markets:** Both Rincon and South markets show a moderate increase in accessible population with extended access time, with the South market serving a particularly large area at 30 minutes.
- **Community Centers:** The South community center covers a significantly larger population at 30 minutes compared to Rincon.
- **Schools:** Both Rincon and South schools show a significant increase in the population served with an extended access time, with School South having the largest increase.

#### Conclusion
The service area analysis reveals that most facilities on Bonaire can serve a considerable portion of the population within a 15-minute walk. Extending the walking distance to 30 minutes significantly increases accessibility, highlighting the importance of improving infrastructure to support longer walking and cycling distances.

This preliminary analysis provides a foundation for further studies and policy recommendations to enhance active mobility and accessibility on Bonaire. Further spatial analysis and community feedback will be crucial in refining these insights and developing targeted interventions.


## Prediction and Impact Analysis App

### Overview
This application is still in progress and aims to model the current situation based on our survey and observation data for 2024 and project future scenarios up to 2038. The goal is to assess the impact of active mobility on health and other factors over time.

### Data Required
- **Current Mobility Data:** Collected from the observation data and Field Surveys.
- **Health Data:** Health metrics such as BMI, blood pressure, and incidence of chronic conditions.
- **Demographic Data:** Age, sex, occupation, and other relevant demographic information.
- **Environmental Data:** Data on infrastructure, neighborhood amenities, and environmental factors.

### Methodology
We plan to use statistical models and machine learning techniques to predict future trends in physical activity, health outcomes, and demographic changes. The models will be calibrated using the collected data and validated against historical trends.

## Impact Assessment
The impact assessment will evaluate the benefits of increased active mobility on various health outcomes. This will include:
- Reduction in obesity and overweight prevalence.
- Economic benefits due to reduced healthcare costs and increased productivity.

## References
- Berrie, L., Feng, Z., Rice, D., Clemens, T., Williamson, L., & Dibben, C. (2024). Does cycle commuting reduce the risk of mental ill-health? An instrumental variable analysis using distance to nearest cycle path. *International Journal of Epidemiology*, 53(1), dyad153. https://doi.org/10.1093/ije/dyad153

## Conclusion
This project aims to improve the health and well-being of Bonaire residents by promoting active mobility. Combining local knowledge, involving community stakeholders, spatial analysis of the area helps us to understand better what active mobility policy options exist for Bonaire.
For any inquiries regarding the execution of the project, please contact:
**Dr. Dylan Power**
Senior Researcher at Urban Cycling Institute
Email: dylan@urbancyclinginstitute.org