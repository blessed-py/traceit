from app.Blueprints.Utils.ai_detector import detect_image

# use your real image path
image_path = "/Users/blessed/Downloads/dataset/bag.webp"

result = detect_image(image_path)

print("RESULT:", result)  