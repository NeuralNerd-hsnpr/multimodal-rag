"""Caption every image in data/corpus once and write data/corpus/captions.json.

Run this only when images are added or changed. The demo reads the committed captions and
never loads this model, which keeps a 674 MB download out of the first run.
"""

import json
from pathlib import Path

from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor

MODEL = "microsoft/git-base-coco"
CORPUS = Path(__file__).resolve().parent.parent / "data" / "corpus"

processor = AutoProcessor.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

captions = {}
for path in sorted(CORPUS.iterdir()):
    if path.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    pixels = processor(images=Image.open(path).convert("RGB"), return_tensors="pt").pixel_values
    output = model.generate(pixel_values=pixels, max_new_tokens=40)
    captions[path.name] = processor.batch_decode(output, skip_special_tokens=True)[0].strip()
    print(f"{path.name}: {captions[path.name]}")

(CORPUS / "captions.json").write_text(json.dumps(captions, indent=2) + "\n")
