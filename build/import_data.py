from datasets import load_dataset

# Télécharger le dataset
dataset = load_dataset("wikitext", "wikitext-2-raw-v1")

# Sauvegarder localement dans data/raw/train, data/raw/test, data/raw/dev
for split in ["train", "test", "validation"]:
    data = dataset[split]
    path = f"data/raw/{split}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(data["text"]))
    print(f"Saved {split} data to {path}")
