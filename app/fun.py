import google.generativeai as genai
import os
import json
from dotenv import load_dotenv  # Add this import

load_dotenv()  # Load variables from .env file

# --- Configuration ---
# Option 1: Configure API key directly in the script (NOT RECOMMENDED for production)
# Replace "YOUR_API_KEY" with your actual API key.
# genai.configure(api_key="YOUR_API_KEY")

# Option 2: Load API key from an environment variable (RECOMMENDED)
# Make sure you have an environment variable named GOOGLE_API_KEY set with your API key.
try:
    api_key = os.environ.get("GEMINI_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Error: {e}")
    print("Please set the GOOGLE_API_KEY environment variable or configure the API key directly in the script.")
    exit()
    
# --- Select a Model ---
# List available models (optional, for informational purposes)
# print("Available models:")
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

# Choose a model. For text generation, 'gemini-pro' or 'gemini-1.5-flash' are common choices.
# 'gemini-1.5-flash' is often faster and more cost-effective for simpler tasks.
model_name = "gemini-2.0-flash" # Or "gemini-pro"

try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    print(f"Error creating model: {e}")
    exit()

# --- Send a Query ---
# --- Load prompt from fun.json ---
try:
    with open("fun.json", "r") as f:
        data = json.load(f)
        prompt = data.get("prompt", "")
        if not prompt:
            raise ValueError("No 'prompt' key found in fun.json.")
except Exception as e:
    print(f"Error loading prompt from fun.json: {e}")
    exit()
print(f"\nSending prompt to {model_name}: '{prompt}'\n")

try:
    # Generate content
    response = model.generate_content(prompt)

    # --- Display the Response ---
    if response.parts:
        print("Gemini's Response:")
        for part in response.parts:
            print(part.text)
    else:
        print("Gemini's Response (raw):")
        print(response.text) # Fallback if parts are not structured as expected

    # You can also inspect other parts of the response if needed:
    # print("\nFull response object:")
    # print(response)
    # print("\nPrompt feedback:")
    # print(response.prompt_feedback)
    # print("\nCandidates:")
    # print(response.candidates)

except Exception as e:
    print(f"An error occurred while sending the query or processing the response: {e}")