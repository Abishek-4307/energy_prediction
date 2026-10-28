from pathlib import Path

import numpy as np
import pandas as pd


def load_data(sample_size=2000, chunksize=50000):
    """Load a representative sample using limited memory."""

    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "household_power_consumption.txt"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    required_columns = [
        "Time",
        "Global_active_power",
        "Global_intensity",
        "Voltage",
    ]

    samples = []
    numeric_columns = [
        "Global_active_power",
        "Global_intensity",
        "Voltage",
    ]

    reader = pd.read_csv(
        file_path,
        sep=";",
        usecols=required_columns,
        chunksize=chunksize,
        low_memory=False,
    )

    for chunk_number, chunk in enumerate(reader):
        chunk.columns = chunk.columns.str.strip()

        for column in numeric_columns:
            chunk[column] = pd.to_numeric(
                chunk[column].replace("?", np.nan),
                errors="coerce",
            )

        chunk["Time"] = pd.to_datetime(
            chunk["Time"],
            format="%H:%M:%S",
            errors="coerce",
        )

        chunk["Hour"] = chunk["Time"].dt.hour

        chunk.dropna(
            subset=[
                "Hour",
                "Global_active_power",
                "Global_intensity",
                "Voltage",
            ],
            inplace=True,
        )

        if not chunk.empty:
            count = min(50, len(chunk))

            samples.append(
                chunk.sample(
                    n=count,
                    random_state=42 + chunk_number,
                )
            )

    if not samples:
        raise ValueError(
            "No valid energy consumption records were found."
        )

    data = pd.concat(samples, ignore_index=True)

    if len(data) > sample_size:
        data = data.sample(
            n=sample_size,
            random_state=42,
        )

    data.reset_index(drop=True, inplace=True)

    # Preserve the existing feature-generation approach.
    rng = np.random.default_rng(42)

    data["Global_active_power"] *= (
        1 + rng.normal(0, 0.2, len(data))
    )

    data["Random_noise"] = rng.normal(
        0, 1, len(data)
    )

    print(f"Loaded {len(data)} energy records.")

    return data
