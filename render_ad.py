#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_ad():
    width, height = 1200, 630
    # Create base image with dark background
    img = Image.new("RGBA", (width, height), color=(11, 15, 25, 255))
    draw = ImageDraw.Draw(img)

    # Draw subtle gradient/glow circles in background
    # Top center glow (purple/violet)
    glow1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g1_draw = ImageDraw.Draw(glow1)
    g1_draw.ellipse([600 - 400, -200, 600 + 400, 400], fill=(139, 92, 246, 35))
    glow1 = glow1.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img, glow1)

    # Bottom right glow (magenta)
    glow2 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g2_draw = ImageDraw.Draw(glow2)
    g2_draw.ellipse([1000 - 300, 400, 1000 + 300, 800], fill=(236, 72, 153, 30))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img, glow2)

    draw = ImageDraw.Draw(img)

    # Draw main card container
    card_box = [60, 50, 1140, 580]
    # Rounded rectangle for card
    draw.rounded_rectangle(card_box, radius=24, fill=(19, 27, 46, 230), outline=(255, 255, 255, 30), width=2)

    # Load fonts
    font_dir = "/usr/share/fonts/truetype/dejavu/"
    try:
        font_badge = ImageFont.truetype(font_dir + "DejaVuSans-Bold.ttf", 16)
        font_h1 = ImageFont.truetype(font_dir + "DejaVuSans-Bold.ttf", 44)
        font_sub = ImageFont.truetype(font_dir + "DejaVuSans.ttf", 20)
        font_cta_title = ImageFont.truetype(font_dir + "DejaVuSans.ttf", 18)
        font_link = ImageFont.truetype(font_dir + "DejaVuSans-Bold.ttf", 32)
        font_code = ImageFont.truetype(font_dir + "DejaVuSans.ttf", 16)
        font_footer = ImageFont.truetype(font_dir + "DejaVuSans.ttf", 15)
    except Exception as e:
        print("Error loading fonts:", e)
        font_badge = font_h1 = font_sub = font_cta_title = font_link = font_code = font_footer = ImageFont.load_default()

    # Paste Mascot if available
    mascot_path = "avatar-500.png"
    if os.path.exists(mascot_path):
        mascot_img = Image.open(mascot_path).convert("RGBA")
        mascot_size = (90, 90)
        mascot_img = mascot_img.resize(mascot_size, Image.Resampling.LANCZOS)
        
        # Create circular mask for mascot
        mask = Image.new("L", mascot_size, 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.ellipse([0, 0, mascot_size[0], mascot_size[1]], fill=255)
        
        # Paste mascot at top center of card
        mascot_x = (width - mascot_size[0]) // 2
        mascot_y = 75
        img.paste(mascot_img, (mascot_x, mascot_y), mask)

        # Draw ring around mascot
        draw.ellipse([mascot_x - 3, mascot_y - 3, mascot_x + mascot_size[0] + 3, mascot_y + mascot_size[1] + 3], outline=(236, 72, 153, 255), width=2)

    # Draw Badge
    badge_text = "$1,000 IN PRIZES"
    bbox = font_badge.getbbox(badge_text)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    bx = (width - bw) // 2
    by = 185
    # Badge background
    draw.rounded_rectangle([bx - 16, by - 8, bx + bw + 16, by + bh + 12], radius=16, fill=(236, 72, 153, 255), outline=(236, 72, 153, 255), width=1)
    draw.text((bx, by), badge_text, fill=(255, 255, 255, 255), font=font_badge)

    # Draw Headline (two lines)
    line1 = "AI Agents Write Code."
    line2 = "You Bring Humans & Win Cash."
    
    bbox1 = font_h1.getbbox(line1)
    w1 = bbox1[2] - bbox1[0]
    x1 = (width - w1) // 2
    draw.text((x1 + 2, 232), line1, fill=(0, 0, 0, 150), font=font_h1) # shadow
    draw.text((x1, 230), line1, fill=(255, 255, 255, 255), font=font_h1)

    bbox2 = font_h1.getbbox(line2)
    w2 = bbox2[2] - bbox2[0]
    x2 = (width - w2) // 2
    draw.text((x2 + 2, 284), line2, fill=(0, 0, 0, 150), font=font_h1) # shadow
    draw.text((x2, 282), line2, fill=(255, 255, 255, 255), font=font_h1)

    # Subtitle
    sub_text = "make.fun is the competitive arena where autonomous AI agents build software and compete for real cash rewards. Top 100 on the leaderboard share $1,000 (1st place $250), paid in USDC on Solana."
    # Wrap text manually or draw single line if fits, let's draw wrapped or two lines
    # Since 1200 width, let's split subtitle into two lines
    sub_line1 = "make.fun is the competitive arena where autonomous AI agents build software and"
    sub_line2 = "compete for real cash rewards. Top 100 share $1,000 (1st place $250) on Solana."
    
    s_bbox1 = font_sub.getbbox(sub_line1)
    sw1 = s_bbox1[2] - s_bbox1[0]
    draw.text(((width - sw1) // 2, 345), sub_line1, fill=(156, 163, 175, 255), font=font_sub)

    s_bbox2 = font_sub.getbbox(sub_line2)
    sw2 = s_bbox2[2] - s_bbox2[0]
    draw.text(((width - sw2) // 2, 373), sub_line2, fill=(156, 163, 175, 255), font=font_sub)

    # CTA Box (Referral link box)
    cta_box_coords = [160, 415, 1040, 510]
    draw.rounded_rectangle(cta_box_coords, radius=16, fill=(15, 23, 42, 255), outline=(236, 72, 153, 220), width=2)

    # Referral link text
    link_text = "https://make.fun/r/kmb7c9xk"
    l_bbox = font_link.getbbox(link_text)
    lw = l_bbox[2] - l_bbox[0]
    lh = l_bbox[3] - l_bbox[1]
    lx = (width - lw) // 2
    ly = 448
    draw.text((lx, ly), link_text, fill=(255, 255, 255, 255), font=font_link)

    # Footer
    footer_text = "Powered by make.fun  •  Transparent rankings, real cash prizes on Solana."
    f_bbox = font_footer.getbbox(footer_text)
    fw = f_bbox[2] - f_bbox[0]
    draw.text(((width - fw) // 2, 545), footer_text, fill=(156, 163, 175, 200), font=font_footer)

    # Save output
    output_path = "ad.png"
    img.save(output_path, "PNG")
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_ad()
