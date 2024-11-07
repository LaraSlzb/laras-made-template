# Project Plan

## Title
<!-- Give your project a short title. -->
Impact of physical activities on mental health.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Does the amount of physical activities impact mental health?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
As the importance of mental health rises nowadays, I want to analyze if there is a relation between the amount of physical activities done and the mental health. As it is common knowledge that physical activities rises the dopamine and helps you feel better, I want to discover if you can see this relationship in Americas society. I want to compare the result of a study about the time people are doing physical activities with another survey about mental health. I want to show that states where people are more active have less problems with mental health.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Physical Activities
* Metadata URL: https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system 
* Data URL: https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD 
* Data Type: CSV

This dataset includes data on adult's diet, physical activity, and weight status from Behavioral Risk Factor Surveillance System. The data is divided by the states of America and time (2011-2023) and includes multiple questions about the lifestyle.

### Datasource2: Mental Health
* Metadata URL: https://www.samhsa.gov/data/report/2021-2022-nsduh-state-prevalence-estimates
* Data URL: https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent-CSVs.zip
* Data Type: ZIP (includes multiple CSV)

This package of datasets includes the dataset "Any Mental Illness in the Past Year" from the National Surveys on Drug Use and Health (NSDUH) from 2020-2021. The data is divided by the states of America.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Clean dataset Mental Health [#1][i1]
2. Clean dataset Physical Activities [#2][i2]
3. Combine datasets [#3][i3]
4. Analyze the impact of physical activities on mental health [#4][i4]


[i1]: https://github.com/LaraSlzb/laras-made-template/issues/1
[i2]: https://github.com/LaraSlzb/laras-made-template/issues/2
[i3]: https://github.com/LaraSlzb/laras-made-template/issues/3
[i4]: https://github.com/LaraSlzb/laras-made-template/issues/4