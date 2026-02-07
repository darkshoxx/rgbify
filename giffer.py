from PIL import Image
from pathlib import Path
HERE = Path(__file__).parent
SOURCE_FOLDER = HERE / "SourceImages"
FINAL_FOLDER = HERE / "FinalImages"
SEQUENCE_FOLDER = FINAL_FOLDER / "ColourPost2_50"


frames = [Image.open(p) for p in sorted(SEQUENCE_FOLDER.iterdir()) if p.suffix == ".png"]

frames[0].save(
    SEQUENCE_FOLDER / "output.gif",
    save_all=True,
    append_images=frames[1:],
    duration=5,  # ms per frame
    loop=0         # 0 = infinite loop
)
print("Gif Created!")