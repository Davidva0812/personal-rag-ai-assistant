# Bank Statement Data Analysis


This project analyzes a bank statement dataset using **Pandas** for data processing
and **Plotly** for visualization. The goal is to **clean the data, extract useful insights**,
visualize **monthly balance trends** and **monthly transaction numbers**.

---

## **Features**
- File selection via a graphical interface (Tkinter)
- Reads transaction data from an Excel file.
- Cleans and processes the dataset (date formatting, balance conversion, sorting).
- Creates a **Months** column to group transactions by month.
- Extracts:
  - The last balance value of each month.
  - The total number of transactions per month.
- Saves cleaned data into **HTML**, **CSV** and **JSON** files.
- Generates two visual reports using **Plotly**:
  - **Area Chart**: Shows the balance trend over time.
  - **Bar Chart**: Displays the number of transactions per month.

## **Prerequisites**
Ensure you have the following installed before running the script:
- **Python 3.x**
- **Pandas**
- **Plotly**
- **Tkinter** (comes with Python)
- **OpenPyXL** (for reading Excel files)

## **Screenshots**
![screenshot](screenshots/balance.png)
![screenshot](screenshots/transactions.png)

## **Installation**
To install the required dependencies, run:
```bash
pip install pandas plotly openpyxl
```

## **Output files:**
- `fig1.html`: Interactive visualization of monthly balance trends.
- `fig2.html`: Interactive visualization of the number of monthly transactions.
Console log messages indicating processing steps.
Furthermore, **CSV** and **JSON** files:
- `monthly_balance_trend.csv`
- `monthly_balance_trend.json`
- `monthly_transaction_count.csv` 
- `monthly_transaction_count.json`

## **Error Handling**
If the Excel file is missing, a warning is displayed, and the script exits.
Data cleaning steps handle common formatting issues (date parsing, string-to-float conversion).

## **Example Area Chart**
The output visualization will look like this:
- **X-axis**: Year-Month
- **Y-axis**: Balance (HUF)
- Interactive tooltips showing the exact balance per month

## **Example Bar Chart**
The output visualization will look like this:
- **X-axis**: Year-Month
- **Y-axis**: Number of Transactions
- Interactive tooltips showing the exact transactions per month

## **Unit tests**
This project includes a **test_financial_statement.py** file,
containing unit tests for the **save_dataframe()** function.
Code coverage can be measured using the Coverage package (non-built-in module).

## **Future Improvements**
- Add more unit tests to increase code coverage
- Generate automated PDF reports using FPDF
- Export Plotly charts as images and embed them into PDFs
- Integrate e-mail functionality to send reports
- Create a simple web interface for uploading and viewing results

## **License**
This project is open-source and available under the **MIT License**.