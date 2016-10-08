from google_translate_api import GoogleTranslateAPI
from twilio_sms_api import TwilioSMSAPI

# Main
googleApi = GoogleTranslateAPI("------------------------------")
translated_message = googleApi.translate("Text to translate here", "th")
print(translated_message)

twilioApi = TwilioSMSAPI("-----------------------", "-----------------------")
twilioApi.send('+-----------', '+----------', translated_message)