# MP1 Data Pipeline

mp1-data-pipeline is a command line pipeline that takes a CSV file and a YAML config file and outputs the cleaned CSV. The pipeline can also works on other datasets besides the sample_data.csv without changing the code since nothing is hard coded. The first step of the pipeline is to check the input and config file to see if it exists, then it checks the data to see if all the coloumns exists etc, then it cleans the data by removing missing values and duplicates, finally it saves the result and prints a full report on what it did. pipeline.py coordinates the steps, while the work is done by the files in src/. 


## Example
```
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```
ut output/clean.csv --config config/config.yaml --verbose
19:39:04 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
19:39:04 INFO     src.utils — Input file validated: fixtures/sample_data.csv
19:39:04 INFO     src.utils — Input file validated: config/config.yaml
19:39:04 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
19:39:04 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
19:39:04 WARNING  src.data_validator — Invalid numeric value in rating at row 94: 'not_available'
19:39:04 WARNING  src.data_validator — Invalid numeric value in rating at row 95: 'error'
19:39:04 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
19:39:04 DEBUG    src.data_validator — Validation: 100 -> 98 rows
19:39:04 INFO     __main__ — Validation complete: 100 -> 98 rows
19:39:04 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
19:39:04 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
19:39:04 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
19:39:04 INFO     __main__ — Processing complete: 98 -> 92 rows
19:39:04 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
19:39:04 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'columns_after': 5,
 'columns_before': 5,
 'columns_removed': 0,
 'rows_after': 92,
 'rows_before': 98,
 'rows_removed': 6}
```