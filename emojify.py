import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found! Set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load JSON file
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Function to rewrite text with emojis using OpenAI API
def rewrite_with_emojis(text, text_type="description"):
    prompt_type = {
        "description": "Rewrite the following text using appropriate emojis while keeping it clear and professional:",
        "category": "Rewrite this category title by adding appropriate emojis while keeping it concise and readable:"
    }
    
    prompt = f"{prompt_type[text_type]}\n\n{text}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You enhance text by adding relevant emojis for better readability."},
                  {"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

# Process each category's content and update titles
print("🚀 Starting emoji enhancement process...\n")

for super_category in data["super_categories"]:
    print(f"🟢 Processing Super Category: {super_category['title']}")

    for category in super_category["categories"]:
        print(f"  🔵 Enhancing Category: {category['title']}...")
        category["title"] = rewrite_with_emojis(category["title"], text_type="category")  # Update category title

        for resource in category["resources"]:
            print(f"    🟡 Updating: {resource['title']}...")
            resource["content"] = rewrite_with_emojis(resource["content"], text_type="description")  # Update resource descriptions

print("\n✅ Emoji enhancement complete! Saving updated data to 'data2.json'...")

# Save updated JSON to a new file
with open("data2.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("🎉 Data has been successfully updated with emojis and saved to 'data2.json'!")
