* Retractions of publications in radiomics: an underestimated problem?

## Data Processing

After retrieving all data from the sources and saving them as CSV (or similar) files to `./data/<source>`, the script `merge.py` was used to harmonize and merge them. This script also removes duplicate entries and reports the corresponding numbers. The harmonized and merged data is then written to `./results/table_raw.csv`.

**NOTE:** The date column in `table_raw.csv` is partially incorrect due to an error in using dates from the original CSV files. The dates were corrected in `table_final.xlsx`.

Subsequently, missing information was completed, primarily regarding the relevance of the publications, the origin country of the first authors, and the publisher. The completed file was saved as `./results/table_raw.xlsx` (note that this is now an Excel file).

Next, `filter.py` was used to exclude non-relevant publications and further harmonize the data. The final, filtered table was saved as `./results/table_relevant.xlsx`. This table was then further enriched by adding information such as the number of publication citations and time-to-retraction, and saved as `./results/table_final.xlsx`. From this final table, `parse.py` will generate the plots for the publication.

In addition, `journal.py` identifies all journals that published a radiomics paper in 2025. This analysis aims to determine whether the majority of radiomics publications are published in radiological/oncological journals, which indeed they are.
