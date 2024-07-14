import os
import pandas as pd


def assemble_csvs_to_dataframe(data_folder="data"):
    all_data = []

    for root, _, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".csv"):
                country = file.split(".")[0]
                date = os.path.basename(root)
                file_path = os.path.join(root, file)

                # Read the CSV file
                df = pd.read_csv(file_path)

                # Rename columns to a common format
                df.columns = ["Time", "Import_to_UA", "Export_from_UA"]

                # Add the country and date columns
                df["Country"] = country
                df["Date"] = date

                all_data.append(df)

    # Concatenate all dataframes
    final_df = pd.concat(all_data, ignore_index=True)

    return final_df


def export_dataframe_to_json(df, output_file="output.json"):
    df.to_json(output_file, orient="records", date_format="iso", indent=2)


def group_daily(df):
    return (
        df.groupby(["Date", "Country"])[["Export_from_UA", "Import_to_UA"]]
        .sum()
        .reset_index()
    )


if __name__ == "__main__":
    df = assemble_csvs_to_dataframe().sort_values(["Date", "Country"])
    df_daily = group_daily(df)
    export_dataframe_to_json(df)
    export_dataframe_to_json(df_daily, "output_daily.json")
    print(f"Data successfully exported to output.json")
