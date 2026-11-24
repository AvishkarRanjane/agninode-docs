import os
import socket
import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_M
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgPathImage
from PIL import Image, ImageDraw, ImageFont


def get_font(
    name: str,
    size: int
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    fonts_dir = os.path.join(
        os.environ.get('WINDIR', 'C:\\Windows'),
        'Fonts'
    )
    path = os.path.join(fonts_dir, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def generate_clean_qr(url: str, filename: str) -> Image.Image:
    """Generate clean, ultra-high-contrast QR code without center badge."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=16,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=PilImage,
        fill_color="#000000",
        back_color="#ffffff"
    )
    pil_img: Image.Image = img.get_image().convert('RGBA')
    pil_img.save(filename, format="PNG")
    print(f"Generated Clean QR: {filename} -> {url}")
    return pil_img


def generate_branded_qr(url: str, filename: str) -> Image.Image:
    """Generate high-contrast QR code with Level H error correction."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=16,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=PilImage,
        fill_color="#090d16",
        back_color="#ffffff"
    )
    pil_img: Image.Image = img.get_image().convert('RGBA')
    width, height = pil_img.size

    # Badge size: exactly 20% of total QR size
    badge_size = int(width * 0.20)
    badge = Image.new('RGBA', (badge_size, badge_size), (255, 255, 255, 0))
    bdraw = ImageDraw.Draw(badge)

    # Rounded orange badge with border
    bdraw.rounded_rectangle(
        [0, 0, badge_size, badge_size],
        radius=badge_size // 4,
        fill="#ea580c"
    )
    bdraw.rounded_rectangle(
        [2, 2, badge_size - 2, badge_size - 2],
        radius=badge_size // 4,
        outline="#ffffff",
        width=3
    )

    # Stylized flame symbol
    cx, cy = badge_size // 2, badge_size // 2
    bdraw.ellipse(
        [
            cx - badge_size // 3,
            cy - badge_size // 4,
            cx + badge_size // 3,
            cy + int(badge_size // 2.5)
        ],
        fill="#fbbf24"
    )
    bdraw.polygon(
        [
            (cx, cy - int(badge_size // 2.4)),
            (cx - int(badge_size // 3.2), cy + badge_size // 6),
            (cx + int(badge_size // 3.2), cy + badge_size // 6)
        ],
        fill="#f97316"
    )
    bdraw.ellipse(
        [
            cx - badge_size // 5,
            cy + badge_size // 9,
            cx + badge_size // 5,
            cy + int(badge_size // 2.8)
        ],
        fill="#ffffff"
    )

    pos = ((width - badge_size) // 2, (height - badge_size) // 2)
    pil_img.paste(badge, pos, badge)
    pil_img.save(filename, format="PNG")
    print(f"Generated Branded QR: {filename} -> {url}")
    return pil_img


def generate_presentation_card_dark(
    qr_img: Image.Image,
    url: str,
    filename: str = "assets/qr/AgniNode_Scan_Card.png"
) -> None:
    """Generate high-resolution dark-mode presentation placard."""
    card_w, card_h = 900, 1320
    card = Image.new("RGBA", (card_w, card_h), "#070a13")
    draw = ImageDraw.Draw(card)

    font_title = get_font("segoeuib.ttf", 34)
    font_sub = get_font("segoeui.ttf", 20)
    font_badge = get_font("segoeuib.ttf", 15)
    font_pill = get_font("segoeuib.ttf", 18)
    font_sec = get_font("segoeuib.ttf", 19)
    font_item = get_font("segoeui.ttf", 17)
    font_mono = get_font("arialbd.ttf", 16)
    font_small = get_font("segoeui.ttf", 14)

    # Top accent glowing bar
    draw.rectangle([0, 0, card_w, 14], fill="#f97316")

    # Card outer border
    draw.rounded_rectangle(
        [18, 18, card_w - 18, card_h - 18],
        radius=24,
        outline="#1e293b",
        width=2
    )

    # Top Pill Badge
    badge_w = 260
    badge_x = (card_w - badge_w) // 2
    draw.rounded_rectangle(
        [badge_x, 42, badge_x + badge_w, 78],
        radius=18,
        fill="#1e293b"
    )
    draw.text(
        (card_w // 2, 60),
        "AGNI-NODE ARCHIVE",
        fill="#f97316",
        font=font_badge,
        anchor="mm"
    )

    # Header Titles
    draw.text(
        (card_w // 2, 114),
        "Autonomous Fire Suppression System",
        fill="#ffffff",
        font=font_title,
        anchor="mm"
    )
    draw.text(
        (card_w // 2, 154),
        "Official Documentation, Field Videos & Casualty Analysis Reports",
        fill="#94a3b8",
        font=font_sub,
        anchor="mm"
    )

    # QR Code Container
    qr_box_size = 500
    qr_resized = qr_img.resize(
        (qr_box_size, qr_box_size),
        Image.Resampling.LANCZOS
    )
    qr_x = (card_w - qr_box_size) // 2
    qr_y = 195

    # Glowing rounded container for QR
    box_rect = [
        qr_x - 18,
        qr_y - 18,
        qr_x + qr_box_size + 18,
        qr_y + qr_box_size + 18
    ]
    draw.rounded_rectangle(
        box_rect,
        radius=24,
        fill="#ffffff",
        outline="#f97316",
        width=4
    )
    card.paste(qr_resized, (qr_x, qr_y), qr_resized)

    # Scan Action Pill Button
    pill_w = 460
    pill_x = (card_w - pill_w) // 2
    pill_y = qr_y + qr_box_size + 36
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_w, pill_y + 50],
        radius=25,
        fill="#ea580c"
    )
    draw.text(
        (card_w // 2, pill_y + 25),
        "SCAN WITH PHONE CAMERA TO OPEN",
        fill="#ffffff",
        font=font_pill,
        anchor="mm"
    )

    # Files List Container
    box_y = pill_y + 72
    box_h = 320
    draw.rounded_rectangle(
        [48, box_y, card_w - 48, box_y + box_h],
        radius=18,
        fill="#0f172a",
        outline="#1e293b",
        width=2
    )

    draw.text(
        (74, box_y + 24),
        "FILES & MEDIA INCLUDED IN THIS SCANNER:",
        fill="#f97316",
        font=font_sec
    )

    items = [
        ("►", " AgniNode Working Demo (Full HD 1080p - 01:00 min)"),
        ("►", " Aerosol Module Test (1080p High-Speed - 00:11 sec)"),
        ("📄", " NCRB Accidental Fire Deaths in India (2021-2025)"),
        ("📄", " NCRB Electrical Short Circuit Fires (2021-2025)"),
        ("📄", " Reducing Electrical Fire Deaths in India")
    ]

    curr_y = box_y + 64
    for icon, text in items:
        draw.text((74, curr_y), icon, fill="#f97316", font=font_item)
        draw.text((104, curr_y), text, fill="#f1f5f9", font=font_item)
        curr_y += 48

    # Footer Section
    draw.text(
        (card_w // 2, card_h - 66),
        url,
        fill="#f97316",
        font=font_mono,
        anchor="mm"
    )
    draw.text(
        (card_w // 2, card_h - 38),
        "Compatible with iPhone, Android, Google Lens & WhatsApp",
        fill="#64748b",
        font=font_small,
        anchor="mm"
    )

    card.save(filename, format="PNG")
    print(f"Generated Dark Scan Card: {filename}")


def generate_presentation_card_light(
    qr_img: Image.Image,
    url: str,
    filename: str = "assets/qr/AgniNode_Scan_Card_Light.png"
) -> None:
    """Generate print-ready light card (ideal for standard office printers)."""
    card_w, card_h = 900, 1320
    card = Image.new("RGBA", (card_w, card_h), "#ffffff")
    draw = ImageDraw.Draw(card)

    font_title = get_font("segoeuib.ttf", 34)
    font_sub = get_font("segoeui.ttf", 20)
    font_badge = get_font("segoeuib.ttf", 15)
    font_pill = get_font("segoeuib.ttf", 18)
    font_sec = get_font("segoeuib.ttf", 19)
    font_item = get_font("segoeui.ttf", 17)
    font_mono = get_font("arialbd.ttf", 16)
    font_small = get_font("segoeui.ttf", 14)

    # Top accent bar
    draw.rectangle([0, 0, card_w, 14], fill="#ea580c")
    draw.rounded_rectangle(
        [18, 18, card_w - 18, card_h - 18],
        radius=24,
        outline="#cbd5e1",
        width=3
    )

    # Badge
    badge_w = 260
    badge_x = (card_w - badge_w) // 2
    draw.rounded_rectangle(
        [badge_x, 42, badge_x + badge_w, 78],
        radius=18,
        fill="#ffedd5"
    )
    draw.text(
        (card_w // 2, 60),
        "AGNI-NODE ARCHIVE",
        fill="#c2410c",
        font=font_badge,
        anchor="mm"
    )

    # Titles
    draw.text(
        (card_w // 2, 114),
        "Autonomous Fire Suppression System",
        fill="#0f172a",
        font=font_title,
        anchor="mm"
    )
    draw.text(
        (card_w // 2, 154),
        "Official Documentation, Field Videos & Casualty Analysis Reports",
        fill="#475569",
        font=font_sub,
        anchor="mm"
    )

    # QR Container
    qr_box_size = 500
    qr_resized = qr_img.resize(
        (qr_box_size, qr_box_size),
        Image.Resampling.LANCZOS
    )
    qr_x = (card_w - qr_box_size) // 2
    qr_y = 195

    box_rect = [
        qr_x - 18,
        qr_y - 18,
        qr_x + qr_box_size + 18,
        qr_y + qr_box_size + 18
    ]
    draw.rounded_rectangle(
        box_rect,
        radius=24,
        fill="#ffffff",
        outline="#ea580c",
        width=4
    )
    card.paste(qr_resized, (qr_x, qr_y), qr_resized)

    # Action Pill
    pill_w = 460
    pill_x = (card_w - pill_w) // 2
    pill_y = qr_y + qr_box_size + 36
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_w, pill_y + 50],
        radius=25,
        fill="#ea580c"
    )
    draw.text(
        (card_w // 2, pill_y + 25),
        "SCAN WITH PHONE CAMERA TO OPEN",
        fill="#ffffff",
        font=font_pill,
        anchor="mm"
    )

    # Files List Container
    box_y = pill_y + 72
    box_h = 320
    draw.rounded_rectangle(
        [48, box_y, card_w - 48, box_y + box_h],
        radius=18,
        fill="#f8fafc",
        outline="#e2e8f0",
        width=2
    )

    draw.text(
        (74, box_y + 24),
        "FILES & MEDIA INCLUDED IN THIS SCANNER:",
        fill="#c2410c",
        font=font_sec
    )

    items = [
        ("►", " AgniNode Working Demo (Full HD 1080p - 01:00 min)"),
        ("►", " Aerosol Module Test (1080p High-Speed - 00:11 sec)"),
        ("📄", " NCRB Accidental Fire Deaths in India (2021-2025)"),
        ("📄", " NCRB Electrical Short Circuit Fires (2021-2025)"),
        ("📄", " Reducing Electrical Fire Deaths in India")
    ]

    curr_y = box_y + 64
    for icon, text in items:
        draw.text((74, curr_y), icon, fill="#ea580c", font=font_item)
        draw.text((104, curr_y), text, fill="#1e293b", font=font_item)
        curr_y += 48

    # Footer
    draw.text(
        (card_w // 2, card_h - 66),
        url,
        fill="#ea580c",
        font=font_mono,
        anchor="mm"
    )
    draw.text(
        (card_w // 2, card_h - 38),
        "Compatible with iPhone, Android, Google Lens & WhatsApp",
        fill="#64748b",
        font=font_small,
        anchor="mm"
    )

    card.save(filename, format="PNG")
    print(f"Generated Light Scan Card: {filename}")


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    public_url = "https://avishkarranjane.github.io/agninode-docs/"
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:8080/"

    print("=" * 60)
    print("Generating AgniNode Scanners and Cards...")
    print(f"Public Portal URL : {public_url}")
    print(f"Local Offline URL : {local_url}")
    print("=" * 60)

    os.makedirs("assets/qr", exist_ok=True)

    # 1. Clean Black & White QR (Highest scanability)
    generate_clean_qr(public_url, "assets/qr/AgniNode_QR_Clean.png")

    # 2. Branded QR Code
    pub_qr = generate_branded_qr(
        public_url,
        "assets/qr/AgniNode_QR_Public.png"
    )

    # 3. Dark Presentation Placard
    generate_presentation_card_dark(
        pub_qr,
        public_url,
        "assets/qr/AgniNode_Scan_Card.png"
    )

    # 4. Light Printable Placard
    generate_presentation_card_light(
        pub_qr,
        public_url,
        "assets/qr/AgniNode_Scan_Card_Light.png"
    )

    # 5. Local Offline Wi-Fi QR & Placard
    loc_qr = generate_branded_qr(
        local_url,
        "assets/qr/AgniNode_QR_Local_WiFi.png"
    )
    generate_presentation_card_dark(
        loc_qr,
        local_url,
        "assets/qr/AgniNode_Scan_Card_Local_WiFi.png"
    )

    # 6. Scalable Vector Graphic (SVG)
    svg_qr = qrcode.make(public_url, image_factory=SvgPathImage)
    with open("assets/qr/AgniNode_QR_Public.svg", "wb") as svg_file:
        svg_qr.save(svg_file)
    print("Generated SVG: assets/qr/AgniNode_QR_Public.svg")
    print("All scanners generated successfully!")
