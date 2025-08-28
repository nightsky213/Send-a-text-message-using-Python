#!/usr/bin/env python3
"""
send_sms.py
Send an SMS using Twilio (recommended) with a fallback to direct HTTP requests if the `twilio` package isn't installed.

Usage examples:
  # Using environment variables (recommended)
  export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  export TWILIO_AUTH_TOKEN="your_auth_token"
  export TWILIO_FROM="+1234567890"   # Twilio phone number
  python send_sms.py --to "+19876543210" --body "Hello from Python!"

  # Or pass credentials on the CLI (less secure)
  python send_sms.py --to "+19876543210" --body "Hi" --account-sid "AC..." --auth-token "..." --from "+1234567890"

Notes:
 - Twilio trial accounts require the recipient number to be verified.
 - Carrier fees may apply.
 - Keep credentials secret: prefer environment variables.
"""

import argparse
import os
import sys

def send_with_twilio(account_sid, auth_token, from_number, to_number, body):
    try:
        from twilio.rest import Client
    except Exception as e:
        raise ImportError("twilio package not installed") from e
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=body, from_=from_number, to=to_number)
    return {"sid": message.sid, "status": message.status}

def send_with_requests(account_sid, auth_token, from_number, to_number, body):
    # Minimal direct HTTP fallback to Twilio REST API v2010-04-01
    import requests
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    payload = {
        "From": from_number,
        "To": to_number,
        "Body": body,
    }
    resp = requests.post(url, data=payload, auth=(account_sid, auth_token), timeout=30)
    resp.raise_for_status()
    return resp.json()

def parse_args():
    p = argparse.ArgumentParser(description="Send an SMS via Twilio (recommended).")
    p.add_argument("--to", required=True, help="Recipient phone number in E.164 format, e.g. +14155552671")
    p.add_argument("--body", required=True, help="Message body (text)")
    p.add_argument("--account-sid", help="Twilio Account SID (defaults to TWILIO_ACCOUNT_SID env)")
    p.add_argument("--auth-token", help="Twilio Auth Token (defaults to TWILIO_AUTH_TOKEN env)")
    p.add_argument("--from", dest="from_number", help="From phone (Twilio number) (defaults to TWILIO_FROM env)")
    return p.parse_args()

def main():
    args = parse_args()
    account_sid = args.account_sid or os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = args.auth_token or os.getenv("TWILIO_AUTH_TOKEN")
    from_number = args.from_number or os.getenv("TWILIO_FROM")

    if not (account_sid and auth_token and from_number):
        sys.exit("Missing credentials. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM env vars or pass them via CLI.")

    to_number = args.to
    body = args.body

    # Try twilio package first (cleanest), otherwise fallback to requests
    try:
        result = send_with_twilio(account_sid, auth_token, from_number, to_number, body)
        print("Sent via twilio package. Result:", result)
    except ImportError:
        print("twilio package not installed; attempting HTTP fallback using requests.")
        try:
            result = send_with_requests(account_sid, auth_token, from_number, to_number, body)
            print("Sent via HTTP API. Response:")
            print(result)
        except Exception as e:
            print("Failed to send message via HTTP API:", str(e))
            raise
    except Exception as e:
        print("Failed to send via twilio package:", str(e))
        raise

if __name__ == "__main__":
    main()
