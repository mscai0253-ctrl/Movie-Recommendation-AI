import pandas as pd

def load_movies():
    df = pd.read_csv("data/movies.csv")

    # 🔥 Clean columns completely
    df.columns = df.columns.str.strip().str.lower()

    print("Columns found:", df.columns.tolist())

    # 🔥 Fix title column
    if "series_title" in df.columns:
        df.rename(columns={"series_title": "title"}, inplace=True)

    # 🔥 Handle genres column variations
    if "genres" not in df.columns:
        for col in df.columns:
            if "genre" in col:   # match genre / genres / Genre
                df.rename(columns={col: "genres"}, inplace=True)
                break

    # 🔥 Final safety check
    if "title" not in df.columns:
        raise Exception(f"Title column missing. Found: {df.columns.tolist()}")

    if "genres" not in df.columns:
        raise Exception(f"Genres column missing. Found: {df.columns.tolist()}")

    # Fill missing values
    df["genres"] = df["genres"].fillna("")

    return df