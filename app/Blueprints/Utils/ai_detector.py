import requests

API_KEY = "62nlqetIfWiUoeX9d7yS"
MODEL = "objects-nqpna/14"

def detect_image(image_path):
    try:
        with open(image_path, "rb") as f:
            response = requests.post(
                f"https://detect.roboflow.com/{MODEL}",
                params={"api_key": API_KEY},
                files={"file": f}
            )

        result = response.json()
        print("RAW RESULT:", result)

        if "predictions" in result and len(result["predictions"]) > 0:

            ignore = ["person"]

            # Priority items (important for your system)
            priority_items = ["bottle", "cell phone", "laptop", "backpack", "book", "bag"]

            predictions = result["predictions"]

            # Step 1: Check if any priority item exists
            for p in predictions:
                if p["class"] in priority_items:
                    return p["class"], p["confidence"]

            # Step 2: Remove useless ones
            filtered = [p for p in predictions if p["class"] not in ignore]

            if filtered:
                best = max(filtered, key=lambda x: x["confidence"])

                # Confidence check
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