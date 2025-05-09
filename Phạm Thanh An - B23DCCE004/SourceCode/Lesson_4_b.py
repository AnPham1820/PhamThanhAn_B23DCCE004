import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.impute import KNNImputer
from xgboost import XGBRegressor
import warnings

warnings.filterwarnings("ignore")

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    
    df["Age"] = df["Age"].apply(lambda x: int(str(x).split("-")[0]) if pd.notna(x) and "-" in str(x) else np.nan)
    
    imputer = KNNImputer(n_neighbors=3)
    df[["Age", "Goals", "Assists"]] = imputer.fit_transform(df[["Age", "Goals", "Assists"]])
    df["Age"] = df["Age"].astype(int)
    
    df["Goals_x_Assists"] = df["Goals"] * df["Assists"]
    
    return df

df = load_and_preprocess_data("results_bai_4.csv")

numeric_features = ["Age", "Goals", "Assists", "Goals_x_Assists"]
categorical_features = ["Position"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

X = df.drop(columns=["ETV", "Name"])
y = df["ETV"].str.replace("€", "").str.replace("M", "").astype(float)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", XGBRegressor(random_state=42))
])

param_grid = {
    "regressor__n_estimators": [200, 300],
    "regressor__max_depth": [6, 8, 10],
    "regressor__learning_rate": [0.01, 0.1],
    "regressor__subsample": [0.8, 1.0],
    "regressor__colsample_bytree": [0.8, 1.0]
}

grid_search = GridSearchCV(
    model, 
    param_grid, 
    cv=5, 
    scoring="r2",
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"✅ Best Parameters: {grid_search.best_params_}")
print(f"✅ R² Score: {r2:.4f}")
print(f"✅ MAE: {mae:.2f}")

feature_names = numeric_features + list(
    best_model.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out()
)
importances = best_model.named_steps["regressor"].feature_importances_