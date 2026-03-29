from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from openai import OpenAI
import concurrent.futures # For parallel processing if needed

client = OpenAI(api_key="sk-proj-abc123yourrealactualkey")

app = Flask(__name__)
CORS(app)

# Load schemes once at startup
try:
    with open("schemes.json", encoding="utf-8") as f:
        schemes = json.load(f)
except Exception as e:
    print(f"Error loading schemes.json: {e}")
    schemes = []

@app.route("/get_schemes", methods=["POST"])
def get_schemes():
    try:
        data = request.json
        lang = data.get("lang", "en")
        income = int(data.get("income", 0))
        user_age = int(data.get("age", 0)) # Age added
        user_gender = data.get("gender", "any").lower()
        user_caste = data.get("caste", "any").lower()
        user_roles = [x.strip().lower() for x in data.get("occupation", "").split(",")]

        matched = []
        for s in schemes:
            # 1. Faster filtering
            age_match = s.get("age_min", 0) <= user_age <= s.get("age_max", 100)
            inc_match = s.get("income_min", 0) <= income <= s.get("income_max", 9999999)
            occ_match = any(role in s["occupation"] for role in user_roles) or "any" in s["occupation"]
            gen_match = user_gender in s.get("gender", []) or "any" in s.get("gender", [])
            caste_match = user_caste in s.get("caste", []) or "any" in s.get("caste", [])

            if age_match and inc_match and occ_match and gen_match and caste_match:
                matched.append({
                    "name": s.get(f"name_{lang}", s["name_en"]),
                    "benefit": s.get(f"benefit_{lang}", s["benefit_en"]),
                    "documents": s.get(f"docs_{lang}", s.get("documents", ["Aadhar Card"])),
                    "link": s.get("link", "#"),
                    # 🔥 REMOVED AI CALL FROM LOOP: 
                    # Use a static explanation or a generic "You qualify!" 
                    "explanation": s.get(f"explanation_{lang}", "You match the criteria for this scheme.")
                })
        
        # Returns instantly because no API calls are made here
        return jsonify(matched)
    except Exception as e:
        print(f"Scheme Route Error: {e}")
        return jsonify([])

@app.route("/chat", methods=["POST"])
def chat():
    # Keep this as is - this is for the one-on-one conversation
    try:
        data = request.json
        query = data.get("query")
        if not query:
            return jsonify({"reply": "No query received"}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Sahayak AI. Answer questions about Indian government schemes briefly and clearly."},
                {"role": "user", "content": query}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"reply": "I'm having trouble connecting to my brain. Please try again."}), 500
    
if __name__ == "__main__":
    app.run(port=5000, debug=False) # Debug false for better performance