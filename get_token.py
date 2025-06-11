from kiteconnect import KiteConnect

api_key = "kjz4xgysne8a61xl"

kite = KiteConnect(api_key=api_key)

print("Login URL:", kite.login_url())
