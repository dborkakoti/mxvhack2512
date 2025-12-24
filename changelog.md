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

# Using MCP for the sales data and policies

## Step A: create initial structure

#### Prompt

> Now we want to augment the chatbot with two MCP clients. 1. Sales data client: which uses the existing connection, and queries the sales table for information on the sales. 2. The policy client: which connects with the pinecone vector database `mxvtravel` to reply to questions around policy. 
> For now create a outline to add these functionalities.

# Evaluation

## First evaluation
Ask for an evaluator.

#### Prompt
```md
Eval_questions.xlsx
 has question-answer pairs for evaluationg the chatbot performance. Create a test python file to test 
chatbot.py
 on those questions. Create a new folder called test_results. Run the tests and create a tracking file with the test question, expected answer, and actual answer for each test run (with the datetime of the test run). Also include a summary of accuracy, precision and recall for the test run in the results file.
 ```

## Finetuning the prompt
First run had precision/accuracy of 0.53. So, checking for suggestion on improving the system prompt.

#### Prompt
```md
These are some sample outputs where the answer returned by the chatbot didn't match the expected answer.

<outputs>
<output>
Question: "I took 6 consecutive working days of approved Earned Leave in March, which was quarter-end. My manager says incentives will be reduced. Is this correct?"
Sample answer: "Partially correct. Approved leave itself does not automatically reduce incentives, but extended leave during a critical period can reduce incentive eligibility if policy-defined productivity thresholds or availability clauses are breached. The reduction must be policy-backed, not discretionary."
Actual answer: "I do not have enough information to determine whether your incentives will be reduced due to taking 6 days of approved leave in March. To determine whether this is correct, you should consult the Sales Incentive Policy for details on how leave impacts incentive eligibility. I can search the policy document for you, but I need a more specific query. For example, does the policy mention anything about leave taken during quarter-end?  "
Evaluation: "The actual answer states it doesn't have enough information, and suggests consulting the policy document. It doesn't provide any factual information to compare with the expected answer. Therefore, there are no true positives, false positives, or false negatives. Precision and recall are 0. Accuracy is 0 as the answer does not contain any of the expected information."
</output><output>
Question: I was on approved leave during a launch week and another salesperson closed deals in my territory. Who gets credit?
Sample answer: "The salesperson who executed and closed the deal gets credit unless there is prior documented deal ownership. Approved leave does not preserve incentive entitlement for work not performed."
Actual answer: "The policy documents state that during approved leave, temporary territory coverage arrangements may be made. Permanent territory reassignment may occur in extreme cases of prolonged absence combined with business risk. Territory reassignment does not automatically reset performance history unless explicitly stated. I do not have information on how sales credits are specifically assigned during temporary territory coverage.
Evaluation: The actual answer does not contain any of the facts from the expected answer. Therefore, there are no true positives. The actual answer discusses territory coverage and reassignment during leave, but it does not address how sales credits are specifically assigned. The expected answer directly addresses sales credit assignment during leave, stating the salesperson who closes the deal gets credit unless there is prior deal ownership and that approved leave does not preserve incentive entitlement for work not performed. Due to the absence of overlap, precision and recall are 0. The answer is not factually correct with respect to the expected answer, thus accuracy is 0.
</output><output>
Question: A deal was booked before territory reassignment but invoiced after. Who gets credit?
Sample answer: "Credit follows the booking date and territory ownership at the time of deal confirmation, not invoicing, unless policy explicitly defines revenue recognition otherwise."
Actual answer: "The policy documents state that territory reassignment impacts incentives, and incentives may be prorated based on days of ownership. For more specific details, please query the policy documents further.
Evaluation: Expected Facts: Credit is determined by booking date and territory at the time of deal confirmation. Actual summary: Territory reassignment impacts incentives. Incentives may be prorated based on ownership days.
</output><output>
Question: I received a Level 2 warning but met targets. Can incentives be withheld?
Sample answer: "Yes. Active disciplinary actions can override performance outcomes. Incentives are contingent on both results and compliance."
Actual answer: "I am sorry, I am unable to process your request. There seems to be an issue with the query."
Evaluation: The actual answer indicates an inability to process the request, providing no factual information.
</output><output>
Question: Incentives were withheld during a disciplinary review that later closed clean. Can they be reinstated?
Sample answer: Possibly. Reinstatement is allowed if the policy explicitly permits retrospective payout after clearance. It is not automatic and requires formal approval.
Actual answer: The disciplinary policy takes precedence over the sales incentive policy. I do not have specific information about the reinstatement of incentives after a disciplinary review closes clean. I recommend reviewing the "Disciplinary Actions" policy document for details, or consulting with the HR department.
Evaluation: The actual answer does not provide any of the expected information, such as the possibility of reinstatement and the need for policy review and formal approval.
</output><output>
Question: I took 7 days of approved Earned Leave in a month and met targets. Can incentives be reduced?
Sample answer: Yes. Extended leave can proportionally reduce incentive eligibility if minimum active working days or coverage requirements are defined in policy.
Actual answer: I have retrieved the Sales Incentive Policy. However, based on the policy document, I cannot determine whether incentives can be reduced for taking 7 days of approved Earned Leave in a month, even if targets are met. To determine if your incentives can be reduced, you need to refer to the detailed terms outlined in the Sales Incentive Policy document.
Evaluation: The actual answer fails to provide a definitive answer to the question and states that the information could not be determined from the document, even though the expected answer indicates a reduction may be possible based on policy conditions.
</output><output>
Question: I worked remotely while on approved leave. Does this count as attendance?,
Sample answer: No. Approved leave remains leave even if work was performed informally. Attendance and incentive eligibility depend on formal status, not ad hoc effort.
Actual answer: Remote work is not a substitute for field attendance unless explicitly approved. Lack of field presence during assigned territory days may be reviewed even if leave is approved. Reassignment during leave may affect incentive and rating calculations and incentives may be proportionately reduced if leave coincides with critical business windows.
Evaluation: The actual answer does not address the core question of whether working remotely while on leave counts as attendance. The actual answer discusses remote work as a substitute for field attendance and the impact of reassignment during leave on incentives, deviating from the expected answer's focus on leave status and its implications for attendance and eligibility.
</output>
</outputs>

This is the prompt being used:
<prompt>
You are a Sales Intelligence Assistant for MXV Travel.
Your role is to assist sales representatives by providing information about sales policies, territory assignments, performance metrics, leave policy, and disciplinary actions.

You have access to sales data and company policies.

Strict Rules for Answering:
- **Grounding:** Answer ONLY using the information explicitly provided to you in the context or tools.
- **Tools:** You have access to tools to query sales data and company policies. Use them whenever needed.
- **Database Schema (for sales data):**
  - Table: `sales`
  - Columns:
    - `salesperson_id` (Text), `salesperson_name` (Text), `territory` (Text), `category` (Text)
    - `jan`, `feb`, ..., `dec` (Real) - Monthly sales
    - `total_revenue_inr_lakhs` (Real), `target_revenue_inr_lakhs` (Integer)
    - `deals_closed` (Integer), `active_days` (Integer), `approved_leave_days` (Integer)
    - `incentive_eligible` (Text: 'Yes'/'No')
- **Missing Data:** If a user asks about a specific person (e.g., Ramesh), year, or metric that is not present in your current data access, you must explicitly state: "I do not have access to data regarding [Name/Topic] at this time."
- **No Assumptions:** Do not ask clarifying questions (like "which year?") if you do not have the underlying data to answer the question regardless of the year.
- Be professional, concise, and helpful.
</prompt>

Go through the cases of errors, and summarise the issues with them. Improve the prompt to avoid such errors.
```

# Small fixes

```md
In the core app. I want a couple of changes:
* Rate limit the app to max 2 questions per minute
* Ensure that a visible element is shown after the question is submitted and before the answer is avvailalbe from the backend. Grey out the submit button on the chat during this period.
```

# Deploy

#### Vercel

```md
I want to upload the app to a server. I was thinking Vercel, but open to suggestion. How do I get it to work? Note that I have the envirnoment varaibles for GOOGLE api and pinecone api. I want to upload those too, but with an eye out for security. Should I rate limit the app
```
#### Google Cloud Run

```md
I want to upload the app to a server. I was thinking Google Cloud Run, but open to suggestion. How do I get it to work? Note that I have the envirnoment varaibles for GOOGLE api and pinecone api. I want to upload those too, but with an eye out for security. Should I rate limit the app
```

## Note
Neither worked very well for the sales dataset, since both are read only deployments, and thus sqlite3 bombs.

## Trying to deploy to Supabase

```md
Change the database from sqlite3 local to supabase
```