from src.transform import transform

SAMPLE = [
    {"Ccy": "USD", "CcyNm_EN": "US Dollar", "Nominal": "1", "Rate": "12000.50", "Diff": "-10.2", "Date": "25.09.2026"},
    {"Ccy": "JPY", "CcyNm_EN": "Japan Yen", "Nominal": "100", "Rate": "8000", "Diff": "5", "Date": "25.09.2026"},
    {"Ccy": "XXX", "CcyNm_EN": "Broken", "Nominal": "1", "Rate": "", "Diff": "0", "Date": "25.09.2026"},
]


def test_cleans_and_normalises():
    df = transform(SAMPLE)
    assert list(df["currency"]) == ["USD", "JPY"]          # broken row dropped
    assert df.loc[df.currency == "JPY", "rate_per_unit"].iloc[0] == 80.0
    assert df["rate_date"].iloc[0] == "2026-09-25"


def test_empty_input():
    assert transform([]).empty
