import boto3
import os
import mysql.connector

def preprocess_to_staging(bucket_raw, db_host, db_user, db_password, db_name):
    
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="root",
        aws_secret_access_key="root",
        region_name="us-east-1",
        verify=False
    )
    
    combined_texts = s3.get_object(
        Bucket=bucket_raw,
        Key="combined_text.txt"
    )["Body"].read().decode("utf-8")
    
    combined_texts = combined_texts.split("\n")    
    combined_texts = [text for text in combined_texts if text.strip() != ""]

    conn = mysql.connector.connect(database = db_name, host=db_host, user=db_user, password=db_password)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text TEXT NOT NULL
        )
    ''')
    for text in combined_texts:
        cursor.execute('INSERT INTO texts (text) VALUES (%s)', (text,))

        
    cursor.execute('SELECT * FROM texts WHERE text IS NOT NULL')

    if cursor.fetchone() is None:
        print("Aucune ligne insérée dans la table.")
    else:
        _ = cursor.fetchall()
        print("Lignes insérées dans la table.")
        
        cursor.execute('SELECT count(*) FROM texts WHERE text IS NOT NULL')
        print(f"Nombre de lignes insérées : {cursor.fetchone()[0]}")
        
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prétraitement et insertion dans la base de données")
    parser.add_argument("--bucket_raw", required=True, help="Nom du bucket S3 brut")
    parser.add_argument("--db_host", required=True, help="Hôte de la base de données")
    parser.add_argument("--db_user", required=True, help="Utilisateur de la base de données")
    parser.add_argument("--db_password", required=True, help="Mot de passe de la base de données")
    parser.add_argument("--db_name", required=True, help="Nom de la base de données")
    
    args = parser.parse_args()  

    preprocess_to_staging(args.bucket_raw, args.db_host, args.db_user, args.db_password, args.db_name)
    