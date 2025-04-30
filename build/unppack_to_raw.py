import os
import boto3

def unpack_to_raw(input_dir, bucket_name, output_file_name):
    """
    Lit tous les fichiers .txt du répertoire input_dir, les concatène,
    les écrit dans un fichier temporaire, puis les envoie dans un bucket S3.

    Parameters:
    input_dir (str): Dossier contenant les fichiers .txt.
    bucket_name (str): Nom du bucket S3 (LocalStack).
    output_file_name (str): Nom du fichier de sortie dans le bucket S3.
    """

    list_texts = []

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                print(f"Lecture du fichier : {file_path}")
                
                # Lire le contenu du fichier et l'ajouter à la liste
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        list_texts.append(content)

    if list_texts:
        os.makedirs("data/raw", exist_ok=True)
        combined_path = os.path.join("data/raw", output_file_name)

        with open(combined_path, "w", encoding="utf-8") as f:
            f.write("".join(list_texts))  # Séparation optionnelle

        print(f"Fichier combiné sauvegardé localement : {combined_path}")

        s3 = boto3.client(
            "s3",
            endpoint_url="http://localhost:4566",
            aws_access_key_id="root",
            aws_secret_access_key="root",
            region_name="us-east-1",
            verify=False
        )

        s3.upload_file(
            Filename=combined_path,
            Bucket=bucket_name,
            Key=output_file_name
        )

        print(f"Fichier uploadé dans s3://{bucket_name}/{output_file_name}")
    else:
        print("Aucun fichier .txt trouvé dans le dossier.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Combine et upload des fichiers texte")
    parser.add_argument("--input_dir", required=True, help="Répertoire des fichiers texte")
    parser.add_argument("--bucket_name", required=True, help="Nom du bucket S3")
    parser.add_argument("--output_file_name", required=True, help="Nom du fichier uploadé")
    args = parser.parse_args()

    unpack_to_raw(args.input_dir, args.bucket_name, args.output_file_name)
