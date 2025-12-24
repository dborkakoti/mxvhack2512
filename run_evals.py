import pandas as pd
import os
import datetime
import json
import google.generativeai as genai
from app.chatbot import get_chatbot
from dotenv import load_dotenv

load_dotenv()

# Setup Evaluator
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
evaluator_model = genai.GenerativeModel('gemini-2.0-flash')

def evaluate_response(question, expected, actual):
    prompt = f"""
    You are an expert evaluator for a RAG-based chatbot.
    Compare the ACTUAL ANSWER with the EXPECTED ANSWER for the given QUESTION.

    Calculate the metrics based on Key Fact Analysis:

    1. **Analyze Facts**:
       - **Expected Facts**: List the distinct atomic facts in the EXPECTED answer.
       - **Actual Facts**: List the distinct atomic facts in the ACTUAL answer.

    2. **Classify Matches**:
       - **True Positives (TP)**: Actual facts that verify Expected facts.
       - **False Positives (FP)**: Actual facts that are NOT in Expected (hallucinations or irrelevant extra info).
       - **False Negatives (FN)**: Expected facts missing from Actual.

    3. **Calculate Metrics**:
       - **Precision**: TP / (TP + FP)  -> (How much of the generated answer is relevant/correct?)
       - **Recall**: TP / (TP + FN)     -> (How much of the expected answer was retrieved?)
       - **Accuracy**: 1 if the answer is completely factually correct w.r.t Expected (no critical errors), else 0.

    Return ONLY a JSON object with these keys: "accuracy" (float), "precision" (float), "recall" (float), "reasoning" (string).
    
    Question: {question}
    Expected Answer: {expected}
    Actual Answer: {actual}
    """
    
    try:
        response = evaluator_model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        print(f"Eval Error: {e}")
        return {"accuracy": 0, "precision": 0, "recall": 0, "reasoning": str(e)}

def run_evals():
    input_file = "app/dataset/Eval_questions.xlsx"
    chatbot = get_chatbot()
    if not chatbot:
        print("Failed to initialize chatbot.")
        return

    print("Loading questions...")
    df = pd.read_excel(input_file)
    
    results = []
    
    # Process each question
    for index, row in df.iterrows():
        question = row['Question (Salesperson-facing)']
        expected = row['Correct answer']
        
        print(f"Processing Q{index+1}: {question[:50]}...")
        
        # Get Chatbot Response
        try:
            actual = chatbot.generate_response(question)
        except Exception as e:
            actual = f"Error: {e}"
        
        # Evaluate
        metrics = evaluate_response(question, expected, actual)
        
        result_row = {
            "timestamp": datetime.datetime.now().isoformat(),
            "question": question,
            "expected_answer": expected,
            "actual_answer": actual,
            "accuracy": metrics.get("accuracy", 0),
            "precision": metrics.get("precision", 0),
            "recall": metrics.get("recall", 0),
            "reasoning": metrics.get("reasoning", "")
        }
        results.append(result_row)

    # Create DataFrame and Save
    results_df = pd.DataFrame(results)
    
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"test_results/eval_run_{timestamp_str}.csv"
    results_df.to_csv(output_file, index=False)
    
    print(f"\nEvaluation Complete. Results saved to {output_file}")
    print("\nSummary Metrics:")
    print(f"Average Accuracy:  {results_df['accuracy'].mean():.2f}")
    print(f"Average Precision: {results_df['precision'].mean():.2f}")
    print(f"Average Recall:    {results_df['recall'].mean():.2f}")

if __name__ == "__main__":
    run_evals()
