# Sales Register Analysis Tool

## Overview

This Streamlit application is designed for audit professionals to analyze sales register data in accordance with SA 520 (Standard on Auditing 520 - Analytical Procedures). The tool facilitates the comparison of current year and prior year sales data, performs trend analysis, and aids in sample selection using various sampling methodologies for substantive testing procedures.

## Features

### Data Loading and Preparation
- Upload current year and prior year sales register data in CSV format
- Automatic date parsing and formatting
- Year and month extraction for trend analysis

### Filtering Capabilities
- Date range filtering
- Customer-specific filtering
- Amount range filtering (minimum and maximum)

### Analysis Features
- Side-by-side comparison of current and prior year data
- Monthly trend analysis 
- Percentage change calculations
- Visualization of trends using line charts
- Highlighting of significant changes (>10% variance)

### Sample Selection Methods
- Random Sampling
- Systematic Sampling
- Monetary Unit Sampling (MUS)
- Judgmental Sampling
- Stratified Sampling

### Additional Functionality
- Option to add judgmental samples to the initial selection
- Documentation of sampling methodology used
- Customizable sample size

## Installation Requirements

```bash
pip install streamlit pandas plotly
```

## Required Data Format

The application expects CSV files with the following columns:
- `Invoice Number`
- `Invoice Date` (in DD-MM-YYYY format)
- `Customer Name`
- `Total Amount`
- `Total Amount (Inc. Tax)`

## Usage Instructions

1. **Launch the application**:
   ```bash
   streamlit run app.py
   ```

2. **Upload Data**:
   - Use the sidebar to upload current year sales register (required)
   - Upload prior year sales register (optional, for comparison)

3. **Apply Filters**:
   - Set date range
   - Select specific customer (or "All")
   - Set minimum and maximum amount thresholds

4. **View Trend Analysis**:
   - Examine monthly comparison tables
   - Review the line chart visualization
   - Note significant changes highlighted in yellow

5. **Select Samples**:
   - Choose the sampling method
   - Set the sample size
   - Configure method-specific parameters if applicable
   - Generate the initial sample
   - Optionally add judgmental selections

## Sampling Methods Explained

### Random Sampling
Selects transactions completely at random from the filtered dataset, providing each transaction an equal probability of selection.

### Systematic Sampling
Selects transactions at regular intervals throughout the dataset (e.g., every 10th transaction), starting from a specified point.

### Monetary Unit Sampling (MUS)
A probability-proportional-to-size sampling method where selection probability is proportional to the transaction amount. Larger transactions have a higher chance of selection.

### Judgmental Sampling
Allows the auditor to manually select specific transactions of interest based on professional judgment.

### Stratified Sampling
Divides the population into distinct subgroups (strata) based on transaction amounts and selects samples from each stratum, ensuring coverage across the value spectrum.

## Audit Documentation

The application automatically documents the sampling methodology used, which can be included in the audit working papers to demonstrate compliance with standards.

## Best Practices

1. Ensure data completeness before uploading
2. Use consistent data formats between current and prior year
3. Investigate significant variances (>10%)
4. Combine sampling methods for comprehensive coverage
5. Document reasons for judgmental selections

## Troubleshooting

- **File Upload Issues**: Ensure CSV files are properly formatted with the expected column names
- **Date Format Errors**: Confirm invoice dates are in DD-MM-YYYY format
- **Empty Visualizations**: Check that filtered data contains valid transactions within the selected parameters

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contact

For support or questions regarding this application, please contact:

Email: nishanth@varmaandvarma.com
