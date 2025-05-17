import pandas as pd

def sanitize_dataframe(df: pd.DataFrame) -> list[dict]:
    # Replace missing and infinite values
    df = df.replace({pd.NA: None, pd.NaT: None})
    df = df.replace([float("inf"), float("-inf")], None)
    df = df.fillna(pd.NA).astype(object)

    # Convert datetime columns to ISO 8601 strings
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S')

    return df.to_dict(orient="records")