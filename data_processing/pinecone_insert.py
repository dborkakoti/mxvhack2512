import os
import glob
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY not found in environment variables")

pc = Pinecone(api_key=api_key)

print("Check the index, and create if needed")
index_name = "mxvtravel"

existing_indexes = [i.name for i in pc.list_indexes()]

if index_name not in existing_indexes:
    print(f"Creating index {index_name}...")
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "llama-text-embed-v2",
            "field_map": {"text": "text"}
        }
    )
else:
    print(f"Index {index_name} already exists.")

print("Chunk the texts")

chunk_size = 200
overlap = 50
out = []

# Directory containing policy files
policies_dir = os.path.join(os.path.dirname(__file__), "../policies")
policy_files = glob.glob(os.path.join(policies_dir, "*.md"))

for policy_path in policy_files:
    filename = os.path.basename(policy_path)
    policy_type = os.path.splitext(filename)[0]
    print(f"Processing {filename}...")
    
    with open(policy_path, "r", encoding="utf-8") as inf:
        i = 0
        while True:
            chunk = inf.read(chunk_size)
            if not chunk:
                break
            
            out.append({
                "_id": f"{policy_type}_rec{i}",
                "text": chunk,
                "policy_type": policy_type
            })
            
            if len(chunk) < chunk_size:
                break
            
            inf.seek(inf.tell() - overlap)
            i += 1

print(f"Upserting {len(out)} records")
dense_index = pc.Index(index_name)

batch_size = 50
for i in range(0, len(out), batch_size):
    batch = out[i:i+batch_size]
    print(f"Upserting batch {i//batch_size + 1} ({len(batch)} records)...")
    dense_index.upsert_records("policy", batch)
