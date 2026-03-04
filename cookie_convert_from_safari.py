# Cookie copied from Safari
# session	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9	.goulielmos.org	/	04/03/2027, 09:49:31	258 B	✓	✓	Lax

# Same cookie in a format usable by curl -b
# session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9;	Domain=.goulielmos.org;	Path=/;	Max-Age=31536000;	Secure;	HttpOnly;	SameSite=lax;

import sys
import re
from datetime import datetime

def convert_cookie(raw_input):
    # Safari copies columns as tab-separated values
    # Format: Name | Value | Domain | Path | Expiry | Size | Secure | HttpOnly | SameSite
    parts = raw_input.strip().split('\t')
    
    if len(parts) < 5:
        # Fallback for space-separated if tabs are converted to spaces
        parts = re.split(r'\s{2,}', raw_input.strip())

    if len(parts) < 5:
        return "Error: Could not parse cookie columns. Ensure you copied the full row from Safari."

    name = parts[0]
    value = parts[1]
    domain = parts[2]
    path = parts[3]
    expires_str = parts[4]
    
    # Flags (Safari uses the checkmark '✓' for True)
    # The positions can vary slightly, so we look for the symbol in the flag columns
    is_secure = "✓" in parts[6] if len(parts) > 6 else False
    is_httponly = "✓" in parts[7] if len(parts) > 7 else False
    samesite = parts[8] if len(parts) > 8 else "Lax"

    # Calculate Max-Age based on the provided expiry date
    # Input format: 04/03/2027, 09:49:31
    try:
        expiry_dt = datetime.strptime(expires_str, "%d/%m/%Y, %H:%M:%S")
        # Current time is March 2026
        max_age = int((expiry_dt - datetime.now()).total_seconds())
    except Exception:
        max_age = 31536000 # Default 1 year

    # Build the Curl/Standard format
    cookie_str = f"{name}={value}; Domain={domain}; Path={path}; Max-Age={max_age};"
    
    if is_secure:
        cookie_str += " Secure;"
    if is_httponly:
        cookie_str += " HttpOnly;"
    
    cookie_str += f" SameSite={samesite.lower()};"

    return cookie_str

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Accept input as a quoted argument
        user_input = sys.argv[1]
    else:
        print("Paste the Safari cookie row and press Enter (Ctrl+D to finish):")
        user_input = sys.stdin.read()

    if user_input.strip():
        print("\n--- Formatted for Curl ---")
        print(convert_cookie(user_input))
