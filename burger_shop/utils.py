from PIL import Image
from django.conf import settings
import os

def generate_burger_image(ingredient_images, burger_id, top_bun_image):
    # Load bottom bun
    bottom_bun_path = os.path.join(settings.MEDIA_ROOT, 'burger_components/bottom-bun.png')
    bottom_bun = Image.open(bottom_bun_path)

    # Load top bun
    top_bun_path = os.path.join(settings.MEDIA_ROOT, top_bun_image)
    top_bun = Image.open(top_bun_path)

    # Load the middle ingredients
    middle_images = [Image.open(os.path.join(settings.MEDIA_ROOT, img_path)) for img_path in ingredient_images]

    all_images = [top_bun] + middle_images + [bottom_bun]

    # Get total height and max width
    total_height = sum(img.height for img in all_images)
    max_width = 300

    # Create a blank image (white background or transparent)
    final_image = Image.new('RGBA', (max_width, total_height), (255, 255, 255, 0))

    # Paste images on top of each other
    y_offset = 0
    for img in all_images:
        final_image.paste(img, (0, y_offset), img)  # Use image as mask for transparency
        y_offset += img.height -20

    final_folder = os.path.join(settings.MEDIA_ROOT, 'custom_burgers')
    os.makedirs(final_folder, exist_ok=True)

    # Save the final image
    final_path = os.path.join(final_folder, f'custom-burger-id-{burger_id}.png')
    final_image.save(final_path)

    return f'custom_burgers/custom-burger-id-{burger_id}.png'
