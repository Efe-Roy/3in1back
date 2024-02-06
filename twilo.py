from twilio.rest import Client

account_sid = 'ACa5df16262abbbd8f40e59febeb07ee07'
auth_token = '8355eb35ae9fc4c34d61c3a51ffb7441'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+2348134964142'
)

print(message.sid)