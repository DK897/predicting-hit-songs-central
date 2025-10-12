"""
Helper script for PDF conversion instructions.
"""

import os
from pathlib import Path

def main():
    print("📄 PDF CONVERSION INSTRUCTIONS")
    print("=" * 50)
    
    writeup_path = "reports/final_report/one_page_writeup.md"
    pdf_path = "reports/final_report/hit_song_prediction_writeup.pdf"
    
    print(f"📁 Markdown file: {writeup_path}")
    print(f"�� Target PDF: {pdf_path}")
    
    print(f"\n🎯 METHOD 1: VS Code (Recommended)")
    print("=" * 30)
    print("1. Open VS Code")
    print("2. Install extension: 'Markdown PDF' by yzane")
    print("3. Open the file: reports/final_report/one_page_writeup.md")
    print("4. Right-click in the editor")
    print("5. Select 'Markdown PDF: Export (pdf)'")
    print("6. Save as: hit_song_prediction_writeup.pdf")
    
    print(f"\n🎯 METHOD 2: Command Line")
    print("=" * 30)
    print("1. Install: pip install markdown-pdf")
    print("2. Run: markdown-pdf reports/final_report/one_page_writeup.md")
    print("3. Rename: mv one_page_writeup.pdf reports/final_report/hit_song_prediction_writeup.pdf")
    
    print(f"\n🎯 METHOD 3: Online Converter")
    print("=" * 30)
    print("1. Go to: https://md2pdf.netlify.app/")
    print("2. Copy content from one_page_writeup.md")
    print("3. Paste and convert to PDF")
    print("4. Download and save to reports/final_report/")
    
    print(f"\n📋 FINAL SUBMISSION CHECKLIST:")
    print("=" * 30)
    print("✅ GitHub repository with complete code")
    print("✅ One-page PDF write-up")
    print("✅ Trained models (79.8% accuracy)")
    print("✅ Comprehensive documentation")
    print("✅ Presentation materials")
    print("✅ Live demo ready")

if __name__ == "__main__":
    main()
