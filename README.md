# 📒 Real Estate Price Prediction

This project aims to predict real estate prices using machine learning models. The system provides users with insights into property prices based on various features such as location, property type, living area, and more.

## 📦 Directory Structure

- **api**: Contains files related to the FastAPI-based API used for real estate price prediction.
  - `app.py`: Defines the FastAPI application and API endpoints for predicting property prices.
  - `Dockerfile`: Dockerfile for containerizing the FastAPI application.
  - `light_gbm.pkl`: Trained LightGBM model for price prediction.
  - `requirements.txt`: List of Python dependencies required for the API.
  - `utils.py`: Utility functions and preprocessing pipeline for data processing.

- **streamlit**: Includes files for the Streamlit web application used for interacting with the prediction model.
  - `requirements.txt`: List of Python dependencies required for the Streamlit app.
  - `streamlit_app.py`: Streamlit web application for user input and displaying predicted property prices.

```
Repo structure:
.
├── api
│   ├──files/
│   ├── app.py
│   ├── Dockerfile
│   ├──light_gbm.pkl
│   ├── requirements.txt
│   └──utils.py
├── streamlit
│   ├── requirements.txt
│   └── streamlit_app.py
```

## 🎮 Usage

### API
1. Navigate to the `api` directory.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the FastAPI application using `uvicorn app:app --host 0.0.0.0 --port 8000`.
4. Access the API at `http://localhost:8000`.

### Streamlit Web Application
1. Navigate to the `streamlit` directory.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the Streamlit web application using `streamlit run streamlit_app.py`.
4. Access the web application at the provided URL.

## 📊 Data and Model Sources

- **Raw Data**: The raw data for training the machine learning models was obtained from a web scraping project available [here](https://github.com/bear-revels/immo-eliza-scraping-Python_Pricers.git).
- **Model Training**: The machine learning models were trained and evaluated using data preprocessing techniques and training scripts available [here](https://github.com/bear-revels/immo-ml.git).

## ⏱️ Project Timeline

This project was completed over a span of 5 days, including data collection, model training, and web application development.

## 💬 Connect with the Programmer

For any inquiries, feedback, or collaborations, please reach out to the programmer, [Bear Revels](https://www.linkedin.com/in/bear-revels/).

## 📌 Web Application URLs

- **Streamlit Web App**: [https://immo-deployment-bear-revels.streamlit.app/](https://immo-deployment-bear-revels.streamlit.app/)
- **API Endpoint (FastAPI)**: [https://immo-deployment.onrender.com/](https://immo-deployment.onrender.com/)

