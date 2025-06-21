import requests
from bs4 import BeautifulSoup
import json
import time

SERPAPI_KEY = "656279a8d3fdd09da95382a41283fc3b01e1ceb9227c3b2b52268ea2790e701b"
TRUSTED_SITES = ["cdc.gov", "mayoclinic.org", "clevelandclinic.org", "who.int"]

def search_question(question):
    url = "https://serpapi.com/search"
    params = {
        "q": question,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 5
    }
    res = requests.get(url, params=params)
    results = res.json().get("organic_results", [])
    for r in results:
        link = r.get("link", "")
        if any(site in link for site in TRUSTED_SITES):
            return link
    return None

def extract_answer(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        # Grab first <p> tag with decent text length
        for p in soup.find_all("p"):
            text = p.get_text().strip()
            if len(text) > 100:
                return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def load_questions():
    with open("data/questions.json") as f:
        return json.load(f)

def save_answers(answers):
    with open("data/ground_truth.json", "w") as f:
        json.dump(answers, f, indent=2)

if __name__ == "__main__":
    questions = load_questions()
    ground_truth = []

    for i, entry in enumerate(questions):
        q = entry["question"]
        print(f"\n[{i+1}] Searching: {q}")

        link = search_question(q)
        print(f" → Top result: {link}")

        if link:
            answer = extract_answer(link)
            if answer:
                ground_truth.append({ "question": q, "answer": answer })
            else:
                print(" ⚠️ No usable paragraph found.")
                ground_truth.append({ "question": q, "answer": "" })
        else:
            print(" ❌ No trusted site found.")
            ground_truth.append({ "question": q, "answer": "" })

        time.sleep(2)  # Avoid hitting rate limits

    save_answers(ground_truth)
    print("\n✅ Ground truth saved to data/ground_truth.json")
