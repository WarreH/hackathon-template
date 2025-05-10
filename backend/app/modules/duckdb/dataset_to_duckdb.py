from datasets import load_dataset
from duckdb import DuckDBPyConnection

SOURCE_DATASET =  "source_dataset"

def load_dataset_in_duckdb(duck: DuckDBPyConnection):
    # Check if the table exists
    table_exists = duck.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{SOURCE_DATASET}'").fetchone()[0]
    if table_exists != 0:
        return

    print("Loading ..")  # fixme replace with logger

    # Load a Hugging Face dataset, e.g., 'imdb'
    dataset = load_dataset("ns2agi/antwerp-osm-navigator")

    # Convert to pandas DataFrame
    train_split = dataset["train"]  # Is required for to_pandas method
    df = train_split.to_pandas()

    # Load into DuckDB as a table
    duck.execute(f"CREATE TABLE {SOURCE_DATASET} AS SELECT * FROM df")
    print("Done!")
    print(duck.execute(f"DESCRIBE SELECT * FROM {SOURCE_DATASET}").df())
