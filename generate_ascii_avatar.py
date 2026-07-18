import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ==========================================
# CONFIGURATION
# ==========================================

GITHUB_USERNAME = "Riess-01"

OUTPUT_DIR = "assets"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "ascii_avatar.gif"
)

WIDTH = 100
FONT_SIZE = 10

# Karakter ASCII
ASCII_CHARS = "@%#*+=-:. "


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ==========================================
# 1. GET GITHUB PROFILE
# ==========================================

print("[1/6] Connecting to GitHub...")

API_URL = (
    f"https://api.github.com/users/"
    f"{GITHUB_USERNAME}"
)

response = requests.get(API_URL)

if response.status_code != 200:
    raise Exception(
        "GitHub profile not found!"
    )

user_data = response.json()

avatar_url = user_data["avatar_url"]

print(
    f"[+] User found: "
    f"{user_data['login']}"
)


# ==========================================
# 2. DOWNLOAD AVATAR
# ==========================================

print(
    "[2/6] Downloading GitHub avatar..."
)

image_response = requests.get(
    avatar_url
)

image = Image.open(
    BytesIO(
        image_response.content
    )
).convert("L")


# ==========================================
# 3. RESIZE IMAGE
# ==========================================

print(
    "[3/6] Resizing image..."
)

aspect_ratio = (
    image.height /
    image.width
)

height = int(
    WIDTH *
    aspect_ratio *
    0.5
)

image = image.resize(
    (
        WIDTH,
        height
    )
)


# ==========================================
# 4. CONVERT IMAGE TO ASCII
# ==========================================

print(
    "[4/6] Converting image to ASCII..."
)


def image_to_ascii(
    img
):

    pixels = img.getdata()

    ascii_lines = []

    for y in range(
        img.height
    ):

        line = ""

        for x in range(
            img.width
        ):

            pixel = pixels[
                y *
                img.width +
                x
            ]

            index = int(
                pixel /
                256 *
                len(
                    ASCII_CHARS
                )
            )

            if index >= len(
                ASCII_CHARS
            ):

                index = (
                    len(
                        ASCII_CHARS
                    ) - 1
                )

            line += (
                ASCII_CHARS[
                    index
                ]
            )

        ascii_lines.append(
            line
        )

    return ascii_lines


ascii_lines = image_to_ascii(
    image
)


# ==========================================
# 5. CREATE GIF FRAMES
# ==========================================

print(
    "[5/6] Creating terminal animation..."
)


# Load monospace font
try:

    font = ImageFont.truetype(
        "DejaVuSansMono.ttf",
        FONT_SIZE
    )

except:

    font = ImageFont.load_default()


frames = []


# ------------------------------------------
# FRAME 1
# TERMINAL BOOT
# ------------------------------------------

boot_lines = [

    "> SYSTEM INITIALIZING...",
    "> CONNECTING TO GITHUB...",
    f"> USER: {GITHUB_USERNAME}",
    "> AUTHENTICATING PROFILE...",
    "> FETCHING AVATAR...",
    "> IMAGE FOUND",
    "> CONVERTING PIXELS...",
    "> GENERATING ASCII MATRIX...",
    "",
]


for i in range(
    len(boot_lines) + 1
):

    canvas = Image.new(
        "RGB",
        (
            1200,
            800
        ),
        "black"
    )

    draw = ImageDraw.Draw(
        canvas
    )

    text = "\n".join(
        boot_lines[:i]
    )

    draw.text(
        (
            40,
            40
        ),
        text,
        fill=(
            0,
            255,
            80
        ),
        font=font
    )

    frames.append(
        canvas
    )


# ------------------------------------------
# FRAME 2
# ASCII IMAGE APPEARS
# ------------------------------------------

for visible_lines in range(
    1,
    len(ascii_lines) + 1,
    2
):

    canvas = Image.new(
        "RGB",
        (
            1200,
            800
        ),
        "black"
    )

    draw = ImageDraw.Draw(
        canvas
    )

    ascii_text = "\n".join(
        ascii_lines[
            :visible_lines
        ]
    )

    draw.text(
        (
            40,
            150
        ),
        ascii_text,
        fill=(
            0,
            255,
            80
        ),
        font=font
    )

    frames.append(
        canvas
    )


# ------------------------------------------
# FRAME 3
# FINAL PROFILE
# ------------------------------------------

final_frame = Image.new(
    "RGB",
    (
        1200,
        800
    ),
    "black"
)

draw = ImageDraw.Draw(
    final_frame
)


# Terminal header

draw.text(
    (
        40,
        30
    ),
    "> PROFILE LOADED",
    fill=(
        0,
        255,
        80
    ),
    font=font
)


draw.text(
    (
        40,
        70
    ),
    f"> USER: {GITHUB_USERNAME}",
    fill=(
        0,
        255,
        80
    ),
    font=font
)


# ASCII portrait

draw.text(
    (
        40,
        130
    ),
    "\n".join(
        ascii_lines
    ),
    fill=(
        0,
        255,
        80
    ),
    font=font
)


# Footer

draw.text(
    (
        40,
        700
    ),
    "> SYSTEM STATUS: ONLINE_",
    fill=(
        0,
        255,
        80
    ),
    font=font
)


frames.append(
    final_frame
)


# ==========================================
# 6. SAVE GIF
# ==========================================

print(
    "[6/6] Saving GIF..."
)

frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0
)


# ==========================================
# DONE
# ==========================================

print()
print(
    "======================================"
)

print(
    " ASCII TERMINAL AVATAR CREATED"
)

print(
    "======================================"
)

print(
    f"Output: {OUTPUT_FILE}"
)

print(
    "Done!"
)