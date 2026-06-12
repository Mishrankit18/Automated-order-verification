import pandas as pd
import pyautogui
import time
import urllib.parse
import os

# --- Configuration ---
# 1. Path to your Excel file
EXCEL_FILE_PATH = "C:\\Users\\ankit\\Desktop\\Book1.xlsx" # Adjust this path!

# 2. Delay between sending messages (CRITICAL for safety)
# 15 to 20 seconds is a bare minimum for safer bulk sending.
WAIT_TIME_SECONDS = 40 

# 3. Column names in your Excel file
PHONE_COL_NAME = 'Phone'
MESSAGE2_COL_NAME = 'item'
MESSAGE1_COL_NAME = 'name'

# --- Data Loading --
try:
    # Read the first sheet of the Excel file
    df = pd.read_excel(EXCEL_FILE_PATH,dtype={'Phone':str})                       
    contact_list = df.to_dict('records')
except FileNotFoundError:
    print(f"Error: Excel file not found at '{EXCEL_FILE_PATH}'")
    exit()
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

print(f"Found {len(contact_list)} contacts in the Excel file.")
print("\n!!! ATTENTION: You have 10 seconds to switch to your browser, open a new tab, and ensure WhatsApp Web is visible! !!!")
time.sleep(10) # Gives you time to switch windows

# --- WhatsApp Automation Loop ---
for index, contact in enumerate(contact_list):
    try:
        phone_number = str(contact[PHONE_COL_NAME]).strip()
        message1 = str(contact[MESSAGE1_COL_NAME])
        message2 = str(contact[MESSAGE2_COL_NAME])

        message = f"Hello {message1} \n\n Casemurk is here.\n\n Please confirm your order for the following product so that we can proceed with dispatch.\n\n Product Name- {message2} \n\n Kindly reply with Yes or Confirm to confirm your order✅ \n\n Note- It is not Phone❗ It is Phone case(Cover). \n\n Team Casemurk! "
        
        # 1. Format the phone number (remove non-digits except '+')
        if not phone_number.startswith('+'):
             phone_number = '+91' + phone_number

        # 2. URL-encode the message content
        encoded_message = urllib.parse.quote(message)
        
        # WhatsApp Web URL format: wa.me/<number>?text=<encoded_message>
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
        
        print(f"Processing contact {index + 1}/{len(contact_list)}: {phone_number}")

        # 3. Automate Browser Navigation
        # Press Ctrl+T (or Cmd+T on Mac) to open a new tab
        pyautogui.hotkey('ctrl', 't') 
        time.sleep(1)
        
        # Type the URL and press Enter
        pyautogui.write(whatsapp_url)
        pyautogui.press('enter')
        
        # 4. Wait for WhatsApp Web to load the chat and the send button
        # This delay is crucial for the web page to fully render.
        time.sleep(WAIT_TIME_SECONDS / 2) 
        
        # 5. Press Enter to send the message (Assumes the input box is focused)
        pyautogui.press('enter')

        # 6. Wait for the message to be sent and for the next iteration
        print(f"Message sent. Waiting for {WAIT_TIME_SECONDS} seconds before next contact...")
        time.sleep(10)

        # 7. Close the current tab (optional but recommended to keep the screen clean)
        pyautogui.hotkey('ctrl', 'w') 
        time.sleep(1)

    except Exception as e:
        print(f"An error occurred in the automation for row {index + 2} ({phone_number}): {e}")
        time.sleep(5) # Wait briefly and try the next contact
        continue

print("Process complete. All contacts exhausted from the Excel file.")
