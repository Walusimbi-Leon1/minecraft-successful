#!/usr/bin/env python3
"""Build updated index.html with full book content inline, support link, and other books section."""

import markdown
import re
import os
import json

BOOK_DIR = "/home/ec2-user/.openclaw/workspace/minecraft-book"

chapters = [
    ("chapter-1.md", "The First Dig", "Iron"),
    ("chapter-2.md", "Bone Rush", "Bones"),
    ("chapter-3.md", "Gold Heist", "Gold"),
    ("chapter-4.md", "Emerald Exchange", "Emeralds"),
    ("chapter-5.md", "Diamond Score", "Diamonds"),
    ("chapter-6.md", "The Enchantment", "Enchanting"),
    ("chapter-7.md", "Stronghold Run", "The End Portal"),
    ("chapter-8.md", "End Battle", "The Ender Dragon"),
    ("chapter-9.md", "Wither War", "The Wither"),
    ("chapter-10.md", "The Successful Life", "Finale"),
]

def read_chapter(filename):
    path = os.path.join(BOOK_DIR, filename)
    with open(path, 'r') as f:
        content = f.read()
    content = re.sub(r'^# .*?\n', '', content, count=1)
    return content

def md_to_html(md_text):
    extras = ['extra', 'sane_lists']
    html = markdown.markdown(md_text, extensions=extras)
    # Wrap blockquotes nicely
    return html

def build_chapter_html(i, title, mission, md_content):
    html_content = md_to_html(md_content)
    return f'''<div class="chapter-card">
    <button class="chapter-toggle" onclick="toggleChapter({i})">
        <span class="ch-num">{i}.</span>
        <span class="ch-title">{title}</span>
        <span class="ch-mission">{mission}</span>
        <span class="ch-arrow">▼</span>
    </button>
    <div class="chapter-body" id="chapter-{i}">
        {html_content}
    </div>
</div>'''

# Other books data
other_books = [
    ("salt-and-silk", "Salt & Silk", "A literary novel of desire spanning Marrakech, Istanbul, Kyoto, Havana, and Santorini.", "https://walusimbi-leon1.github.io/salt-and-silk/"),
    ("the-rhythm-of-your-heart", "The Rhythm of Your Heart", "A love novel about finding harmony in unexpected places.", "https://github.com/Walusimbi-Leon1/the-rhythm-of-your-heart"),
    ("whispers-of-destiny", "Whispers of Destiny", "A romantic tale of fate, choices, and the paths we take.", "https://github.com/Walusimbi-Leon1/whispers-of-destiny"),
    ("letters-i-never-sent", "Letters I Never Sent", "A novel built from unsent letters — raw, emotional, honest.", "https://github.com/Walusimbi-Leon1/letters-i-never-sent"),
    ("under-the-acacia-tree", "Under the Acacia Tree", "A love story rooted in African soil and timeless connection.", "https://github.com/Walusimbi-Leon1/under-the-acacia-tree"),
    ("atlas-of-feeling", "Atlas of Feeling", "A complete guide to every human emotion — 33 chapters.", "https://github.com/Walusimbi-Leon1/atlas-of-feeling"),
    ("the-architecture-of-thought", "The Architecture of Thought", "A philosophical inquiry into how we think and why.", "https://github.com/Walusimbi-Leon1/the-architecture-of-thought"),
    ("beyond-the-horizon", "Beyond the Horizon", "A love novel about what waits beyond what we can see.", "https://github.com/Walusimbi-Leon1/beyond-the-horizon"),
    ("dialogues-with-my-love", "Dialogues With My Love", "Based on a true story — intimate conversations between Leon and Nazurah.", "https://github.com/Walusimbi-Leon1/dialogues-with-my-love"),
    ("mrbeast", "MrBeast", "The unauthorized biography of Jimmy Donaldson — SGSS Books.", "https://walusimbileon1.github.io/mrbeast/"),
    ("ishowspeed", "IShowSpeed", "The complete biography of Darren Watkins Jr. — SGSS Books.", "https://github.com/Walusimbi-Leon1/ishowspeed"),
    ("prison-break", "Prison Break", "A comprehensive book on the Prison Break TV series.", "https://github.com/Walusimbi-Leon1/prison-break"),
]

# Build chapter HTML
all_chapters_html = []
for i, (filename, title, mission) in enumerate(chapters, 1):
    md = read_chapter(filename)
    all_chapters_html.append(build_chapter_html(i, title, mission, md))

chapters_joined = "\n".join(all_chapters_html)

