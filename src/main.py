# src/main.py

import os
import json
import time
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# 1. Initial Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model (using flash or flash-lite depending on your project availability)
model = genai.GenerativeModel('gemini-2.5-flash-lite') 

# Directory configuration (Pathlib is cross-platform and robust)
INPUT_DIR = Path("../data/input")
OUTPUT_DIR = Path("../data/output")

# Create directories automatically if they do not exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_buyers_with_ai(chat_batch_text):
    """
    Sends a batch of raw chat logs to the Gemini API and returns a list 
    of JSON dictionaries containing confirmed buyer details.
    """
    prompt = f"""
    You are a data extraction expert. I will provide you with a series of WhatsApp chat logs.
    
    TASK:
    1. Identify ONLY confirmed buyers. 
    2. A buyer is confirmed if they provided a delivery address AND/OR phone number, or if the order was explicitly confirmed by either party.
    3. Ignore people who only asked for prices, catalogs, or stopped responding before confirming.
    
    DATA TO EXTRACT (if buyer is confirmed):
    - Name
    - Phone Number (in international format if possible)
    - Approximate Date of Purchase
    
    OUTPUT FORMAT:
    Return a valid JSON list of objects. Each object must have these keys: "name", "phone", "date".
    If no buyers are found, return an empty list [].
    
    IMPORTANT: Do not return any text other than the JSON.
    
    INPUT DATA:
    {chat_batch_text}
    """

    try:
        response = model.generate_content(prompt)
        # Clean the markdown formatting that the AI sometimes appends
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"⚠️ Error processing batch: {e}")
        return []

def main():
    print("🚀 Starting the extraction pipeline...")
    
    all_chats = []
    
    # 2. Read ALL .txt files from the data/input/ directory
    txt_files = list(INPUT_DIR.glob("*.txt"))
    
    if not txt_files:
        print(f"❌ No .txt files found in: {INPUT_DIR.resolve()}")
        print("Please ensure the WhatsApp chat logs are placed there.")
        return
        
    print(f"📂 Found {len(txt_files)} text file(s). Reading content...")
    
    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Separate chats using the header as a delimiter
            chats_in_file = [chat.strip() for chat in content.split('--- CHAT') if chat.strip()]
            all_chats.extend(chats_in_file)
            
    print(f"💬 Total individual conversations found: {len(all_chats)}")
    
    # 3. Batch Processing
    BATCH_SIZE = 20  # Grouping by 20 to avoid exceeding the context window
    extracted_buyers_list = []
    
    print(f"🤖 Processing with Gemini in batches of {BATCH_SIZE} chats...")
    
    for i in range(0, len(all_chats), BATCH_SIZE):
        batch = all_chats[i:i + BATCH_SIZE]
        
        # Reconstruct the text batch for the AI prompt
        chat_batch_text = "\n\n--- CHAT ".join(batch)
        chat_batch_text = "--- CHAT " + chat_batch_text 
        
        current_batch = (i // BATCH_SIZE) + 1
        total_batches = ((len(all_chats) - 1) // BATCH_SIZE) + 1
        print(f"   ⏳ Processing batch {current_batch} of {total_batches}...")
        
        results = extract_buyers_with_ai(chat_batch_text)
        extracted_buyers_list.extend(results)
        
        # 2-second pause to respect API Rate Limits and prevent HTTP 429 errors
        time.sleep(2)
        
    # 4. Cleaning and Exporting with Pandas
    if extracted_buyers_list:
        df = pd.DataFrame(extracted_buyers_list)
        
        # Basic cleaning: remove rows where the phone is empty due to AI parsing errors
        df.replace("", pd.NA, inplace=True)
        df.dropna(subset=['phone'], inplace=True)
        
        # Strict deduplication based on phone number
        initial_count = len(df)
        df.drop_duplicates(subset=['phone'], keep='first', inplace=True)
        final_count = len(df)
        
        print("\n✅ PROCESSING COMPLETE")
        print(f"👤 Unique buyers extracted: {final_count}")
        if initial_count > final_count:
            print(f"🗑️ Removed {initial_count - final_count} duplicate records.")

        # Save the final dataframe to the data/output/ directory
        output_file = OUTPUT_DIR / "confirmed_buyers.csv"
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"💾 File successfully saved to: {output_file.resolve()}")
        
        print("\n--- PREVIEW ---")
        print(df.head())
    else:
        print("\n❌ No confirmed buyers were detected in the provided files.")

if __name__ == "__main__":
    main()


