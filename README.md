## Project Title

**PhonePe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly**

## Technologies

- Github Cloning
- Python
- Pandas
- MySQL
- mysql-connector-python
- Streamlit
- Plotly

## Domain

Fintech

## Problem Statement

The PhonePe Pulse GitHub repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL database

### Steps

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/jaysri125278/PhonePe-visualization-using-plotly.git
    ```

2. **Create a Virtual Environment and Activate It**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Required Packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Setup MySQL Database**:
    - Create a new MySQL database.
    - Update the database configuration in the project code (database connection details).

5. **Run the Streamlit App**:
    ```sh
    streamlit run app.py
    ```

6. **Access the Dashboard**:
    Open your browser and navigate to `http://localhost:8501`.

## File Structure

- `main.py`: Main script to run the Streamlit application.
- `phonepe.ipynb`: Script for cleaning and transforming the data for setting up the MySQL database and inserting data.
- `requirements.txt`: List of required Python packages.
- `README.md`: This readme file.

## Contributions

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## Contact

For any questions or suggestions, please reach out to jaysrisaravanan95@gmail.com.