# Other books HTML
other_books_html = ""
for repo, name, desc, url in other_books:
    other_books_html += f'''<a href="{url}" class="book-card" target="_blank" rel="noopener">
    <div class="book-card-inner">
        <h3>{name}</h3>
        <p>{desc}</p>
    </div>
</a>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minecraft Successful — The Block Crew Chronicles</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #1a1a2e;
            color: #e0e0e0;
            line-height: 1.6;
            min-height: 100vh;
        }}
        .hero {{
            background: linear-gradient(135deg, #16213e 0%, #0f3460 50%, #1a1a2e 100%);
            padding: 4rem 2rem;
            text-align: center;
            border-bottom: 3px solid #3c7a3c;
        }}
        .hero h1 {{
            font-size: 3rem;
            color: #5cb85c;
            letter-spacing: 3px;
            margin-bottom: 0.5rem;
        }}
        .hero .subtitle {{
            font-size: 1.2rem;
            color: #aaa;
            font-style: italic;
        }}
        .hero .tagline {{
            margin-top: 1rem;
            color: #888;
            font-size: 0.9rem;
        }}
        .container {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        .box {{
            background: #16213e;
            border: 1px solid #3c7a3c;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}
        .box h2 {{
            color: #5cb85c;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        .box p {{ color: #bbb; }}
        .box p + p {{ margin-top: 0.5rem; }}
        .downloads {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }}
        .btn {{
            display: inline-block;
            padding: 0.8rem 1.5rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.2s;
            font-size: 1rem;
        }}
        .btn-primary {{
            background: #3c7a3c;
            color: white;
        }}
        .btn-primary:hover {{
            background: #4a9a4a;
            transform: translateY(-2px);
        }}
        .btn-secondary {{
            background: #0f3460;
            color: #aaa;
            border: 1px solid #3c7a3c;
        }}
        .btn-secondary:hover {{
            background: #1a4a80;
            transform: translateY(-2px);
        }}
        /* ---- Chapter Toggle Cards ---- */
        .chapter-card {{
            border: 1px solid #2a3a5a;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            overflow: hidden;
        }}
        .chapter-toggle {{
            width: 100%;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.8rem 1rem;
            background: #1e2a45;
            border: none;
            color: #ccc;
            font-family: inherit;
            font-size: 1rem;
            cursor: pointer;
            text-align: left;
            transition: background 0.15s;
        }}
        .chapter-toggle:hover {{
            background: #253252;
        }}
        .ch-num {{
            font-weight: bold;
            color: #5cb85c;
            min-width: 1.8rem;
        }}
        .ch-title {{
            flex: 1;
        }}
        .ch-mission {{
            color: #888;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }}
        .ch-arrow {{
            color: #5cb85c;
            font-size: 0.75rem;
            transition: transform 0.25s;
        }}
        .chapter-body {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease;
            background: #12182b;
            border-top: 0 solid #2a3a5a;
        }}
        .chapter-body.open {{
            max-height: 50000px;
            border-top-width: 1px;
        }}
        .chapter-body.open + .chapter-toggle .ch-arrow,
        .chapter-toggle.open .ch-arrow {{
            transform: rotate(180deg);
        }}
        .chapter-body p {{
            margin: 0.6rem 0;
            text-indent: 1.2em;
            color: #ccc;
        }}
        .chapter-body p:first-of-type {{ text-indent: 0; }}
        .chapter-body h1 {{
            font-size: 1.6rem;
            color: #5cb85c;
            margin: 1.2rem 0 0.4rem;
        }}
        .chapter-body h2 {{
            font-size: 1.2rem;
            color: #8bc34a;
            margin: 1rem 0 0.3rem;
            border-bottom: 1px solid #2a3a5a;
            padding-bottom: 0.2rem;
        }}
        .chapter-body h3 {{ font-size: 1.1rem; color: #aaa; margin: 0.8rem 0 0.2rem; }}
        .chapter-body blockquote {{
            border-left: 3px solid #5cb85c;
            margin: 0.5rem 0;
            padding: 0.3rem 0 0.3rem 0.8rem;
            background: #0d1525;
            color: #aaa;
            font-style: italic;
        }}
        .chapter-body blockquote p {{ text-indent: 0; }}
        .chapter-body hr {{ border: none; border-top: 1px solid #2a3a5a; margin: 1rem 0; }}
        .chapter-body strong {{ color: #ddd; }}
        .chapter-body code {{
            background: #0d1525;
            padding: 1px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }}
        .chapter-body ul, .chapter-body ol {{ margin: 0.5rem 0; padding-left: 1.5rem; color: #ccc; }}
        .chapter-body li {{ margin: 0.2rem 0; }}

        /* ---- Characters ---- */
        .characters {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        .character-card {{
            background: #1e2a45;
            border-radius: 8px;
            padding: 1rem;
            border-left: 3px solid #5cb85c;
        }}
        .character-card h3 {{ color: #5cb85c; font-size: 1rem; }}
        .character-card p {{ color: #999; font-size: 0.85rem; margin-top: 0.3rem; }}

        /* ---- Other Books ---- */
        .books-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        .book-card {{
            text-decoration: none;
            display: block;
        }}
        .book-card-inner {{
            background: #1e2a45;
            border-radius: 8px;
            padding: 1rem;
            border-top: 3px solid #3c7a3c;
            transition: all 0.2s;
            height: 100%;
        }}
        .book-card:hover .book-card-inner {{
            background: #253252;
            transform: translateY(-2px);
            border-top-color: #5cb85c;
        }}
        .book-card-inner h3 {{
            color: #5cb85c;
            font-size: 0.95rem;
            margin-bottom: 0.3rem;
        }}
        .book-card-inner p {{
            color: #999;
            font-size: 0.8rem;
            line-height: 1.4;
        }}

        /* ---- Support Banner ---- */
        .support-banner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            background: linear-gradient(135deg, #1a2a1a, #16213e);
            border: 1px solid #3c7a3c;
            border-radius: 8px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 2rem;
        }}
        .support-banner p {{
            color: #bbb;
            flex: 1;
            font-size: 0.95rem;
        }}
        .support-banner .btn {{
            flex-shrink: 0;
        }}

        .footer {{
            text-align: center;
            padding: 2rem;
            color: #555;
            font-size: 0.8rem;
            border-top: 1px solid #2a2a4a;
            margin-top: 2rem;
        }}

        @media (max-width: 600px) {{
            .hero h1 {{ font-size: 2rem; }}
            .hero {{ padding: 2rem 1rem; }}
            .container {{ padding: 0 1rem; }}
            .chapter-toggle {{ flex-wrap: wrap; }}
            .ch-mission {{ margin-left: 2.3rem; width: 100%; }}
            .books-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
<div class="hero">
    <h1>⛏️ Minecraft Successful</h1>
    <p class="subtitle">A Story-Driven Mission Book</p>
    <p class="tagline">Five players. Ten missions. One blocky world.</p>
</div>

<div class="container">
    <div class="box">
        <h2>📖 About the Book</h2>
        <p>Follow <strong>The Block Crew</strong> — Stone, Red, Brick, Pick, and Gear — through 10 chapters of GTA-style missions. From their first iron dig to conquering the Ender Dragon and the Wither, every chapter blends an immersive story with real Minecraft strategies.</p>
        <p style="color:#888;">~21,000 words · 10 chapters · Minecraft version-agnostic</p>
        <div class="downloads">
            <a href="https://github.com/Walusimbi-Leon1/minecraft-successful/releases/download/v1.0/Minecraft_Successful.pdf" class="btn btn-primary">📕 Download PDF</a>
            <a href="https://github.com/Walusimbi-Leon1/minecraft-successful" class="btn btn-secondary">💻 View on GitHub</a>
        </div>
    </div>

    <!-- SUPPORT BANNER -->
    <div class="support-banner">
        <p>❤️ Enjoying the book? If you'd like to support our work and help us create more stories like this one, consider making a contribution. Every bit fuels the next chapter!</p>
        <a href="https://walusimbi-leon1.github.io/voice-support/" class="btn btn-primary" target="_blank" rel="noopener">💚 Support SGSS</a>
    </div>

    <div class="box">
        <h2>🧱 The Block Crew</h2>
        <div class="characters">
            <div class="character-card"><h3>Stone</h3><p>Veteran miner. Practical, experienced, stubborn. The muscle.</p></div>
            <div class="character-card"><h3>Red</h3><p>Crew leader. Ambitious, fast-talking, always scheming.</p></div>
            <div class="character-card"><h3>Brick</h3><p>Enforcer. Hot-headed, loyal, always ready to fight.</p></div>
            <div class="character-card"><h3>Pick</h3><p>Strategist. Cautious, smart, always has a plan.</p></div>
            <div class="character-card"><h3>Gear</h3><p>Tech expert. Builder, inventor, redstone genius.</p></div>
        </div>
    </div>

    <div class="box">
        <h2>📚 Read Online</h2>
        <p style="margin-bottom:1rem;">Click any chapter to expand and read the full story right here in your browser.</p>
        {chapters_joined}
    </div>

    <div class="box">
        <h2>📖 More Books</h2>
        <p style="margin-bottom:1rem;">Discover other books from the SGSS Literary Collection:</p>
        <div class="books-grid">
            {other_books_html}
        </div>
    </div>
</div>

<div class="footer">
    <p>Minecraft Successful &copy; 2026 · SGSS Literary Collection</p>
    <p style="margin-top: 0.3rem;">Minecraft is a trademark of Mojang AB. This is an unofficial fan work.</p>
</div>

<script>
function toggleChapter(id) {{
    var body = document.getElementById('chapter-' + id);
    var btn = body.parentElement.querySelector('.chapter-toggle');
    if (body.classList.contains('open')) {{
        body.classList.remove('open');
        btn.classList.remove('open');
    }} else {{
        body.classList.add('open');
        btn.classList.add('open');
    }}
}}
</script>
</body>
</html>'''

with open(os.path.join(BOOK_DIR, 'index.html'), 'w') as f:
    f.write(html)

size = len(html.encode('utf-8'))
print(f"index.html written ({size:,} bytes)")

# Count total words in the HTML chunk for the book content
word_count = len(re.findall(r'\\w+', html))
print(f"Done!")
