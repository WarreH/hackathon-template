from datasets import load_dataset

def load_dataset_in_duckdb(duck):
    print("Loading ..")  # fixme replace with logger

    # Load a Hugging Face dataset, e.g., 'imdb'
    dataset = load_dataset("ns2agi/antwerp-osm-navigator")

    # Convert to pandas DataFrame
    train_split = dataset["train"]  # Is required for to_pandas method
    df = train_split.to_pandas()

    # Load into DuckDB as a table
    duck.execute("CREATE TABLE source_dataset AS SELECT * FROM df")
    print("Done!")
