# LLM Shipment Data Generator

This project generates synthetic logistics shipment data using Google's Gemini API and validates the generated data against complex business rules.

## Project Structure

The system is divided into three parts:

### Part 1: Shipment Generation

* **Script**: `generate_shipments.py`
* **Input**: `references/Eval_set.csv` (contains 12 specific evaluation prompts) and reference data (Origins, Commodities, Equipment).
* **Output**: Generates 12 Excel files (e.g., `EVAL-001_Output.xlsx`) in the `generated_data/` directory.
* **Logic**: Uses Gemini 2.5 Flash to convert natural language prompts into structured JSON shipment data.

### Part 2: Validators

* **Script**: `validators.py`
* **Logic**: Contains specific Python functions (`validate_eval_001` to `validate_eval_012`) to strictly verify that the generated data meets every constraint in the prompt (weight ranges, commodity types, date logic, arithmetic sequences, etc.).

### Part 3: Result Recording

* **Script**: `run_validations.py`
* **Output**: `Eval_result.xlsx`
* **Logic**: Iterates through all generated files, applies the corresponding validator, and aggregates the results (PASS/FAIL, findings, and check counts) into a summary spreadsheet.

## Setup

1. **Clone the repository**
2. **Create a virtual environment** (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure API Key**:
    Create a `.env` file in the root directory:

    ```env
    GEMINI_API_KEY=your_google_ai_studio_api_key
    ```

## Usage

### 1. Generate Data

Run the generation script to create the shipment files. This may take a minute as it calls the LLM for each scenario.

```bash
python generate_shipments.py
```

* Outputs will be saved to `generated_data/`.
* Note: The script includes retry logic for API rate limits.

### 2. Validate Data

Run the validation suite to check the quality of the generated data.

```bash
python run_validations.py
```

* This will check all files in `generated_data/`.
* Results will be saved to `Eval_result.xlsx`.

## Directory Structure

```
.
├── generate_shipments.py  # Main generation script
├── run_validations.py     # Main validation driver
├── validators.py          # Validation logic library
├── requirements.txt       # Python dependencies
├── references/            # Input CSVs (Eval_set, Origins, etc.)
├── generated_data/        # Folder for generated Excel files
└── Eval_result.xlsx       # Final validation report
```
