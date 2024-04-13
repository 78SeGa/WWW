from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    # Extracting animal battle details from the POST request
    animal1 = request.json.get('animal1', 'Unknown')
    animal2 = request.json.get('animal2', 'Unknown')
    battle_query = f"Who would win in a battle between a {animal1} and a {animal2}?"
    response = get_openai_response(battle_query)
    return jsonify({'reply': response})

def get_openai_response(prompt):
    api_key = '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'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    instructions = "Provide an answer understandable by someone with a 1st grade reading comprehension. Focus on which animal would probably win and a short summary of why. Avoid detailed commentary on why the confrontation wouldn't happen. Keep the explanation simple and straightforward, suitable for entertainment and not bound by strict realism."

    data = {
        'model': 'gpt-4-turbo',  # Ensure this is your desired model
        'messages': [
            {'role': 'system', 'content': instructions},
            {'role': 'user', 'content': prompt}
        ]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            return response_json['choices'][0]['message']['content'].strip()
        else:
            return "Received an unexpected format or empty choices from the API."
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for detailed error logs
