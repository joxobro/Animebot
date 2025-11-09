import json

# Ma'lumotlarni o'qish
with open('bot_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Kanallarni yangilash
data['main_channels'] = [-1002924787403]  # Asosiy kanal
data['channels'] = [-1001640219491]  # Majburiy obuna kanali

# Saqlash
with open('bot_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Kanallar yangilandi!")
print(f"Asosiy kanal: {data['main_channels']}")
print(f"Majburiy obuna: {data['channels']}")
