from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import traceback

app = Flask(__name__)

# Configure Gemini API key
GEMINI_API_KEY = 'AIzaSyAYnww2Q2VF7dmBPjP393XUQDJpVU_V7aQ'

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini 2.5 Pro Preview model and start chat session
try:
    chat_model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    chat_session = chat_model.start_chat(history=[])

    response = chat_session.send_message("Hello!")
    print(response.text)

except Exception as e:
    print("❌ ERROR loading Gemini model:", e)
    traceback.print_exc()
    exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'reply': "Please send a valid message."})

    try:
        print(f"📩 User message: {user_message}")

        # Send message using chat session
        response = chat_session.send_message(user_message)

        print(f"📜 Raw response object: {response}")

        # Extract reply text
        if hasattr(response, 'text') and response.text:
            reply = response.text
        else:
            reply = "Sorry, I didn't understand that."

        print(f"🤖 Bot reply: {reply}")

    except Exception as e:
        print("❌ ERROR during Gemini API call:", e)
        traceback.print_exc()
        reply = "Sorry, there was an internal error. Please try again later."

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
