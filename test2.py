import concurrent.futures
import openai
import json
import os

def get_response(message):
    response = openai.ChatCompletion.create(
        # model = 'gpt-3.5-turbo',
        model = 'gpt-4',
        temperature = 0.7,
        messages = [
            {'role': 'user', 'content': f'{message}'}
        ]
    )
    return response.choices[0]["message"]["content"]

chunks = [""]
with open("output.json", "r") as f:
    data = json.load(f)
    for item in data:
        txt = "\n".join(item["text"])
        if "carry" in txt:
            chunks[-1] += "\n\n" + txt
            if len(chunks[-1]) > 6000:
                chunks.append("")
print("Chunks", len(chunks))

with open("lines.txt", "w+") as f:
    f.write("\n".join(chunks))

results = []

def run(i, chunk):
    prompt = f"""
        I need to find historical gun laws analogous. From the list of historical gun laws below, please select the ones that are most similar to: 0) private property restrictions, 1) restrictions in city-owned buildings, 2) restrictions in federal / state buildings, 3) restrictions in school or child care facilities, 4) restrictions in public parks, 5) restrictions in shelters to protect at-risk people, 6) restrictions in nature preserves, 7) restrictions in voter service centers, 8) restrictions in public transportation, 9) restrictions in liquor establishments, 10) restrictions at public gatherings, 11) restrictions at entertainment establishments, 12) restrictions at cannabis dispensaries, and 13) restrictions at healthcare facilities. If no historical gun law was found analogous, just skip it in your answer. Provide the excerpt of the appropriate gun law in your answer. Include laws only about carrying guns, not about firing or shooting guns.

        Historical gun laws:
        {chunk}
    """
    response = get_response(prompt)
    print(response)
    os.makedirs("output", exist_ok=True)
    with open(f"output/response-{i}.txt", "w+") as f:
        f.write(response)
    return response

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(run, i, chunk) for i, chunk in enumerate(chunks)]
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())