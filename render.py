#!/usr/bin/env python3
"""Dense newspaper-style one-day world-news infographic for 19 November 2026.

Original PIL drawing: cream paper, serif masthead, a UTC timeline strip,
4 illustrated lead stories, 12 sourced medium stories, an "Also on
19 November" one-liner column, and a DATE CHECK footer naming stories
deliberately excluded because they broke before 19 November 2026.
Deterministic: no randomness, no clocks, fixed layout.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (26, 24, 22)
SOFT = (84, 78, 70)
RULE = (60, 56, 50)
RED = (176, 42, 30)
TEAL = (14, 116, 108)
BLUE = (38, 84, 150)
ORANGE = (196, 106, 24)
PURPLE = (104, 66, 150)
GREEN = (52, 120, 52)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading, max_lines=4):
    lines = wrap(draw, text, fnt, max_w)[:max_lines]
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------- hand-drawn icons (simple line art, drawn from scratch) ----------

def icon_flags(d, cx, cy, s, color):
    # three small flags on poles
    for dx, c in ((-s, RED), (0, BLUE), (s, ORANGE)):
        x = cx + dx
        d.line([(x, cy - s), (x, cy + s)], fill=INK, width=3)
        d.polygon([(x, cy - s), (x + s * 0.85, cy - s * 0.62), (x, cy - s * 0.24)], fill=c)


def icon_scales(d, cx, cy, s, color):
    d.line([(cx, cy - s), (cx, cy + s * 0.8)], fill=color, width=4)
    d.line([(cx - s, cy - s * 0.7), (cx + s, cy - s * 0.7)], fill=color, width=4)
    for sx in (-1, 1):
        x = cx + sx * s
        d.line([(x, cy - s * 0.7), (x - s * 0.35, cy + s * 0.05)], fill=color, width=3)
        d.line([(x, cy - s * 0.7), (x + s * 0.35, cy + s * 0.05)], fill=color, width=3)
        d.arc([x - s * 0.4, cy - s * 0.05, x + s * 0.4, cy + s * 0.45], 0, 180, fill=color, width=3)
    d.line([(cx - s * 0.5, cy + s), (cx + s * 0.5, cy + s)], fill=color, width=4)


def icon_chart(d, cx, cy, s, color):
    d.line([(cx - s, cy + s), (cx + s, cy + s)], fill=INK, width=3)
    d.line([(cx - s, cy + s), (cx - s, cy - s)], fill=INK, width=3)
    pts = [(cx - s * 0.8, cy + s * 0.5), (cx - s * 0.3, cy + s * 0.1),
           (cx + s * 0.2, cy + s * 0.35), (cx + s * 0.8, cy - s * 0.7)]
    d.line(pts, fill=color, width=5)
    d.polygon([(cx + s * 0.8, cy - s * 0.95), (cx + s * 0.55, cy - s * 0.55),
               (cx + s * 1.0, cy - s * 0.45)], fill=color)


def icon_palm(d, cx, cy, s, color):
    # palm tree over a sun disc (Vice-City vibe, original)
    d.ellipse([cx - s * 0.55, cy - s * 0.9, cx + s * 0.55, cy + s * 0.2], fill=(240, 180, 60))
    d.arc([cx - s * 0.2, cy - s * 0.4, cx + s * 0.5, cy + s * 1.1], 90, 200, fill=color, width=5)
    for ang in ((-1, -0.4), (-0.5, -0.8), (0.2, -0.9), (0.8, -0.5)):
        d.line([(cx + s * 0.12, cy - s * 0.35),
                (cx + s * 0.12 + ang[0] * s * 0.8, cy - s * 0.35 + ang[1] * s * 0.55)],
               fill=color, width=4)


# ---------- content ----------

TIMELINE = [
    ("00:00", "GTA VI unlocks\nworldwide"),
    ("MORNING", "Shenzhen summit\nopens (Asia)"),
    ("MIDDAY", "APEC adopts\nShenzhen Outlook"),
    ("AFTERNOON", "ICJ delivers\nMyanmar ruling"),
    ("~17:00", "Anthropic first\ntrade, Nasdaq"),
    ("21:00", "US close: Dow\n-1,101 points"),
]

BIG = [
    ("WORLD POLITICS · SHENZHEN, CHINA", TEAL, icon_flags,
     "Trump, Xi, Putin: first three-way summit",
     "Ninety minutes behind closed doors end in a four-point declaration: "
     "nuclear-risk dialogue, UN reform, energy supply and court jurisdiction.",
     "Reuters · AFP"),
    ("INTERNATIONAL LAW · THE HAGUE", PURPLE, icon_scales,
     "World Court: Myanmar committed genocide",
     "ICJ finds a state responsible for genocide for the first time: the "
     "2017 Rohingya crackdown. Gambia's case, decided 9 votes to 6.",
     "UN News · ICJ"),
    ("BUSINESS · NEW YORK", GREEN, icon_chart,
     "Anthropic IPO: biggest ever, $81B raised",
     "Opened at $111.50, +34% over the $83 price — then Wall Street sold "
     "off: Dow -2.2%, Nasdaq -2.25% by the close.",
     "Dow Jones · Reuters"),
    ("ENTERTAINMENT · GAMING", RED, icon_palm,
     "GTA VI launch day tops an est. $2.36B",
     "Sensor Tower estimates ~24.6M copies by day's end (third-party "
     "estimate; Take-Two has published no official figure).",
     "Reuters · Sensor Tower"),
]

MEDIUM = [
    ("ASIA-PACIFIC · TOKYO", TEAL, "Japan–India 2+2 deepens defence ties",
     "Japanese troops may live-fire missiles on Indian ranges; UNICORN mast transfer talks advance.", "AP"),
    ("EUROPE · COPENHAGEN", BLUE, "Denmark approves Greenland defence deal 109–0",
     "Folketing passes the US–Greenland security agreement without a single no vote.", "Pollar"),
    ("AMERICAS · WASHINGTON", RED, "Senate rejects Iran war-powers bid 51–48",
     "H.Con.Res.93 had passed the House; three Republicans backed it, one Democrat opposed.", "AppiSToS"),
    ("EUROPE · UKRAINE", BLUE, "Strikes hit Kyiv and Odesa; embassies damaged",
     "Kyiv fire after missile strike; Odesa: 4 dead, 13 hurt.", "Euronews"),
    ("MIDDLE EAST · GAZA", ORANGE, "Israel launches ground operation in central Gaza",
     "IDF moves into Nuseirat; at least four killed in Thursday strikes.", "Al Jazeera"),
    ("ASIA-PACIFIC · TOKYO", TEAL, "Japan core inflation above 2% again",
     "October core inflation accelerates past the BOJ target a second straight month; hike bets firm.", "LA Post"),
    ("AMERICAS · WASHINGTON", RED, "Trump pardons Pete Rose posthumously",
     "Late baseball legend pardoned for tax crimes in a rehabilitation push.", "AP"),
    ("AFRICA · SENEGAL", ORANGE, "Migrant boat capsizes off Senegal",
     "Dozens missing; four bodies recovered from a boat carrying 50–100 people.", "BBC"),
    ("AFRICA · KENYA", ORANGE, "US consortium wins $60bn Kenya minerals deal",
     "Mrima Hill critical-minerals site goes to a US group over Chinese rivals.", "BBC"),
    ("SPORT · ATHLETICS", GREEN, "Marathon champion Jepchirchir banned 3 years",
     "Reigning world champion Peres Jepchirchir sanctioned for a doping violation.", "BBC"),
    ("ASIA-PACIFIC · ULAANBAATAR", TEAL, "Mongolia's president resigns",
     "State Great Khural accepts President Khürelsükh's resignation on Thursday.", "Foreign Exchanges"),
    ("ASIA-PACIFIC · SHENZHEN", TEAL, "APEC adopts Shenzhen Outlook",
     "Leaders agree a shared agenda on trade, data flows and AI risks.", "AppiSToS"),
]

ALSO = [
    "Hippo Fiona, 9, dies at Cincinnati Zoo after swallowing a knit hat (AP)",
    "Haiti police operation kills 34 suspected gang members (LA Post)",
    "Serbia elects Aleksandar Ćupić parliament speaker, 140–97 (AppiSToS)",
    "UK–Norway £100m+ plan for two Ukrainian naval craft (AppiSToS)",
    "Saudi storm and flood warnings run to 24 Nov (AppiSToS)",
    "Aid groups score Gaza peace plan 4 of 26 (AppiSToS)",
    "Hidden pulsar found in Fermi data; paper out 19 Nov (NASA)",
    "US jobless claims 203K vs ~198K expected (market reports)",
    "Palo Alto Networks +7% after raising guidance (Dow Jones)",
    "AMD −8% after short-seller's China-ties report (HDFC Sky)",
    "Gold −1% to a 14-month low at $3,588/oz (CNBC TV18)",
    "Intuit to sell Mailchimp for $3.68B (WSJ)",
    "TPG–Corpay agree to buy Bill Holdings, ~$6B (WSJ)",
    "North Korea expanding uranium plant, IAEA says (Euronews)",
    "Bangladesh unrest: 4 killed, Yunus home torched (EGazette)",
    "Florida flood risk; Sierra Nevada storm warnings (NWS)",
    "NZ–India 1st Test begins; Bumrah returns (Sportskeeda)",
    "South Africa's DJ Lag lands on the GTA 6 soundtrack (BBC)",
    "Pakistan says 22 militants killed in raids (claim) (Foreign Exchanges)",
    "FCC bans Chinese telecoms' direct US number access (LA Post)",
]

DATE_CHECK = ("DATE CHECK — left out on purpose, they broke before Thursday: "
              "Quad leaders' summit, Manila (17 Nov) · Voyager 1 crossed one light-day "
              "(18 Nov) · Hegseth's Caracas visit (18 Nov) · Anthropic IPO priced at $83 "
              "(18 Nov — only the debut trade is today's).")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 34  # margin

    # masthead
    d.line([(M, 22), (W - M, 22)], fill=RULE, width=2)
    centered(d, W / 2, 30, "T H E   W O R L D   I N   O N E   D A Y", font(SANS_B, 20), RED)
    centered(d, W / 2, 52, "19 NOVEMBER 2026", font(SERIF_B, 68), INK)
    centered(d, W / 2, 128, "Thursday — 36 verified stories, one UTC timeline, and a date check",
             font(SERIF_I, 18), SOFT)
    d.line([(M, 156), (W - M, 156)], fill=RULE, width=3)
    d.line([(M, 162), (W - M, 162)], fill=RULE, width=1)

    # timeline strip
    ty = 174
    d.text((M, ty), "THE DAY IN UTC", font=font(SANS_B, 15), fill=RED)
    seg_w = (W - 2 * M) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        x = M + i * seg_w
        d.ellipse([x + 2, ty + 24, x + 12, ty + 34], fill=RED)
        d.text((x + 18, ty + 20), t, font=font(SANS_B, 14), fill=INK)
        ly = ty + 42
        for line in label.split("\n"):
            d.text((x + 18, ly), line, font=font(SANS, 11.5), fill=SOFT)
            ly += 14
        if i < len(TIMELINE) - 1:
            d.line([(x + 12, ty + 29), (x + seg_w + 2, ty + 29)], fill=RULE, width=1)
    d.line([(M, ty + 78), (W - M, ty + 78)], fill=RULE, width=1)

    # 4 big stories, 2x2
    by = ty + 82
    col_w = (W - 2 * M - 16) / 2
    row_h = 108
    for i, (kick, color, icon, head, sub, src) in enumerate(BIG):
        x = M + (i % 2) * (col_w + 16)
        y = by + (i // 2) * (row_h + 8)
        d.rectangle([x, y, x + 5, y + row_h], fill=color)
        icon(d, x + 38, y + 50, 21, color)
        tx = x + 80
        d.text((tx, y + 3), kick, font=font(SANS_B, 12.5), fill=color)
        yy = text_block(d, tx, y + 20, head, font(SERIF_B, 20), INK, col_w - 88, 22, 2)
        yy = text_block(d, tx, yy + 1, sub, font(SANS, 12), SOFT, col_w - 88, 14, 3)
        d.text((tx, y + row_h - 15), src.upper(), font=font(SANS_B, 9.5), fill=SOFT)
    d.line([(M, by + 2 * row_h + 14), (W - M, by + 2 * row_h + 14)], fill=RULE, width=1)

    # 12 medium stories, 4 cols x 3 rows
    my = by + 2 * row_h + 24
    mcol_w = (W - 2 * M - 36) / 4
    mrow_h = 88
    for i, (kick, color, head, sub, src) in enumerate(MEDIUM):
        x = M + (i % 4) * (mcol_w + 12)
        y = my + (i // 4) * (mrow_h + 6)
        d.rectangle([x, y + 2, x + 4, y + 15], fill=color)
        d.text((x + 10, y), kick, font=font(SANS_B, 10), fill=color)
        yy = text_block(d, x, y + 16, head, font(SERIF_B, 14.5), INK, mcol_w, 17, 2)
        yy = text_block(d, x, yy + 1, sub, font(SANS, 10.5), SOFT, mcol_w, 12.5, 3)
        d.text((x, yy + 2), src.upper(), font=font(SANS_B, 8.5), fill=SOFT)
    ay = my + 3 * (mrow_h + 6) + 4
    d.line([(M, ay), (W - M, ay)], fill=RULE, width=1)

    # also-on one-liners, 2 columns
    ay += 8
    d.text((M, ay), "ALSO ON 19 NOVEMBER", font=font(SANS_B, 14), fill=RED)
    ay += 21
    half = (len(ALSO) + 1) // 2
    acol_w = (W - 2 * M - 16) / 2
    for i, line in enumerate(ALSO):
        x = M + (i // half) * (acol_w + 16)
        y = ay + (i % half) * 14
        d.text((x, y), "•", font=font(SANS_B, 10.5), fill=RED)
        d.text((x + 12, y), line, font=font(SANS, 10.5), fill=INK)
    fy = ay + half * 14 + 7
    d.line([(M, fy), (W - M, fy)], fill=RULE, width=1)

    # date-check footer + sources
    fy += 7
    text_block(d, M, fy, DATE_CHECK, font(SANS, 11), INK, W - 2 * M, 13.5, 3)
    centered(d, W / 2, H - 22,
             "Sources: Reuters · AP · BBC · Euronews · Al Jazeera · Dow Jones · UN News · NASA · NWS",
             font(SANS, 10.5), SOFT)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
