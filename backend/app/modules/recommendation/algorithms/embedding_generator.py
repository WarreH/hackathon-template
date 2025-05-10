import json

import pandas as pd
from datasets import load_dataset
import numpy as np
from tqdm import tqdm
import torch
from sentence_transformers import SentenceTransformer, util


# FOR TESTING
def load_and_process_osm_data(dataset_name="ns2agi/antwerp-osm-navigator"):
    print(f"Loading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name)

    print("\nDataset structure:")
    print(dataset)

    train_split = dataset["train"]

    print("\nFiltering for 'node' types and entries with non-empty tags...")
    node_dataset = train_split.filter(lambda example: example["type"] == "node" and example["tags"] and example["tags"] !="{}")
    print(f"Found {len(node_dataset)} nodes with non-empty tags.")

    print("\nConverting the nodes to a pandas DataFrame...")
    df = node_dataset.select(range(100)).to_pandas()
    print(df.head())
    return df

def build_tag_embedding_matrix(df):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 1: Collect all tag keys
    all_keys = set()
    all_values = set()

    for tags in df["tags"]:
        for k, v in json.loads(tags).items():
            all_keys.add(k)
            all_values.add(v)

    all_keys = sorted(all_keys)
    all_values = sorted(all_values)

    # Step 2: Embed all values once
    value_to_embedding = {}
    batch_size = 64
    for i in tqdm(range(0, len(all_values), batch_size), desc="Embedding values"):
        batch = all_values[i:i+batch_size]
        embeddings = model.encode(batch, show_progress_bar=False)
        for val, emb in zip(batch, embeddings):
            value_to_embedding[val] = emb

    embedding_dim = model.get_sentence_embedding_dimension()
    zero_vec = np.zeros(embedding_dim)

    row_embeddings = []

    for idx, tags in tqdm(df["tags"].items(), desc="Processing rows"):
        tags = json.loads(tags)
        if len(tags) == 0:
            print(f"Skipping row {idx} because tags are empty")
            continue
        row_vector = []
        for key in all_keys:
            val = tags.get(key, None)
            vec = value_to_embedding.get(val, zero_vec)
            row_vector.append(vec)
        if len(row_vector) > 0:
            row_embeddings.append(np.concatenate(row_vector))
        else:
            print(f"Skipping row {idx} due to missing values for all keys")

    # Check if any valid embeddings were collected
    if len(row_embeddings) == 0:
        raise ValueError("No valid embeddings were created. Check data filtering or tag values.")

    embedding_matrix = np.vstack(row_embeddings)

    # Step 4: Create column names like amenity_0, amenity_1, ...
    column_names = []
    for key in all_keys:
        column_names.extend([f"{key}_{i}" for i in range(embedding_dim)])

    # Step 5: Create DataFrame
    embedding_df = pd.DataFrame(embedding_matrix, columns=column_names)

    # Step 6: Save to CSV
    # csv_filename = "osm_tag_embeddings.csv"
    # embedding_df.to_csv(csv_filename, index=False)
    # print(f"Saved embedding DataFrame to '{csv_filename}'.")

    return embedding_df, all_keys



def find_closest_entries_by_tag_match(embedding_df,all_keys, keyword, top_k=20):

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding_dim = model.get_sentence_embedding_dimension()
    keyword_emb = model.encode(keyword, convert_to_tensor=True, normalize_embeddings=True)

    # Splitting tag embeddings per tag key...
    tag_slices = {key: (i * embedding_dim, (i + 1) * embedding_dim) for i, key in enumerate(all_keys)}

    embedding_tensor = torch.tensor(embedding_df.values, dtype=torch.float32)
    embedding_tensor = torch.nn.functional.normalize(embedding_tensor, p=2, dim=1)

    max_scores = []

    for idx in tqdm(range(len(embedding_tensor)), desc="Computing max similarity per row"):
        row_emb = embedding_tensor[idx]
        max_sim = -1.0
        for key, (start, end) in tag_slices.items():
            tag_vec = row_emb[start:end].unsqueeze(0)
            sim = util.cos_sim(keyword_emb, tag_vec).item()
            if sim > max_sim:
                max_sim = sim
        max_scores.append((idx, max_sim))

    top_results = sorted(max_scores, key=lambda x: x[1], reverse=True)[:top_k]
    return  top_results


def apply_cosine_simularity(df,keywords):
    # Generate embeddings for the tags
    embedding_df, tag_keys = build_tag_embedding_matrix(df)

    matches = []
    for keyword in keywords:
        top_matches = find_closest_entries_by_tag_match(embedding_df, tag_keys, keyword, top_k=20)
        matches.extend(top_matches)

    top_results = sorted(matches, key=lambda x: x[1], reverse=True)[:20]
    indexes = [i for i, _ in top_results]
    return df.iloc[indexes]

#  For testing
# if __name__ == "__main__":
#     # Load and process OSM data
#     osm_dataframe = load_and_process_osm_data()
#
#     # Generate embeddings for the tags
#     embedding_df, tag_keys = build_tag_embedding_matrix(osm_dataframe)
#
#     top_matches = find_closest_entries_by_tag_match(embedding_df,tag_keys, "cycling",top_k=20)
#
#     indexes = [i for i,_ in top_matches]
#     print(osm_dataframe.iloc[indexes].head())