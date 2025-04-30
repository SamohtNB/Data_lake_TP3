import pymysql
import pymongo
from transformers import AutoTokenizer
from datetime import datetime

# Connect to MySQL database

mysql_conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='staging'
)

cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT * FROM texts")
rows = cursor.fetchall()

# Connect to MongoDB database
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["curated"]
mongo_collection = mongo_db["wikitexts"]

#tokenizer initialization
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# process and insert into MongoDB
for row in rows:
    tokens = tokenizer(row['text'], truncation=True, padding=True, max_length=128)["input_ids"]
    mongo_doc = {
        "id" : row['id'],
        "text": row['text'],
        "tokens": tokens,
        "metadata": {
            "source": "mysql    ",
            "processed_at":     datetime.utcnow().isoformat()
        }
    }
    mongo_collection.insert_one(mongo_doc)

print(f"Data successfully inserted into MongoDB collection '{mongo_collection.name}'")

cursor.close()
mysql_conn.close()
