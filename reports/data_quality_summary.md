# Data Quality Summary

## Dataset Validation

The mutual fund datasets were reviewed to ensure data consistency and quality.

## Data Completeness

- Missing values were checked across datasets.
- Duplicate records were identified and removed wherever required.
- Data types were validated for numerical and categorical columns.

## Data Consistency

- AMFI scheme codes from Fund Master were compared with NAV History.
- Total Fund Master AMFI Codes: 40
- Total NAV History AMFI Codes: 40
- No missing AMFI codes were identified.

## NAV Data Validation

- Live NAV data was fetched successfully from mfapi.in.
- NAV data for 6 mutual fund schemes was collected and stored as CSV files.

## Conclusion

The ingested datasets passed basic data quality checks and are ready for further analysis and dashboard development.