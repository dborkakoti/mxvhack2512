# Initial commit db

Project created, and synced between github and local folder.

# Initial commit of the project data, and the pinecone insert

Added the problem statement files. Segregated the problem statement, policy, and the xlsx files. Converted the policy files to md using [word2md](https://word2md.com) and added them to the `policies` folder.

Used a stub of the `upsert.py` file to create the pinecone insert script, on antigravity.

## Pinecone insert prompt

> Modify `upsert.py` to clean the code. Do things like not having api keys in the file, but in .env instead. Also, instead of the current input file, it should pick the md files in the folder `policies` . The files should be upserted into the pinecone database with id, text, and field for the type of policy (given by the file name).

# Initial front end

Just created a minimum app.

## Prompt
> Use fastapi to create a minimal app to provide a chat interface. For now the backend should return "hello". Use a simple sqlite3 db as the backend.


