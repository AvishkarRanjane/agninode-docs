import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_qr(url, filename, label="AgniNode"):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0f172a", back_color="#ffffff").convert('RGBA')

    # Draw a stylized center badge if desired
    width, height = img.size
    badge_size = int(width * 0.22)
    badge = Image.new('RGBA', (badge_size, badge_size), (255, 255, 255, 0))
    bdraw = ImageDraw.Draw(badge)
    
    # Rounded badge box
    bdraw.rounded_rectangle([0, 0, badge_size, badge_size], radius=badge_size//5, fill="#ea580c")
    bdraw.rounded_rectangle([2, 2, badge_size-2, badge_size-2], radius=badge_size//5, outline="#ffffff", width=2)
    
    # Simple Flame icon drawing
    cx, cy = badge_size // 2, badge_size // 2
    bdraw.ellipse([cx - badge_size//3, cy - badge_size//4, cx + badge_size//3, cy + badge_size//2.5], fill="#fbbf24")
    bdraw.polygon([
        (cx, cy - badge_size//2.5),
        (cx - badge_size//3.5, cy + badge_size//6),
        (cx + badge_size//3.5, cy + badge_size//6)
    ], fill="#f97316")
    bdraw.ellipse([cx - badge_size//5, cy + badge_size//8, cx + badge_size//5, cy + badge_size//2.8], fill="#ffffff")

    pos = ((width - badge_size) // 2, (height - badge_size) // 2)
    img.paste(badge, pos, badge)
    
    img.save(filename, format="PNG")
    print(f"Generated QR Code: {filename} -> {url}")
    return img

def generate_branded_poster(qr_img, url, filename="AgniNode_Scan_Card.png"):
    # Create an elegant high-res card 800 x 1100
    card_w, card_h = 800, 1100
    card = Image.new("RGBA", (card_w, card_h), "#0b0f19")
    draw = ImageDraw.Draw(card)

    # Top accent gradient bar
    draw.rectangle([0, 0, card_w, 14], fill="#f97316")

    # Outer border
    draw.rounded_rectangle([20, 20, card_w - 20, card_h - 20], radius=24, outline="#1e293b", width=3)

    # AgniNode Pill badge
    draw.rounded_rectangle([card_w//2 - 130, 45, card_w//2 + 130, 85], radius=20, fill="#1e293b")
    draw.text((card_w//2, 65), "AGNI-NODE ARCHIVE", fill="#f97316", anchor="mm")

    # Title
    draw.text((card_w//2, 120), "Smart Fire Suppression System", fill="#ffffff", anchor="mm")
    draw.text((card_w//2, 155), "Official Documentation & Working Demonstrations", fill="#94a3b8", anchor="mm")

    # QR Code container with rounded white background
    qr_box_size = 460
    qr_resized = qr_img.resize((qr_box_size, qr_box_size), Image.Resampling.LANCZOS)
    qr_x = (card_w - qr_box_size) // 2
    qr_y = 195

    draw.rounded_rectangle([qr_x - 16, qr_y - 16, qr_x + qr_box_size + 16, qr_y + qr_box_size + 16], radius=24, fill="#ffffff", outline="#f97316", width=4)
    card.paste(qr_resized, (qr_x, qr_y), qr_resized)

    # Scan instruction
    draw.rounded_rectangle([card_w//2 - 170, qr_y + qr_box_size + 30, card_w//2 + 170, qr_y + qr_box_size + 70], radius=20, fill="#ea580c")
    draw.text((card_w//2, qr_y + qr_box_size + 50), "SCAN TO ACCESS ALL FILES & VIDEOS", fill="#ffffff", anchor="mm")

    # Features / Files List Box
    box_y = qr_y + qr_box_size + 95
    draw.rounded_rectangle([50, box_y, card_w - 50, card_h - 90], radius=16, fill="#111827", outline="#1f2937", width=2)

    items = [
        " AgniNode Working Demo (Full HD Video - 01:00 min)",
        " Aerosol Module Discharge Test (1080p Video - 11 sec)",
        " NCRB Accidental Fire Deaths in India (2021-2025)",
        " NCRB Electrical Short Circuit Fires (2021-2025)",
        " Reducing Electrical Fire Deaths: Components & Evidence"
    ]

    draw.text((70, box_y + 25), "INCLUDED IN THIS SCANNER:", fill="#f97316")
    curr_y = box_y + 55
    for item in items:
        draw.text((70, curr_y), item, fill="#e2e8f0")
        curr_y += 30

    # Footer URL
    draw.text((card_w//2, card_h - 55), url, fill="#64748b", anchor="mm")
    draw.text((card_w//2, card_h - 35), "Compatible with iPhone Camera, Android, Google Lens & WhatsApp", fill="#475569", anchor="mm")

    card.save(filename, format="PNG")
    print(f"Generated Branded Scan Card: {filename}")

if __name__ == "__main__":
    public_url = "https://avishkarranjane.github.io/agninode-docs/"
    local_url = "http://192.168.1.5:8080/"

    # Generate Public QR Code
    pub_qr = generate_qr(public_url, "AgniNode_QR_Public.png")
    generate_branded_poster(pub_qr, public_url, "AgniNode_Scan_Card.png")

    # Generate Local Wi-Fi QR Code
    loc_qr = generate_qr(local_url, "AgniNode_QR_Local_WiFi.png")
    generate_branded_poster(loc_qr, local_url, "AgniNode_Scan_Card_Local_WiFi.png")

    # Generate SVG version of public QR
    import qrcode.image.svg
    svg_factory = qrcode.image.svg.SvgPathImage
    svg_qr = qrcode.make(public_url, image_factory=svg_factory)
    svg_qr.save("AgniNode_QR_Public.svg")
    print("Generated SVG QR Code: AgniNode_QR_Public.svg")
