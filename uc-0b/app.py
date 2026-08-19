"""
UC-0B app.py — Starter file.
Build this using the RICE + agents.md + skills.md + CRAFT workflow.
See README.md for run command and expected behaviour.
"""
import argparse
import os

def retrieve_policy(file_path: str) -> str:
    """
    Skill: retrieve_policy
    Loads the .txt policy file and returns its content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Policy file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_file(file_path: str) -> str:
    """Helper to load markdown files for the prompt context."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def summarize_policy(policy_text: str, agents_content: str, skills_content: str) -> str:
    """
    Skill: summarize_policy
    Uses an LLM to summarize the policy strictly according to agents.md rules.
    """
    # Attempt to import google.generativeai. If you use OpenAI or another provider,
    # you can swap out the implementation here.
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError("Please install google-generativeai to run this script (pip install google-generativeai)")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it before running.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Construct the RICE prompt based on agents.md and skills.md
    prompt = f"""
You are executing the `summarize_policy` skill. Follow the strict guidelines below:

--- AGENTS.MD CONFIGURATION ---
{agents_content}

--- SKILLS.MD CONFIGURATION ---
{skills_content}

--- SOURCE DOCUMENT TO SUMMARIZE ---
{policy_text}
"""
    
    response = model.generate_content(prompt)
    return response.text

def main():
    parser = argparse.ArgumentParser(description="UC-0B Policy Summarizer")
    parser.add_argument("--input", required=True, help="Path to policy_hr_leave.txt")
    parser.add_argument("--output", required=True, help="Path to write summary output")
    args = parser.parse_args()
    
    try:
        policy_text = retrieve_policy(args.input)
        
        # Load agents.md and skills.md from the same directory as app.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        agents_md = load_file(os.path.join(base_dir, 'agents.md'))
        skills_md = load_file(os.path.join(base_dir, 'skills.md'))
        
        print("Generating summary based on agents.md and skills.md rules...")
        summary = summarize_policy(policy_text, agents_md, skills_md)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        print(f"Summary successfully written to {args.output}")
    except Exception as e:
        print(f"Failed to generate summary: {e}")

if __name__ == "__main__":
    main()
