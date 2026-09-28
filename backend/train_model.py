from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


EXPECTED_FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]

TARGET_COLUMN = "Product_Store_Sales_Total"


def prepare_training_data(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()

    if "Product_Id_char" not in prepared.columns and "Product_Id" in prepared.columns:
        prepared["Product_Id_char"] = prepared["Product_Id"].astype(str).str.extract(r"([A-Za-z]+)", expand=False)

    if "Product_Type_Category" not in prepared.columns and "Product_Type" in prepared.columns:
        prepared["Product_Type_Category"] = prepared["Product_Type"]

    if "Store_Age_Years" not in prepared.columns and "Store_Establishment_Year" in prepared.columns:
        current_year = pd.Timestamp.now().year
        prepared["Store_Age_Years"] = current_year - pd.to_numeric(
            prepared["Store_Establishment_Year"], errors="coerce"
        )

    missing = [c for c in EXPECTED_FEATURES + [TARGET_COLUMN] if c not in prepared.columns]
    if missing:
        raise ValueError(f"Training data is missing required columns: {', '.join(missing)}")

    return prepared


def main() -> None:
    root = Path(__file__).resolve().parent
    data_path = root.parent / "data" / "train.csv"
    model_path = root / "model" / "superkart_model.joblib"

    df = pd.read_csv(data_path, comment="#")
    prepared = prepare_training_data(df)

    X = prepared[EXPECTED_FEATURES]
    y = prepared[TARGET_COLUMN]

    categorical = [
        "Product_Sugar_Content",
        "Store_Size",
        "Store_Location_City_Type",
        "Store_Type",
        "Product_Id_char",
        "Product_Type_Category",
    ]
    numeric = [
        "Product_Weight",
        "Product_Allocated_Area",
        "Product_MRP",
        "Store_Age_Years",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("prep", preprocessor),
            ("model", RandomForestRegressor(n_estimators=200, random_state=42)),
        ]
    )

    pipeline.fit(X, y)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)

    print(f"Saved model to {model_path}")


if __name__ == "__main__":
    main()
