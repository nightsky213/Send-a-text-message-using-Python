Quick start

Install dependencies (recommended):

pip install twilio requests


Set environment variables (recommended):

export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_FROM="+1234567890"   # your Twilio number in E.164 format


Send a message:

python send_sms.py --to "+9876543210" --body "Hello from Python!"


Notes:

Twilio trial accounts require the recipient number to be verified before you can message it.

Carrier fees may apply. Use environment variables or a secrets manager — avoid hardcoding credentials.

If the twilio package is not installed the script will attempt a direct HTTP POST to Twilio’s REST API using requests.
