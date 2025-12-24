# Initial commit db

Project created, and synced between github and local folder.

# Initial commit of the project data, and the vector database
Added the problem statement files. Segregated the problem statement, policy, and the xlsx files. Converted the policy files to md using [word2md](https://word2md.com) and added them to the `policies` folder.

Used a stub of the `upsert.py` file to create the pinecone insert script, on antigravity.

#### Pinecone insert prompt
> Modify `upsert.py` to clean the code. Do things like not having api keys in the file, but in .env instead. Also, instead of the current input file, it should pick the md files in the folder `policies` . The files should be upserted into the pinecone database with id, text, and field for the type of policy (given by the file name).

# Initial front end
Just created a minimum app.

#### Prompt
> Use fastapi to create a minimal app to provide a chat interface. For now the backend should return "hello". Use a simple sqlite3 db as the backend.

# Loading the sales data
Check if the database has the sales table, if not, load the table

#### Prompt
> I have the sales data in `AI Hackathon 2.0_Sales Data.xlsx`. I need to add it to the webapp database so that it can be accessed by the database. Should I do it during init as with `database.py`? 

# Connect Gemini to chat end-point

#### Prompt
> We will begin implementing the fastapi end points. Specifically, /api/chat in @main.py. It will be a gemini powered chat agent. It will use a prompt which will be taken from a file called `chatbot.md` in the /app/prompts folder.
> The details of the chatbot implementation should be packaged into a separate py file, so that evals/tests can be run separately on the chat responses.
> For now the chat response should just use gemini, and give a chat response without extra text. Eventually, we will have to connect two MCP clients (to do some RAG and SQL extraction), so keep that in consideration while desiging the current end point.

#### Prompt to update system prompt
```text
This was the system prompt used
<prompt>
You are a Sales Intelligence Assistant for MXV Travel.
Your role is to assist sales representatives by providing information about sales policies, territory assignments, performance metrics, leave policy, and disciplinary actions.

You have access to sales data and company policies.
When answering questions:
- Be professional, concise, and helpful.
- If you don't know the answer, state that clearly.
- Do not make up information.
</prompt>

This is a conversation with a chatbot.
<conversation>
User > What can you help me with?
Chatbot > As a Sales Intelligence Assistant for MXV Travel, I can help you with information related to: * **Sales Policies:** Details on current sales policies, procedures, and guidelines. * **Territory Assignments:** Information about your assigned sales territory, including key accounts and market demographics. * **Performance Metrics:** Your individual and team sales performance data, including targets, achievements, and relevant KPIs. Essentially, I'm here to provide you with the data and information you need to be successful in your sales role at MXV Travel. Just ask!
User > What is the weight of an unladen swallow
Chatbot > I am designed to provide information about sales policies, territory assignments, and performance metrics for MXV Travel. I do not have access to information about the weight of an unladen swallow.
User > How much sales did Ramesh do during the year?
Chatbot > Please specify which year you are asking about. I need the year to provide you with Ramesh's sales figures.
User > For the current year. 2025
Chatbot > Okay. To best assist you, please specify what information you need for the current year, 2025. For example, are you asking about sales policies, territory assignments, or performance metrics? Please be as specific as possible.
</conversation>

While the chatbot avoided talking about the weight of an unladen swallow, it failed to say that it didn't know about Ramesh, and didn't yet have access to the data. Please update the prompt.
```
