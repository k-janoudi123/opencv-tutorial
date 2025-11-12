import cv2
import easyocr
import numpy as np
import re

reader = easyocr.Reader(["en"], verbose=False)

# Read image
img = cv2.imread("assets/plate-number-3.jpg")

if img is None:
    print("ERROR: Could not load image!")
    exit()

print("Original image size:", img.shape)
# get the height and width
height, width = img.shape[:2]

# Cropping out left side (KUWAIT) and keep main plate area
crop_x_start = int(width * 0.12)  # Skip "KUWAIT" column
cropped = img[:, crop_x_start:]

# Adding padding to the image, so that text near edges are better detected
padding = 30
cropped = cv2.copyMakeBorder(
    cropped,
    padding,
    padding,
    padding,
    padding,
    cv2.BORDER_CONSTANT,
    value=[255, 255, 255],
)

# Convert to grayscale
gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

# Enhance
gray = cv2.convertScaleAbs(gray, alpha=1.3, beta=20)

# Save for debugging
cv2.imwrite("assets/preprocessed.jpg", gray)

# OCR - detect all text
results = reader.readtext(gray, allowlist="0123456789")

print("\n" + "=" * 50)
print("ALL NUMBER DETECTIONS:")
print("=" * 50)

detections = []
print(results)

# results look like:
# x1,y1 .. are the 4 corners of the bbox
# [([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 'text', confidence), ...]

for bbox, text, confidence in results:
    # if text contains numbers only
    numbers = re.sub(r"[^0-9]", "", text)

    if numbers and confidence > 0.5:  # Filter by confidence
        detections.append({"text": numbers, "confidence": confidence})


print("detections", detections)

# detections [{'text': '4', 'confidence': np.float64(0.9936174993473657)},
#  {'text': '66759', 'confidence': np.float64(0.9999540581255164)}]


# Iteration 1:

# bbox = [[300, 114], [494, 114], [494, 386], [300, 386]]
# text = '4'
# confidence = 0.9936174993473657

district_candidates = [d for d in detections if len(d["text"]) in [1, 2]]
main_candidates = [d for d in detections if len(d["text"]) == 5]

district = district_candidates[0]["text"] if district_candidates else ""
main_number = main_candidates[0]["text"] if main_candidates else ""

# Check for horizontal layout (6-7 digits together)
combined_candidates = [d for d in detections if len(d["text"]) in [6, 7]]

print(f"District candidates (1-2 digits): {[d['text'] for d in district_candidates]}")
print(f"Main candidates (5 digits): {[d['text'] for d in main_candidates]}")
print(f"Combined candidates (6-7 digits): {[d['text'] for d in combined_candidates]}")

# output:
# District candidates (1-2 digits): ['4']
# Main candidates (5 digits): ['66759']
# Combined candidates (6-7 digits): []
district = ""
main_number = ""

# Scenario 1: Horizontal layout (all together: "466759" or "1266759")
if combined_candidates and not (district_candidates and main_candidates):
    combined = combined_candidates[0]["text"]

    if len(combined) == 6:
        # 1-digit district + 5-digit main
        district = combined[0]
        main_number = combined[1:]
        print(f"\nLayout: HORIZONTAL (1+5)")
    elif len(combined) == 7:
        # 2-digit district + 5-digit main
        district = combined[0:2]
        main_number = combined[2:]
        print(f"\nLayout: HORIZONTAL (2+5)")

# Scenario 2: Vertical layout (separate detections)
elif district_candidates and main_candidates:
    district = district_candidates[0]["text"]
    main_number = main_candidates[0]["text"]
    print(f"\nLayout: VERTICAL")

# Scenario 3: Only found main number
elif main_candidates:
    main_number = main_candidates[0]["text"]
    print(f"\nLayout: PARTIAL (main only)")

# Scenario 4: Only found district
elif district_candidates:
    district = district_candidates[0]["text"]
    print(f"\nLayout: PARTIAL (district only)")

print(f"District: {district}")
print(f"Main: {main_number}")

# Final result
if district and main_number:
    license_plate = f"{district}-{main_number}"
    print(f"\n*** FINAL LICENSE PLATE: {license_plate} ***")
elif main_number:
    license_plate = main_number
    print(f"\n*** PARTIAL: {license_plate} ***")
elif district:
    license_plate = district
    print(f"\n*** PARTIAL: {license_plate} ***")
else:
    license_plate = "".join([d["text"] for d in detections])
    print(f"\n*** FALLBACK: {license_plate} ***")


print("\nSaved result.jpg")


## **How It Works:**

# 1. **Detects all numbers** in the plate
# 2. **Sorts by Y-position** (top to bottom)
# 3. **Identifies layout:**
#    - If 1-digit on top + 5-digits below → **Vertical** → "4-66759"
#    - If 6-digits together → **Horizontal** → "4-66759"
# 4. **Combines correctly** regardless of layout

# ---

## **Expected Output for Your Image:**

# ALL NUMBER DETECTIONS:
# Text: '4' | Position: (x=300, y=150) | Conf: 85%
# Text: '66759' | Position: (x=400, y=450) | Conf: 78%

# SORTED (top to bottom):
# 4 at y=150
# 66759 at y=450

# Layout: VERTICAL
# District: 4
# Main: 66759

# ✓ FINAL LICENSE PLATE: 4-66759
# ```

# ---

# ## **For Horizontal Layout (Other Plates):**
# ```
# ALL NUMBER DETECTIONS:
# Text: '466759' | Position: (x=400, y=300) | Conf: 82%

# Layout: HORIZONTAL
# District: 4
# Main: 66759

# ✓ FINAL LICENSE PLATE: 4-66759


## **Now Handles All Cases:**

### **Case 1: Vertical with 1-digit district (Your image)**
# ```
# Detections: '4', '66759'
# → District: 4
# → Main: 66759
# → Result: 4-66759 ✅
# ```

# ### **Case 2: Vertical with 2-digit district**
# ```
# Detections: '12', '66759'
# → District: 12
# → Main: 66759
# → Result: 12-66759 ✅
# ```

# ### **Case 3: Horizontal with 1-digit district**
# ```
# Detections: '466759'
# → Split: district='4', main='66759'
# → Result: 4-66759 ✅
# ```

# ### **Case 4: Horizontal with 2-digit district**
# ```
# Detections: '1266759'
# → Split: district='12', main='66759'
# → Result: 12-66759 ✅


# Without border
# ┌────────┐
# │  4     │
# │ 66759  │
# └────────┘

# # With white border (padding=30)
# ┌──────────────┐
# │              │ ← 30px white padding
# │  ┌────────┐  │
# │  │  4     │  │
# │  │ 66759  │  │
# │  └────────┘  │
# │              │ ← 30px white padding
# └──────────────┘
