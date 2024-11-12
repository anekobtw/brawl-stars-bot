import os

import requests
from brawlstats import Player
from PIL import Image, ImageColor, ImageDraw, ImageEnhance, ImageFilter, ImageFont


def download_image(url: str, filename: str) -> str:
    """Download an image and save it locally."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
    else:
        image = Image.new("RGBA", (500, 500), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("LilitaOne-Regular.ttf", 60)
        draw.text((50, 200), "Image not found", font=font, fill=(255, 255, 255))
        image.save(filename)
    return filename


def download_brawler(brawler_id: int) -> str:
    """Download brawler image."""
    return download_image(f"https://cdn.brawlstats.com/character-arts/{brawler_id}.png", f"brawler - {brawler_id}.png")


def download_icon(icon_id: int) -> str:
    """Download player icon image."""
    return download_image(f"https://cdn.brawlstats.com/player-thumbnails/{icon_id}.png", f"icon - {icon_id}.png")


def generate_description(player: Player) -> str:
    """Generate description text for a player."""
    return f"""
Trophies: {player.trophies} (highest {player.highest_trophies})
Exp level: {player.exp_level} ({player.exp_points})
Brawlers: {len(player.brawlers)} / 85

Solo showdown victories: {player.solo_victories}
Duo showdown victories: {player.duo_victories}
3vs3 victories: {player.x3vs3_victories}
"""


def generate_profile(brawler_id: int, icon_id: int, name: str, name_color: str, description: str):
    """Generate a profile image for a player."""
    profile = Image.new("RGBA", (500, 500), (0, 0, 0))

    # Download images
    brawler_image = Image.open(download_brawler(brawler_id))
    icon_image = Image.open(download_icon(icon_id))

    # Background
    blurred_brawler_image = brawler_image.filter(ImageFilter.GaussianBlur(radius=10))
    darker_brawler_image = ImageEnhance.Brightness(blurred_brawler_image).enhance(0.30)
    saturated_brawler_image = ImageEnhance.Color(darker_brawler_image).enhance(1.3)
    profile.paste(saturated_brawler_image, (0, 0))

    # Icon
    profile.paste(icon_image.resize((100, 100)), (20, 75))

    # Text
    draw = ImageDraw.Draw(profile)
    color = "#" + name_color.lstrip("0x")
    draw.text((150, 75), name, font=ImageFont.truetype("Pusia-Bold.otf", 40, encoding="UTF-8"), fill=ImageColor.getcolor(color, "RGBA"))
    draw.text((150, 110), description, font=ImageFont.truetype("Pusia-Bold.otf", 17, encoding="UTF-8"), fill=(255, 255, 255))

    # Save the final image
    profile.save(f"{name}.png")
    os.remove(f"brawler - {brawler_id}.png")
    os.remove(f"icon - {icon_id}.png")
