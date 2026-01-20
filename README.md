# Synthetic Customer Order Generator

This project uses the Google Gemini API to generate synthetic customer order data for testing purposes.

## Deliverables

- `generate_orders.py`: Python script to generate the data.
- `orders.json`: The generated data (created after running the script).

## Requirements

- Python 3
- A valid Gemini API Key

## Setup & Usage

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**

   Add your Gemini API key to the `.env` file:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Run the script:**

   ```bash
   python3 generate_orders.py
   ```

4. **Output:**
   The script will generate `orders.json` containing 20 realistic orders.
