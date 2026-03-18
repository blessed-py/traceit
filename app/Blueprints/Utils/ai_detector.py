import requests
import os

API_KEY = os.environ.get("API_KEY")
MODEL = "objects-nqpna/14"

def detect_image(file_stream, filename):
    try:
        response = requests.post(
            f"https://detect.roboflow.com/{MODEL}",
            params={"api_key": API_KEY},
            files={"file": (filename, file_stream)}
        )

        result = response.json()
        print("RAW RESULT:", result)

        if "predictions" in result and len(result["predictions"]) > 0:

            ignore = ["person"]

            priority_items = ["bottle", "cell phone", "laptop", "backpack", "book", "bag"]

            predictions = result["predictions"]

            # PRIORITY CHECK
            for p in predictions:
                if p["class"] in priority_items:
                    return p["class"], p["confidence"]

            # FILTER
            filtered = [p for p in predictions if p["class"] not in ignore]

            if filtered:
                best = max(filtered, key=lambda x: x["confidence"])

                if best["confidence"] > 0.75:
                    return best["class"], best["confidence"]

                return "Uncertain", best["confidence"]

            # fallback
            best = max(predictions, key=lambda x: x["confidence"])
            return best["class"], best["confidence"]

        return "Unknown", 0

    except Exception as e:
        print("[AI ERROR]", e)
        return "Unknown", 0
    
def map_category(label):
    label = label.lower()

    if "phone" in label:
        return "Electronics"
    elif "backpack" in label or "bag" in label:
        return "Bag"
    elif "laptop" in label:
        return "Electronics"
    elif "book" in label:
        return "Documents"
    elif "bottle" in label:
        return "Other"
    else:
        return "Other"
