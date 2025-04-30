import boto3
import os
import sqlite3

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
        Key="data/raw/combined_text.txt"
    )["Body"].read().decode("utf-8")
    
    combined_texts = combined_texts.split("\n")    
    combined_texts = [text for text in combined_texts if text.strip() != ""]

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')
    for text in combined_texts:
        cursor.execute('INSERT INTO texts (text) VALUES (?)', (text,))
        
    cursor.execute('SELECT * FROM texts WHERE text IS NOT NULL')
    if cursor.fetchone() is None:
        print("Aucune ligne insérée dans la table.")
    else:
        print("Lignes insérées dans la table.")
        
        cursor.execute('SELECT count(*) FROM texts WHERE text IS NOT NULL')
        print(f"Nombre de lignes insérées : {cursor.fetchone()[0]}")
        
    conn.commit()
    conn.close()
    