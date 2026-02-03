# TOPSIS Implementation

**Project by:** Vansh  
**Roll Number:** 102483084  
**PyPI Package:** [Topsis-Vansh-102483084](https://pypi.org/project/Topsis-Vansh-102483084/)

---

## 📋 Project Overview

This repository contains a complete implementation of the **Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)**. It is divided into three distinct parts:

1. **Part 1: Command Line Script** - A Python script to calculate TOPSIS scores from a CSV file.
2. **Part 2: Python Library** - A published PyPI package for easy installation and usage.
3. **Part 3: Web Application** - A Flask-based web service to calculate and email results.

---
## 📂 Project Structure

```text
UCS654_A3_Topsis/
│
├── .gitignore               # Files excluded from Git (e.g., .env)
├── data.csv                 # Sample input dataset for testing
├── README.md                # Project documentation (this file)
│
├── Part_1_Script/           # [Part 1] Command Line Implementation
│   └── topsis.py            # Python script to run TOPSIS via CLI
│
├── Part_2_Package/          # [Part 2] PyPI Package Source
│   ├── README.md            # Package-specific documentation
│   ├── setup.py             # Configuration for building the package
│   └── Topsis_Vansh_102483084/
│       ├── __init__.py      # Package initialization
│       └── topsis.py        # Core TOPSIS logic
│
└── Part_3_Web_App/          # [Part 3] Web Service Implementation
    ├── app.py               # Flask application (Backend)
    ├── requirements.txt     # List of dependencies (Flask, pandas, etc.)
    └── templates/
        └── index.html       # Frontend interface for file upload

---

## 🧮 Methodology

TOPSIS is a multi-criteria decision analysis method that is based on the concept that the chosen alternative should have the shortest geometric distance from the positive ideal solution (PIS) and the longest geometric distance from the negative ideal solution (NIS).

### The Algorithm Steps:

1. **Create a Decision Matrix:** The raw data consisting of $m$ alternatives and $n$ criteria.
2. **Normalize the Matrix:** 
   $$r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}$$
3. **Calculate Weighted Normalized Matrix:** Multiply each column by its corresponding weight ($w_j$).
   $$v_{ij} = w_j \times r_{ij}$$
4. **Determine Ideal Solutions:**
   - **Ideal Best ($V^+$):** Max value for beneficial criteria, Min value for non-beneficial.
   - **Ideal Worst ($V^-$):** Min value for beneficial criteria, Max value for non-beneficial.
5. **Calculate Euclidean Distances:**
   - $S_i^+ = \sqrt{\sum (v_{ij} - V_j^+)^2}$
   - $S_i^- = \sqrt{\sum (v_{ij} - V_j^-)^2}$
6. **Calculate Performance Score ($P_i$):**
   $$P_i = \frac{S_i^-}{S_i^+ + S_i^-}$$
7. **Rank:** Sort alternatives by $P_i$ in descending order.

---
## 📊 Results

### Sample Input Data (`data.csv`)
The following dataset compares different models based on 5 parameters (P1-P5).

| Model | P1 | P2 | P3 | P4 | P5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | 0.87 | 0.76 | 5.1 | 69.9 | 19.16 |
| M2 | 0.60 | 0.36 | 6.6 | 35.3 | 10.72 |
| M3 | 0.83 | 0.69 | 5.2 | 57.8 | 16.13 |
| M4 | 0.91 | 0.83 | 6.1 | 32.1 | 9.99 |
| M5 | 0.78 | 0.61 | 5.2 | 43.4 | 12.5 |
| M6 | 0.73 | 0.53 | 4.8 | 34.2 | 10.07 |
| M7 | 0.67 | 0.45 | 5.5 | 46.2 | 13.21 |
| M8 | 0.84 | 0.71 | 4.0 | 39.9 | 11.36 |

### Output Result (`result.csv`)
**Parameters:** Weights=`1,1,1,1,1`, Impacts=`+,+,-,+,+`

| Model | P1 | P2 | P3 | P4 | P5 | Topsis Score | Rank |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | 0.87 | 0.76 | 5.1 | 69.9 | 19.16 | **0.8467** | **1** |
| **M3** | 0.83 | 0.69 | 5.2 | 57.8 | 16.13 | **0.6700** | **2** |
| **M8** | 0.84 | 0.71 | 4.0 | 39.9 | 11.36 | **0.5056** | **3** |
| **M4** | 0.91 | 0.83 | 6.1 | 32.1 | 9.99 | **0.4258** | **4** |
| **M5** | 0.78 | 0.61 | 5.2 | 43.4 | 12.5 | **0.4087** | **5** |
| **M7** | 0.67 | 0.45 | 5.5 | 46.2 | 13.21 | **0.3209** | **6** |
| **M6** | 0.73 | 0.53 | 4.8 | 34.2 | 10.07 | **0.2840** | **7** |
| **M2** | 0.60 | 0.36 | 6.6 | 35.3 | 10.72 | **0.0602** | **8** |

### Result Visualization
The bar chart below compares the TOPSIS Performance Score of different models.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#4a90e2'}}}%%
gantt
    title TOPSIS Score Ranking
    dateFormat X
    axisFormat %s
    
    section Models
    M1 (Rank 1) : 0, 85
    M3 (Rank 2) : 0, 67
    M8 (Rank 3) : 0, 51
    M4 (Rank 4) : 0, 43
    M5 (Rank 5) : 0, 41
    M7 (Rank 6) : 0, 32
    M6 (Rank 7) : 0, 28
    M2 (Rank 8) : 0, 6

---

## 🚀 How to Run

### Part 1: Using the CLI Script
This method allows you to run the TOPSIS algorithm directly from the command line using the local script.

1.  **Ensure Prerequisites:**
    Make sure you have `pandas` and `numpy` installed:
    ```bash
    pip install pandas numpy
    ```

2.  **Run the Script:**
    Navigate to the root directory and run the following command:
    ```bash
    # Syntax: python <script_path> <input_file> <weights> <impacts> <result_file>
    python Part_1_Script/topsis.py data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv
    ```

---

### Part 2: Using the PyPI Package
This method uses the published library, meaning you don't need the local code to run it.

1.  **Install the Package:**
    ```bash
    pip install Topsis-Vansh-102483084
    ```

2.  **Run via Command Line:**
    ```bash
    topsis data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv
    ```

3.  **Run via Python Script:**
    ```python
    from Topsis_Vansh_102483084.topsis import topsis
    
    # Arguments: Input File, Weights, Impacts, Output File
    topsis("data.csv", "1,1,1,1,1", "+,+,-,+,+", "result.csv")
    ```

---

### Part 3: Web Application
This launches a local web server with a graphical interface to upload files and receive results via email.

1.  **Navigate to the Web App Directory:**
    ```bash
    cd Part_3_Web_App
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables (Crucial):**
    Since sensitive credentials are not uploaded to GitHub, you must create a `.env` file locally.
    * Create a file named `.env` inside the `Part_3_Web_App` folder.
    * Add the following lines (replace with your actual App Password):
    ```text
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASSWORD=your_16_digit_app_password
    ```

4.  **Start the Server:**
    ```bash
    python app.py
    ```

5.  **Access the App:**
    Open your web browser and go to: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
---

## 📜 License
This project is licensed under the MIT License.
