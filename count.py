import os
import time
import pickle
from collections import Counter
from pathlib import Path

from Bio import Entrez
import pandas as pd
from tqdm import tqdm  # progress meter

# Configuration
Entrez.email = "your.name@example.com"  # replace with your email
results_dir = Path("./results")
results_dir.mkdir(exist_ok=True)
cache_file = results_dir / "radiomics_2025_ids.pkl"
output_file = results_dir / "journals2025.xlsx"

# Step 1: Fetch or load cached PubMed IDs
def fetch_ids():
    if cache_file.exists():
        with open(cache_file, "rb") as f:
            ids = pickle.load(f)
    else:
        handle = Entrez.esearch(
            db="pubmed",
            term="radiomics AND 2025[PDAT]",
            retmax=10000,
        )
        record = Entrez.read(handle)
        ids = record["IdList"]
        handle.close()

        with open(cache_file, "wb") as f:
            pickle.dump(ids, f)
    return ids

# Step 2: Fetch journal titles with progress bar
def fetch_journal_titles(ids):
    journals = []
    batch_size = 100
    n_batches = len(ids) // batch_size + int(len(ids) % batch_size > 0)

    for i in tqdm(range(n_batches), desc="Fetching journal names"):
        start = i * batch_size
        end = start + batch_size
        fetch_handle = Entrez.efetch(
            db="pubmed",
            id=ids[start:end],
            rettype="medline",
            retmode="text"
        )
        articles = fetch_handle.read().split("\n\n")
        for article in articles:
            for line in article.split("\n"):
                if line.startswith("JT  -"):
                    journals.append(line.replace("JT  - ", "").strip())
                    break
        time.sleep(0.34)  # be kind to the API
    return journals

# Step 3: Count journals and save to Excel
def save_journal_counts(journals):
    counter = Counter(journals)
    df = pd.DataFrame(counter.items(), columns=["Journal", "Number of Radiomics Papers"])
    df.sort_values(by="Number of Radiomics Papers", ascending=False, inplace=True)
    df.to_excel(output_file, index=False)

# Main execution
if __name__ == "__main__":
    ids = fetch_ids()
    journals = fetch_journal_titles(ids)
    save_journal_counts(journals)
    print(f"\n✅ Saved results to {output_file.resolve()}")
