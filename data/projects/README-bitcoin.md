# Bitcoin Price Prediction with Polynomial Regression


This Python project performs a simple prediction of Bitcoin closing prices for the years 2025 and 2026 
using a **Polynomial Regression** model. 
It includes data preprocessing, model fitting, future value prediction, and interactive visualization with Plotly.

---

## **Features**
- Loads and validates historical Bitcoin price data
- Uses the 'Year' as the only feature for prediction
- Applies Polynomial Regression to model trends
- Predicts closing prices for 2025 and 2026
- Generates an interactive Plotly graph
- Saves the output graph to an HTML file

## **Requirements**
Ensure you have the following installed before running the script:
- **Python 3.x**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Plotly**

## **Installation**
To install the required dependencies, run:
```bash
pip install pandas numpy scikit-learn plotly
```

## **Screenshots**
![screenshot](screenshots/bitcoin_data.png)

## **Future Improvements**
- Incorporate additional features like Open, High, Low, Volume, and Market Cap 
for a more robust and realistic prediction model.
- Use time series forecasting models like ARIMA, SARIMA, Prophet, or LSTM, 
which are more appropriate for financial time series data.
- Introduce performance metrics (e.g. RMSE, MAE, R²) to evaluate 
and compare the accuracy of models.
- Convert the script into a web application using Streamlit, Dash, or Flask 
for a more user-friendly experience.
- Add unit tests with mocking: Implement unit tests that mock external dependencies like file I/O, 
machine learning models, and plotting functions to ensure faster, isolated, and more reliable tests.

## Data source and License
This project uses the [Kaggle - Bitcoin Historical Prices and Activity (2010–2024)](https://www.kaggle.com/datasets/priyamchoksi/bitcoin-historical-prices-and-activity-2010-2024) dataset, 
which has been released under the MIT license.

**Author**: Priyam Choksi  
**License**: MIT License
