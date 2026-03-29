while True:
    import json

    # Load schemes
    with open("schemes.json") as f:
        schemes = json.load(f)

    # Language selection
    print("Select Language / भाषा चुनें")
    print("1. English")
    print("2. Hindi")
    lang_choice = input("Enter number choice for language: ")

    def t(en, hi):
        return hi if lang_choice == "2" else en

    print("\n" + t("🤖 Welcome to Sahayak AI", "🤖 सहायक AI में आपका स्वागत है"))
    print(t("Answer a few questions...\n", "कुछ सवालों के जवाब दें...\n"))

    # Inputs
    name = input(t("Enter your name: ", "अपना नाम दर्ज करें: "))
    age = int(input(t("Enter your age: ", "अपनी उम्र दर्ज करें: ")))
    income = int(input(t("Enter your annual income: ", "अपनी वार्षिक आय दर्ज करें: ")))

    occupation_input = input(t(
        "Enter your occupation (comma separated): ",
        "अपना पेशा दर्ज करें (comma से अलग करें): "
    )).lower()

    education = input(t("Enter your education: ", "अपनी शिक्षा दर्ज करें: ")).lower()
    location = input(t("Enter your location: ", "अपना स्थान दर्ज करें: ")).lower()

    user_roles = [x.strip().lower() for x in occupation_input.split(",")]

    
    result = ""
    if "student" in user_roles:
        result = input(t("Enter your result (pass/fail): ",
                         "अपना परिणाम दर्ज करें (pass/fail): ")).lower()

    print("\n" + t("🤖 Analyzing your profile...",
                   "🤖 आपकी जानकारी का विश्लेषण किया जा रहा है..."))

    matched = []

for scheme in schemes:
    score = 0


    if not (any(role in scheme["occupation"] for role in user_roles) or "any" in scheme["occupation"]):
        continue


    if "student" in scheme["occupation"]:
        if "student" in user_roles and result != "pass":
            continue


    if scheme["income_min"] <= income <= scheme["income_max"]:
        score += 1


    if education in scheme["education"] or "any" in scheme["education"]:
        score += 1


    if score >= 1:
        explanation = explain_scheme(data, scheme)

        matched.append({
            "name": scheme["name"],
            "benefit": scheme["benefit"],
            "link": scheme["link"],
            "explanation": explanation,
            "score": score
        })

        

    print("\n" + t(f"Hello {name}, here are your best schemes:",
                   f"{name}, आपके लिए योजनाएँ:"))

    
    if matched:
        for s, score in matched:
            print("\n👉", s["name"])
            print(t("Benefit: ", "लाभ: "), s["benefit"])
            print(t("Match Score: ", "मैच स्कोर: "), f"{score}/3")
            print(t("Apply here: ", "यहाँ आवेदन करें: "), s["link"])

    else:
        print("\n" + t("❌ No exact schemes found for your profile",
                       "❌ आपके प्रोफाइल के अनुसार कोई योजना नहीं मिली"))

        print("\n" + t("Possible reasons:",
                       "संभावित कारण:"))
        print(t("- Income may be higher than eligibility",
                "- आपकी आय सीमा से अधिक हो सकती है"))
        print(t("- Occupation mismatch",
                "- आपका पेशा योजना से मेल नहीं खाता"))
        print(t("- Education criteria not met",
                "- शिक्षा पात्रता पूरी नहीं होती"))

        print("\n" + t("💡 Suggestions:",
                       "💡 सुझाव:"))
        print(t("- Check state-level schemes",
                "- राज्य स्तर की योजनाएँ देखें"))
        print(t("- Try again with correct details",
                "- सही जानकारी के साथ फिर से प्रयास करें"))

        print("\n" + t("🔎 Showing closest matches:",
                       "🔎 सबसे नज़दीकी योजनाएँ:"))

        # Show only top 2 closest
        for s in schemes[:2]:
            print("\n👉", s["name"])
            print(t("Benefit: ", "लाभ: "), s["benefit"])

    print("\n" + t("✅ Thank you!", "✅ धन्यवाद!"))

    # Restart
    again = input(t("\nDo you want to try again? (yes/no): ",
                    "\nक्या आप फिर से कोशिश करना चाहते हैं? (yes/no): ")).lower()

    if again != "yes":
        print(t("👋 Goodbye!", "👋 अलविदा!"))
        break