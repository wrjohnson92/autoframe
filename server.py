import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os

DOWNLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), 'images')
app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""
    resp = MessagingResponse()
    if request.values['NumMedia'] != '0':
        # Use the message SID as a filename.
        filename = request.values['MessageSid'] + '.png'
        print(filename)
        with open(os.path.join(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
            image_url = request.values['MediaUrl0']
            f.write(requests.get(image_url).content)

        resp.message("Your image has been added to the photoframe!")
    else:
        resp.message("Was not able to find a photo in your message.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)