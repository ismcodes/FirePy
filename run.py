from flask import Flask, request, redirect
import twilio.twiml, random
app = Flask(__name__)
def generate_sequence(): 
    adjectives=["grand", "baby", "musical", "quiet", "quick", "good"]
    colors=["red","blue","green","purple","orange","cyan","pink", "amber", "gray"]
    nouns=["paper", "desk", "plant", "cereal", "dog", "car", "window", "diamond", "street", "water", "icon"]

@app.route("/<string:sequence>", methods=['GET', 'POST'])
def respond_to_fire():
    """Respond to incoming calls with a simple text message."""
 
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)