import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
    print("Please add your API key to the .env file.")
    exit(1)

genai.configure(api_key=API_KEY)

# Define the model
model = genai.GenerativeModel("gemini-2.5-flash")

# Define the prompt
prompt = """
Generate 20 realistic customer orders in JSON format.
The output should be a JSON array of objects.
Do not include any markdown formatting like ```json or ```. Just the raw JSON.

Each order object must have the following structure:
{
  "order_id": "ORD-2025-001",
  "pickup_location": {
    "city": "Dallas",
    "state": "TX",
    "zipcode": "75201"
  },
  "delivery_location": {
    "city": "Houston",
    "state": "TX",
    "zipcode": "77002"
  },
  "weight_lbs": 3500,
  "equipment_required": "Dry Van",
  "commodity": "General Freight",
  "ready_date": "2025-10-15",
  "delivery_deadline": "2025-10-17"
}

Constraints:
1. Generate exactly 20 orders.
2. Use realistic US cities for pickup and delivery locations (ensure city, state, and zipcode match).
3. Weight range: 1,000 - 20,000 lbs.
4. Equipment must be one of: ["Dry Van", "Refrigerated", "Flatbed"].
5. Commodity must be one of: ["General Freight", "Food", "Electronics"].
6. Dates must be in October 2025.
7. delivery_deadline must be after ready_date.
8. order_id should follow the pattern ORD-2025-XXX with unique numbers.
"""

print("Generating data...")

try:
    response = model.generate_content(prompt)

    # Simple cleaning if the model output contains markdown code blocks
    text_content = response.text.strip()
    if text_content.startswith("```json"):
        text_content = text_content[7:]
    if text_content.startswith("```"):
        text_content = text_content[3:]
    if text_content.endswith("```"):
        text_content = text_content[:-3]

    text_content = text_content.strip()

    orders = json.loads(text_content)

    if not isinstance(orders, list):
        raise ValueError("Output is not a JSON list")

    output_file = "orders.json"
    with open(output_file, "w") as f:
        json.dump(orders, f, indent=2)

    print(f"Successfully generated {len(orders)} orders in '{output_file}'.")

except Exception as e:
    print(f"An error occurred: {e}")
    # Print the raw text for debugging if JSON parsing failed
    if "text_content" in locals():
        print("Raw response content:")
        print(text_content[:500] + "..." if len(text_content) > 500 else text_content)
