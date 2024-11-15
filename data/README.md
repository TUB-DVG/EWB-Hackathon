# `data` Directory

The `data` folder stores all data files used in this project, including raw datasets, processed files, and any additional metadata needed for data processing and analysis. Organizing data files here keeps the repository clean and allows for efficient data handling and versioning.

## Folder Structure

To maintain organization, data files are separated into different subdirectories based on their processing stage and type.


data/
├── raw/                       # Raw data files
│   ├── dataset1.csv          # Example raw dataset
│   └── dataset2.json         # Another example raw dataset
├── processed/                 # Processed data files
│   ├── dataset1_processed.csv # Example processed dataset
│   └── dataset2_processed.json # Another example processed dataset
├── interim/                   # Interim data files
│   ├── dataset1_interim.csv   # Example interim dataset
│   └── logs.json              # Example logs file
├── metadata/                  # Metadata files
│   ├── dataset1_metadata.json # Example metadata file
│   └── dataset2_metadata.json # Another example metadata file



### Subfolder Descriptions

- **`raw/`**: Contains the original, unaltered data files as collected or sourced. This data serves as the base for any processing or analysis tasks. Avoid making changes directly to files in this directory to maintain data integrity.

- **`processed/`**: Holds data files that have been cleaned, transformed, and prepared for analysis. This may include datasets with removed duplicates, formatted data, or derived variables.

- **`interim/`**: Stores temporary data files generated during intermediate processing stages. Files here may not be used directly in analysis but are useful for tracking transformations or debugging.

- **`metadata/`**: Contains documentation and descriptive files for the data, such as data dictionaries, README files for individual datasets, or notes on data sources. Metadata provides context, explanations of variables, and any preprocessing steps.

## Usage Guidelines

1. **Data Formats**: Use common, machine-readable formats like CSV for tables, JSON for structured data, and TXT for unstructured or reference data.
   
2. **Naming Conventions**: Name files descriptively to indicate their contents and processing stage. For example, `energy_data_raw.csv` for raw data and `energy_data_cleaned.csv` for processed data.

3. **Data Versioning**: Avoid modifying files directly within `raw/`. Any transformations or cleaning steps should be scripted and saved in `processed/` to maintain a versioned approach to data processing.

4. **File Sizes**: Keep individual file sizes manageable. If a dataset is too large, consider compressing it or providing a sample file for local testing and including instructions for obtaining the full dataset.

5. **Referencing Data Files**: Use relative paths to access data files within the code to ensure compatibility across environments when the project is cloned or moved.

## Contributing to `data`

- **Adding New Data**: Place new datasets in `raw/` and document any relevant details in the `metadata/` folder, including the data source, collection date, and intended use.
- **Updating Data**: When updating a dataset, save the modified version in `processed/` rather than overwriting files in `raw/`.
- **Documentation**: Include any data dictionaries, descriptions, or notes in the `metadata/` folder to help future users understand the context and structure of the data.

---

The `data` folder centralizes data management, ensuring data integrity and traceability across the project. For questions or guidance on handling or organizing data files, please reach out or refer to the main project documentation.
