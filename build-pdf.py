#!/usr/bin/env python3
"""Build a beautiful PDF of Minecraft Successful with table of contents."""

import markdown
import re
import os
from weasyprint import HTML, CSS

BOOK_DIR = "/home/ec2-user/.openclaw/workspace/minecraft-book"

# Chapter titles
chapters = [
    ("chapter-1.md", "The First Dig"),
    ("chapter-2.md", "Bone Rush"),
    ("chapter-3.md", "Gold Heist"),
    ("chapter-4.md", "Emerald Exchange"),
    ("chapter-5.md", "Diamond Score"),
    ("chapter-6.md", "The Enchantment"),
    ("chapter-7.md", "Stronghold Run"),
    ("chapter-8.md", "End Battle"),
    ("chapter-9.md", "Wither War"),
    ("chapter-10.md", "The Successful Life"),
]

def read_chapter(filename):
    path = os.path.join(BOOK_DIR, filename)
    with open(path, 'r') as f:
        content = f.read()
    # Remove the first # heading if it's the title (we handle it)
    return content

def build_html():
    html_parts = []
    
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Minecraft Successful</title>
<style>
@page {
    size: A5;
    margin: 1.5cm 1.2cm;
    @bottom-center {
        content: counter(page);
        font-family: 'Georgia', serif;
        font-size: 9pt;
        color: #888;
    }
}
@page :first {
    @bottom-center { content: none; }
}
body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #2d2d2d;
    text-align: justify;
    hyphens: auto;
}
/* Title Page */
.title-page {
    page-break-after: always;
    text-align: center;
    padding-top: 30%;
}
.title-page h1 {
    font-size: 28pt;
    color: #3c7a3c;
    margin-bottom: 0.3cm;
    letter-spacing: 2px;
}
.title-page .subtitle {
    font-size: 14pt;
    color: #666;
    font-style: italic;
    margin-bottom: 2cm;
}
.title-page .tagline {
    font-size: 11pt;
    color: #999;
    margin-top: 3cm;
    font-style: italic;
}
.title-page .author {
    font-size: 10pt;
    color: #888;
    margin-top: 0.5cm;
}
.title-page .divider {
    border: none;
    border-top: 2px solid #3c7a3c;
    width: 40%;
    margin: 1cm auto;
}
/* TOC Page */
.toc-page {
    page-break-after: always;
}
.toc-page h2 {
    font-size: 18pt;
    color: #3c7a3c;
    text-align: center;
    margin-bottom: 0.8cm;
    letter-spacing: 1px;
}
.toc-page .toc-item {
    display: flex;
    padding: 4pt 0;
    border-bottom: 1px dotted #ccc;
    font-size: 11pt;
}
.toc-page .toc-item .toc-num {
    font-weight: bold;
    color: #3c7a3c;
    min-width: 1.2cm;
}
.toc-page .toc-item .toc-title {
    flex: 1;
}
.toc-page .toc-item .toc-page-num {
    color: #888;
    min-width: 1cm;
    text-align: right;
}
.toc-characters {
    margin-top: 0.8cm;
    padding: 0.3cm 0.5cm;
    background: #f5f5f0;
    border-left: 4px solid #3c7a3c;
}
.toc-characters h3 {
    font-size: 12pt;
    color: #3c7a3c;
    margin-bottom: 3pt;
}
.toc-characters p {
    font-size: 10pt;
    color: #555;
    line-height: 1.4;
    margin: 2pt 0;
}
/* Chapter styles */
.chapter {
    page-break-before: always;
}
.chapter h1 {
    font-size: 20pt;
    color: #3c7a3c;
    text-align: center;
    margin-top: 2cm;
    margin-bottom: 0.2cm;
    page-break-before: always;
}
.chapter h1:first-of-type {
    margin-top: 3cm;
}
.chapter h2 {
    font-size: 14pt;
    color: #555;
    margin-top: 0.5cm;
    margin-bottom: 0.2cm;
    border-bottom: 1px solid #ddd;
    padding-bottom: 2pt;
}
.chapter h3 {
    font-size: 12pt;
    color: #666;
    margin-top: 0.3cm;
}
.chapter p {
    text-indent: 1.5em;
    margin: 4pt 0;
}
.chapter p:first-of-type {
    text-indent: 0;
}
.chapter blockquote {
    border-left: 3px solid #3c7a3c;
    margin: 0.3cm 0;
    padding: 4pt 0 4pt 0.4cm;
    background: #f9f9f4;
    font-style: italic;
    color: #555;
}
.chapter blockquote p {
    text-indent: 0;
}
.chapter hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 0.5cm 0;
}
.chapter strong {
    color: #333;
}
.chapter em {
    color: #666;
}
.chapter code {
    background: #f0f0e8;
    padding: 1pt 4pt;
    border-radius: 2pt;
    font-family: 'Courier New', monospace;
    font-size: 9.5pt;
}
/* Mission header blocks */
.chapter .mission-box {
    background: #f0f7f0;
    border: 1px solid #3c7a3c;
    border-radius: 4pt;
    padding: 0.3cm 0.5cm;
    margin: 0.3cm 0;
}
.chapter .mission-box p {
    text-indent: 0;
    margin: 2pt 0;
    font-size: 10.5pt;
}
/* Chapter intro dropcap-like treatment */
.chapter p:first-of-type::first-letter {
    font-size: 24pt;
    font-weight: bold;
    color: #3c7a3c;
    float: left;
    line-height: 1;
    margin-right: 4pt;
    font-family: 'Georgia', serif;
}
/* Final page */
.final-page {
    page-break-before: always;
    text-align: center;
    padding-top: 40%;
}
.final-page h2 {
    font-size: 18pt;
    color: #3c7a3c;
    margin-bottom: 0.5cm;
}
.final-page p {
    font-size: 11pt;
    color: #666;
    font-style: italic;
}
</style>
</head>
<body>
""")
    
    # ===== TITLE PAGE =====
    html_parts.append("""
