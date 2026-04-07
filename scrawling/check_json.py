import json

with open("i:/My Drive/Sumatra Westkust/webjalur/scrawling/Data_BGS_Sumatra_Full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")

origins = {}
destinations = {}
focus_dest_same = 0

for d in data:
    asal = d.get("Asal")
    tujuan = d.get("Tujuan")
    
    origins[asal] = origins.get(asal, 0) + 1
    destinations[tujuan] = destinations.get(tujuan, 0) + 1
    
    # Check if Asal and Tujuan are the same or if Tujuan is empty
    if callable(getattr(tujuan, "lower", None)) and callable(getattr(asal, "lower", None)):
        if tujuan.lower() == asal.lower():
            focus_dest_same += 1
    elif not tujuan:
        pass

print("Top 5 Asal:", sorted(origins.items(), key=lambda x: -x[1])[:5])
print("Top 5 Tujuan:", sorted(destinations.items(), key=lambda x: -x[1])[:5])
print(f"Count where Asal == Tujuan: {focus_dest_same}")

# Let's inspect 2 cases where Asal == Tujuan
print("\n--- Examples where Asal == Tujuan ---")
examples = [d for d in data if d.get("Asal", "").lower() == d.get("Tujuan", "").lower()][:2]
for e in examples:
    print(f"URL: {e.get('URL')}, Asal: {e.get('Asal')}, Tujuan: {e.get('Tujuan')}")

print("\n--- Examples where Asal != Tujuan ---")
examples2 = [d for d in data if d.get("Asal", "").lower() != d.get("Tujuan", "").lower() and d.get("Tujuan")][:2]
for e in examples2:
    print(f"URL: {e.get('URL')}, Asal: {e.get('Asal')}, Tujuan: {e.get('Tujuan')}")
