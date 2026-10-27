# ⚡ Smart Energy Consumption Prediction System

A web-based machine learning application built with **Django** and **scikit-learn** that predicts household daily energy consumption, estimates electricity bills according to TNEB tariff slabs, visualizes 24-hour load patterns, and compares regression models.

---

## 📌 Features

- **Interactive Sliders**: Real-time adjustment of Voltage (200V – 250V) and Current Intensity (0A – 20A).
- **ML-Powered Energy Forecasting**:
  - Predicts 24-hour hourly energy distribution.
  - Multi-model evaluation comparing **Ridge Regression**, **Decision Tree Regressor**, and **Random Forest Regressor** using $R^2$ scores.
  - Peak-usage window detection (e.g., peak demand hours).
- **Automated Bill Calculation**: Computes estimated bi-monthly electricity bills using the supplied domestic tariff slabs.
- **Smart Usage Recommendations**: Provides dynamic, actionable energy conservation tips based on current electrical intensity.
- **Visual Hourly Breakdown**: Responsive CSS bar chart showing predicted energy usage across every hour of the day.
- **In-Memory Model Caching**: Loads and trains the dataset once on initial request to deliver sub-second predictions without retraining.

---

## 📁 Project Structure

```text
energy_prediction_project/
│
├── data/
│   └── household_power_consumption.txt   # UCI Household Electric Power Consumption dataset
│
├── django_project/                       # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                       # Project settings
│   ├── urls.py                           # Root URL routing
│   └── wsgi.py
│
├── energy/                               # Django application
│   ├── templates/
│   │   └── energy/
│   │       ├── index.html                # Main dashboard UI
│   │       └── results.html              # Dynamic results fragment (AJAX)
│   ├── apps.py
│   ├── urls.py                           # App URL routes
│   └── views.py                          # Prediction logic, caching, & export views
│
├── src/                                  # Machine Learning & utility modules
│   ├── __init__.py
│   ├── data_loader.py                    # Dataset loading, cleaning, & feature extraction
│   ├── model.py                          # Model definitions & training (Ridge, DT, RF)
│   ├── bill.py                           # TNEB electricity bill slab calculation
│   └── utils.py
│
├── db.sqlite3                            # SQLite database
├── manage.py                             # Django CLI management script
├── requirements.txt                      # Project dependencies
└── README.md                             # Project documentation
```

---

## ⚙️ Machine Learning Pipeline

1. **Dataset**: Sampled from the Household Power Consumption dataset (`household_power_consumption.txt`).
2. **Features**:
   - `Hour`: Time of day (0 to 23)
   - `Voltage`: Household voltage level
   - `Global_intensity`: Current intensity (in Amperes)
   - `Random_noise`: Realistic disturbance factor
3. **Target Variable**: `Global_active_power` (kilowatts)
4. **Trained Models**:
   - **Ridge Regression** (`alpha=20`)
   - **Decision Tree Regressor** (`max_depth=4`, `min_samples_leaf=10`)
   - **Random Forest Regressor** (`n_estimators=40`, `max_depth=5`, `min_samples_leaf=8`)

---

## 🧾 Domestic Tariff Slabs (Bi-Monthly)

The estimated bi-monthly consumption is calculated as daily energy multiplied by 60. The tariff is progressive within each tier:

| Total bi-monthly consumption | Slab units | Rate per unit (₹) |
| :--- | :--- | :--- |
| Up to 500 units | 1–200 | Free |
| Up to 500 units | 201–400 | 4.70 |
| Up to 500 units | 401–500 | 6.30 |
| Above 500 units | 1–100 | Free |
| Above 500 units | 101–400 | 4.70 |
| Above 500 units | 401–500 | 6.30 |
| Above 500 units | 501–600 | 8.40 |
| Above 500 units | 601–800 | 9.45 |
| Above 500 units | 801–1,000 | 10.50 |
| Above 500 units | Above 1,000 | 11.55 |

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.9+** or **Anaconda**
- Recommended virtual environment or conda environment

### 2. Clone / Navigate to Directory
```powershell
cd d:\energy_prediction_project
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

*Required packages:*
- `django>=4.2`
- `pandas`
- `numpy`
- `matplotlib`
- `scikit-learn`

### 4. Apply Database Migrations
```powershell
python manage.py migrate
```

### 5. Run the Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 🌐 Application URL

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Main prediction dashboard |

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Django
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **Frontend**: HTML5, Vanilla CSS, JavaScript (Fetch API / AJAX)
