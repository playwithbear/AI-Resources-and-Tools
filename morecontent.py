import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found! Set the OPENAI_API_KEY environment variable.")

# Load JSON data
with open("data2.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to check for missing AI tools in a category
def find_missing_tools(category_title, existing_tools):
    prompt = (
        f"The following AI tools are currently listed under the category '{category_title}':\n"
        f"{', '.join(existing_tools)}\n\n"
        "Are there any important AI tools missing from this category? If so, return them as a valid JSON array of objects, with each object containing:\n"
        "- 'title' (string)\n"
        "- 'content' (string, a short description of the tool)\n"
        "- 'link' (string, the official website)\n"
        "- 'pricing' (string, e.g., 'free', 'freemium', 'paid')\n\n"
        "Ensure the response is **ONLY** valid JSON. Do not include any additional text, explanations, or formatting."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an AI expert completing a JSON directory."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )

    raw_response = response.choices[0].message.content.strip()

    # Try parsing JSON response
    try:
        missing_tools = json.loads(raw_response)
        if isinstance(missing_tools, list):  # Ensure it's an array
            return missing_tools
        else:
            raise ValueError("Invalid JSON format (not a list)")
    except json.JSONDecodeError:
        print(f"⚠️ Failed to parse JSON response for category: {category_title}")
        print("🔍 Raw API response:\n", raw_response)  # Debugging: Print OpenAI's response
        return []

# Process each category and check for missing tools
print("🚀 Checking for missing AI tools...")

for super_category in data["super_categories"]:
    print(f"\n🔍 Checking Super Category: {super_category['title']}")
    
    for category in super_category["categories"]:
        existing_titles = [tool["title"] for tool in category["resources"]]
        print(f"  ➜ Checking Category: {category['title']} (Existing tools: {len(existing_titles)})")
        
        missing_tools = find_missing_tools(category["title"], existing_titles)
        
        if missing_tools:
            print(f"    ✅ Found {len(missing_tools)} missing tools! Adding them to the list.")
            category["resources"].extend(missing_tools)
        else:
            print(f"    ❌ No missing tools detected.")

# Save updated JSON to a new file
output_file = "data3.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"\n🎉 Updated AI tools list saved to {output_file}!")
