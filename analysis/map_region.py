import json
import pathlib
import pandas
import argparse


MEASURE_NUMERIC_COLUMNS = ["ratio", "numerator", "denominator"]


def get_msoa_to_region_mapping():
    # https://geoportal.statistics.gov.uk/datasets/ons::msoa-2021-to-bua-to-lad-to-region-december-2022-best-fit-lookup-in-ew-v2/about
    mapping_file = (
        pathlib.Path(__file__).parents[1]
        / "ONS-data"
        / "MSOA_(2021)_to_Built-up_Area_to_Local_Authority_District_to_Region_(December_2022)_Lookup_in_England_and_Wales_v2.geojson"
    )
    with open(mapping_file) as f:
        geojson = json.load(f)
    return {
        feature["properties"]["MSOA21CD"]: feature["properties"]["RGN22NM"]
        for feature in geojson["features"]
    }


def read_csv(path):
    data = pandas.read_csv(path, dtype=str)
    for column in MEASURE_NUMERIC_COLUMNS:
        if column in data.columns:
            data[column] = pandas.to_numeric(data[column])
    return data


def map_dataset(src_path, dest_path, mapping):
    dataset = read_csv(src_path)
    dataset["region"] = dataset["msoa_code"].map(mapping)
    dataset.drop(columns=["msoa_code"], inplace=True)
    dataset.to_csv(dest_path, index=False)


def _get_groupby(measure_dataframe):
    columns = [c for c in measure_dataframe.columns if c not in MEASURE_NUMERIC_COLUMNS]
    empty_cols = [c for c in columns if measure_dataframe.loc[:, c].isna().all()]
    groupby = [c for c in columns if c not in empty_cols]
    return groupby, empty_cols


def map_measure(src_path, dest_path, mapping):
    measure = read_csv(src_path)
    non_geographic_rows = measure[measure["msoa_code"].isna()].copy()
    non_geographic_rows.rename(columns={"msoa_code": "region"}, inplace=True)
    # These rows then have the columns in the order the original study outputs do
    column_order = list(non_geographic_rows.columns)

    msoa_rows = measure.dropna(subset=["msoa_code"]).copy()
    msoa_rows["region"] = msoa_rows["msoa_code"].map(mapping)
    msoa_rows.drop(columns=["msoa_code"], inplace=True)
    groupby, empty_cols = _get_groupby(msoa_rows)
    msoa_rows.drop(columns=empty_cols, inplace=True)
    region_rows = msoa_rows.groupby(groupby).sum().reset_index()
    region_rows["ratio"] = region_rows["numerator"] / region_rows["denominator"]
    for col in empty_cols:
        region_rows[col] = None
    measure = pandas.concat([region_rows, non_geographic_rows])
    measure.loc[:, column_order].to_csv(dest_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map MSOA codes to regions")
    parser.add_argument(
        "--file-type",
        type=str,
        help="File type (dataset or measure)",
        choices=["dataset", "measure"],
        required=True,
    )
    parser.add_argument(
        "--src-path", type=str, help="Path to the file to map", required=True
    )
    parser.add_argument(
        "--dest-path", type=str, help="Path to save the mapped file", required=True
    )
    args = parser.parse_args()

    pathlib.Path(args.dest_path).parent.mkdir(parents=True, exist_ok=True)

    mapping = get_msoa_to_region_mapping()
    if args.file_type == "dataset":
        map_dataset(args.src_path, args.dest_path, mapping)
    elif args.file_type == "measure":
        map_measure(args.src_path, args.dest_path, mapping)
