import os
import json
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit(1)


client = genai.Client(api_key=API_KEY)


def load_references():
    """Loads reference data to provide context to the LLM."""
    refs = {}
    ref_dir = "references"
    try:
        refs["commodities"] = pd.read_csv(
            os.path.join(ref_dir, "CommodityCodes.csv")
        ).to_string()
        refs["equipment"] = pd.read_csv(
            os.path.join(ref_dir, "EquipmentTypes.csv")
        ).to_string()
        refs["origins"] = pd.read_csv(os.path.join(ref_dir, "Origins.csv")).to_string()
        # Limiting context size if necessary, but flash generally handles large context well.
    except Exception as e:
        print(f"Warning: Could not load some reference files: {e}")
    return refs


def generate_prompt(eval_row, refs):
    """Constructs the prompt for a specific evaluation set."""

    prompt = f"""
    You are a data generation assistant for a logistics company.
    Your task is to generate synthetic shipment data based on a specific requirement (Evaluation Prompt).
    
    ### Reference Data (Use these codes and details)
    
    **Origins (Facilities):**
    {refs.get('origins', '')[:5000]}... (truncated for brevity, assume full access if needed or rely on common US cities if strict lookup not required, but PREFER using valid Location Codes from context if matches found)
    
    **Equipment Types:**
    {refs.get('equipment', '')}
    
    **Commodity Codes:**
    {refs.get('commodities', '')[:5000]}...
    
    ### Output Schema (JSON Array of Objects)
    Each object must have:
    - shipmentId (String, e.g., SHIP-0001)
    - shipFromLocationCode (String, match origin_id from Origins if possible, else create plausible)
    - city (String)
    - state (String)
    - zipCode (String)
    - countryCode (String, usually US)
    - commodityCode (String, match commodity_code)
    - equipmentTypeCode (String, match equipment_code)
    - pickupFromDateTime (ISO 8601)
    - pickupToDateTime (ISO 8601)
    - deliveryFromDateTime (ISO 8601)
    - deliveryToDateTime (ISO 8601)
    - totalWeightLbs (Integer)
    - totalVolumeCuFt (Integer)
    - totalPalletCount (Integer)
    - totalCaseCount (Integer)

    ### The Goal
    {eval_row['User Prompt']}
    
    ### Instructions
    1. Output ONLY a valid JSON array. No markdown blocks.
    2. Ensure ALL constraints in the User Prompt are met exactly (counts, sums, ranges, specific dates).
    3. Use realistic dates in 2025 or 2026 as implied by prompt or default to future.
    4. Validate logical consistency (delivery after pickup).
    """
    return prompt


def generate_dataset(eval_id, prompt):
    print(f"Generating for {eval_id}...")
    retries = 3
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    top_p=0.95,
                ),
            )
            text = response.text.strip()
            # Clean markdown
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            data = json.loads(text)
            return data
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit hit for {eval_id}. Waiting 60s...")
                time.sleep(60)
                continue
            print(f"Error generating {eval_id}: {e}")
            return []
    return []


def main():
    # Load Eval Sets
    try:
        eval_meta = pd.read_csv("references/Eval_set.csv")
    except FileNotFoundError:
        print("Error: references/Eval_set.csv not found.")
        return

    refs = load_references()

    for index, row in eval_meta.iterrows():
        eval_id = f"EVAL-{str(row['#']).zfill(3)}"
        user_prompt = row["User Prompt"]

        # Determine output filename
        output_dir = "generated_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, f"{eval_id}_Output.xlsx")

        if os.path.exists(output_file):
            print(f"Skipping {output_file} (already exists)")
            continue

        full_prompt = generate_prompt(row, refs)

        data = generate_dataset(eval_id, full_prompt)

        if data:
            df = pd.DataFrame(data)
            # Ensure columns are in correct order as per schema (optional strictly, but good practice)
            cols = [
                "shipmentId",
                "shipFromLocationCode",
                "city",
                "state",
                "zipCode",
                "countryCode",
                "commodityCode",
                "equipmentTypeCode",
                "pickupFromDateTime",
                "pickupToDateTime",
                "deliveryFromDateTime",
                "deliveryToDateTime",
                "totalWeightLbs",
                "totalVolumeCuFt",
                "totalPalletCount",
                "totalCaseCount",
            ]

            # Add missing cols with defaults if LLM missed them
            for c in cols:
                if c not in df.columns:
                    df[c] = None

            df = df[cols]
            df.to_excel(output_file, index=False)
            print(f"Saved {output_file}")

        # A bit of wait to be nice to the API
        time.sleep(5)


if __name__ == "__main__":
    main()
