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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Télécharger et sauvegarder le dataset Wikitext")
    parser.add_argument("--output_dir", required=True, help="Répertoire de sortie pour les fichiers texte")
    args = parser.parse_args()

    # Appeler la fonction avec le répertoire de sortie spécifié
    dataset.download_and_save(args.output_dir)
    print(f"Dataset téléchargé et sauvegardé dans {args.output_dir}")