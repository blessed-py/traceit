import requests
import os


API_KEY = os.environ.get("API_KEY")  
MODEL = "lost-and-found-detector/2"



def detect_image(file_stream, filename):
    try:
        response = requests.post(
            f"https://detect.roboflow.com/{MODEL}",
            params={"api_key": API_KEY},
            files={"file": (filename, file_stream)}
        )

        result = response.json()
        print("RAW RESULT:", result)

        if "predictions" in result and result["predictions"]:

            predictions = result["predictions"]

            # Normalize class names
            for p in predictions:
                p["class"] = p["class"].lower()

            # Ignore unnecessary classes
            ignore = ["person"]

            # Priority items (important for your system)
            priority_items = [
                "phone",
                "laptop",
                "wallet",
                "keys",
                "luggage-and-bags",
                "suitcase"
            ]

            #  PRIORITY MATCH FIRST
            for p in predictions:
                if p["class"] in priority_items:
                    return build_response(p)

            # 🔍 FILTER OUT IGNORED
            filtered = [
                p for p in predictions
                if p["class"] not in ignore
            ]

            if filtered:
                best = max(filtered, key=lambda x: x["confidence"])

                if best["confidence"] > 0.6:
                    return build_response(best)

                return {
                    "label": "Uncertain",
                    "confidence": round(best["confidence"], 2),
                    "category": "Other",
                    "box": None
                }

            # fallback
            best = max(predictions, key=lambda x: x["confidence"])
            return build_response(best)

        return {
            "label": "Unknown",
            "confidence": 0,
            "category": "Other",
            "box": None
        }

    except Exception as e:
        print("[AI ERROR]", e)
        return {
            "label": "Error",
            "confidence": 0,
            "category": "Other",
            "box": None
        }


def build_response(pred):
    label_raw = pred["class"]
    label_clean = label_raw.replace("-", " ").title()

    return {
        "label": label_clean,
        "confidence": round(pred["confidence"], 2),
        "category": map_category(label_raw),
        "box": {
            "x": pred.get("x"),
            "y": pred.get("y"),
            "width": pred.get("width"),
            "height": pred.get("height")
        }
    }


def map_category(label):
    label = label.lower()

    if label in ["phone", "laptop", "mouse"]:
        return "Electronics"

    elif label in ["wallet"]:
        return "Wallet"

    elif label in ["keys"]:
        return "Keys"

    elif label in ["luggage-and-bags", "suitcase"]:
        return "Bag"

    elif label in ["shoes"]:
        return "Clothing"

    elif label in ["id card", "id-card"]:
        return "ID Card"

    elif label in ["ring", "necklace", "watch"]:
        return "Jewelry"

    elif label in ["book", "document"]:
        return "Documents"

    else:
        return "Other"




