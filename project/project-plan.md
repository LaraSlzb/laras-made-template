# Project Plan

## Title
<!-- Give your project a short title. -->
Impact of physical activities on mental health.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Does the amount of physical activity have an impact mental health?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
As, nowadays, mental health gets more and more important, I will analyse if there is a correlation between the amount of physical
activity performed and mental health. As it is common knowledge that physical activity increases
the dopamine level and causes a better feeling, I want to explore if such a correlation can be seen in Americas society. 
A study about the time people spending on physical activities will be compared to a different survey about 
mental health. I want to show that in US states where people are more active struggle less with mental health.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefix "DatasourceX" where X is the id of the datasource. -->

### Datasource 1: Physical Activities
* Metadata URL: https://catalog.data.gov/dataset/nutrition-physical-activity-and-obesity-behavioral-risk-factor-surveillance-system 
* Data URL: https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD 
* Data Type: CSV

This dataset includes data on adult's diet, physical activity, and weight status from the Behavioral Risk Factor Surveillance System. The data is provided separately for each state
of the US and for each year from 2011 to 2023 and includes multiple questions about the lifestyle.

### Datasource 2: Mental Health
* Metadata URL: https://www.samhsa.gov/data/report/2018-2019-nsduh-state-prevalence-estimates
* Data URL:https://www.samhsa.gov/data/sites/default/files/reports/rpt32805/2019NSDUHsaeExcelPercents/2019NSDUHsaeExcelPercents/2019NSDUHsaeExcelCSVs.zip
* Data Type: ZIP (includes multiple CSV)

This package of datasets includes the dataset "Any Mental Illness in the Past Year" from the National Surveys on Drug Use and Health (NSDUH) from 2018 to 2019.
The data is again provided separately for each state of the US.

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