<div class="title-page">
    <h1>Minecraft Successful</h1>
    <hr class="divider">
    <div class="subtitle">A Story-Driven Mission Book</div>
    <p class="tagline">Five players. Ten missions. One blocky world.</p>
    <p class="author">The Block Crew Chronicles</p>
</div>
""")
    
    # ===== TOC PAGE =====
    html_parts.append('<div class="toc-page">')
    html_parts.append('<h2>Table of Contents</h2>')
    
    for i, (_, title) in enumerate(chapters, 1):
        html_parts.append(f'<div class="toc-item"><span class="toc-num">{i}.</span><span class="toc-title">{title}</span></div>')
    
    html_parts.append("""
    <div class="toc-characters">
        <h3>🧱 The Block Crew</h3>
        <p><strong>Stone</strong> — Veteran miner. Practical, experienced, stubborn.</p>
        <p><strong>Red</strong> — Crew leader. Ambitious, fast-talking, always scheming.</p>
        <p><strong>Brick</strong> — Enforcer. Hot-headed, loyal, always ready to fight.</p>
        <p><strong>Pick</strong> — Strategist. Cautious, smart, always has a plan.</p>
        <p><strong>Gear</strong> — Tech expert. Builder, inventor, redstone genius.</p>
    </div>
""")
    html_parts.append('</div>')
    
    # ===== CHAPTERS =====
    for i, (filename, title) in enumerate(chapters, 1):
        md_content = read_chapter(filename)
        
        # Remove the first level-1 heading if present (we handle it)
        md_content = re.sub(r'^# .*?\n', '', md_content, count=1)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['extra', 'sane_lists']
        )
        
        # Wrap in mission header
        html_parts.append(f'<div class="chapter">')
        html_parts.append(f'<h1>Chapter {i}: {title}</h1>')
        html_parts.append(html_content)
        html_parts.append('</div>')
    
    # ===== FINAL PAGE =====
    html_parts.append("""
<div class="final-page">
    <h2>Thank you for reading!</h2>
    <p>"Minecraft isn't about beating the game.<br>It's about the crew you build along the way."</p>
</div>
""")
    
    html_parts.append("</body></html>")
    return '\n'.join(html_parts)

# Build HTML
html_content = build_html()
html_path = os.path.join(BOOK_DIR, "Minecraft_Successful.html")
with open(html_path, 'w') as f:
    f.write(html_content)

# Generate PDF with weasyprint
print("Generating PDF...")
pdf_path = os.path.join(BOOK_DIR, "Minecraft_Successful.pdf")
HTML(filename=html_path).write_pdf(pdf_path)

size = os.path.getsize(pdf_path)
print(f"PDF generated: {pdf_path} ({size/1024:.0f} KB)")
print("Done!")
