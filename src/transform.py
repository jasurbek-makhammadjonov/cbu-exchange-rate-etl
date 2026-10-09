"""Transform: clean raw CBU data into a tidy DataFrame."""
import pandas as pd

COLUMNS = {
    "Ccy": "currency",
    "CcyNm_EN": "currency_name",
    "Nominal": "nominal",
    "Rate": "rate",
    "Diff": "diff",
    "Date": "rate_date",
}


def transform(raw: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(raw)
    if df.empty:
        return pd.DataFrame(columns=[*COLUMNS.values(), "rate_per_unit"])

    df = df.rename(columns=COLUMNS)[list(COLUMNS.values())]
    for col in ("nominal", "rate", "diff"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["rate_date"] = pd.to_datetime(df["rate_date"], format="%d.%m.%Y").dt.strftime("%Y-%m-%d")
    df["currency"] = df["currency"].str.strip().str.upper()

    # Some currencies are quoted per 10/100 units: normalise to one unit.
    df["rate_per_unit"] = df["rate"] / df["nominal"]

    df = df.dropna(subset=["currency", "rate", "nominal"])
    df = df[df["nominal"] > 0]
    return df.drop_duplicates(subset=["rate_date", "currency"]).reset_index(drop=True)
