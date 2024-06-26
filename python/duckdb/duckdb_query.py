# -*- coding=utf-8 -*-
"""
https://docs.flyte.org/en/latest/flytesnacks/examples/duckdb_plugin/duckdb_example.html
"""
import json
from typing import List

import pandas as pd
import pyarrow as pa
from flytekit import kwtypes, task, workflow
from flytekit.types.structured.structured_dataset import StructuredDataset
from flytekitplugins.duckdb import DuckDBQuery
from typing_extensions import Annotated

# StructuredDataset-compatible type
simple_duckdb_query = DuckDBQuery(
    name="simple_task",
    query="SELECT SUM(a) FROM mydf",
    inputs=kwtypes(mydf=pd.DataFrame),
)


def get_pandas_df() -> pd.DataFrame:
    return pd.DataFrame({"a": [1, 2, 3]})


def pandas_wf() -> pd.DataFrame:
    return simple_duckdb_query(mydf=get_pandas_df())


def arrow_wf() -> pa.Table:
    return simple_duckdb_query(mydf=get_pandas_df())


# SQL query on Parquet file
parquet_duckdb_query = DuckDBQuery(
    name="parquet_query",
    query=[
        "INSTALL httpfs",
        "LOAD httpfs",
        """SELECT hour(lpep_pickup_datetime) AS hour, count(*) AS count FROM READ_PARQUET(?) GROUP BY hour""",
    ],
    inputs=kwtypes(params=List[str]),
)


def parquet_wf(parquet_file: str) -> pd.DataFrame:
    return parquet_duckdb_query(params=[parquet_file])


# SQL query on StructuredDataset
sd_duckdb_query = DuckDBQuery(
    name="sd_query",
    query="SELECT * FROM sd_df WHERE i = 2",
    inputs=kwtypes(sd_df=StructuredDataset),
)


def get_sd() -> StructuredDataset:
    return StructuredDataset(
        dataframe=pd.DataFrame.from_dict({"i": [1, 2, 3, 4], "j": ["one", "two", "three", "four"]})
    )


def sd_wf() -> pd.DataFrame:
    sd_df = get_sd()
    return sd_duckdb_query(sd_df=sd_df)


# Send parameters to multiple queries
duckdb_params_query = DuckDBQuery(
    name="params_query",
    query=[
        "CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)",
        "INSERT INTO items VALUES (?, ?, ?)",
        "SELECT $1 AS one, $1 AS two, $2 AS three",
    ],
    inputs=kwtypes(params=str),
)


def read_df(df: Annotated[StructuredDataset, kwtypes(one=str)]) -> pd.DataFrame:
    return df.open(pd.DataFrame).all()


def params_wf(
    params: str = json.dumps(
        [
            [["chainsaw", 500, 10], ["iphone", 300, 2]],
            ["duck", "goose"],
        ]
    ),
) -> pd.DataFrame:
    return read_df(df=duckdb_params_query(params=params))


if __name__ == "__main__":
    print(f"Running pandas_wf()... {pandas_wf()}")
    print(f"Running arrow_wf()... {arrow_wf()}")

    parquet_file = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-02.parquet"
    print(f"Running parquet_wf()... {parquet_wf(parquet_file=parquet_file)}")

    print(f"Running sd_wf()... {sd_wf()}")

    print(f"Running params_wf()... {params_wf()}")
