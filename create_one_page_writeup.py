"""
Create one-page project write-up template.
"""

from pathlib import Path

def create_writeup_template():
    """Create one-page write-up template."""
    
    template = """HIT SONG PREDICTION USING MACHINE LEARNING
===========================================

TEAM MEMBERS: [Your Name], [Partner's Name]
COURSE: UE23CS352A Machine Learning
DATE: October 2025

PROBLEM STATEMENT
-----------------
Can we predict whether a song will be a hit based solely on its audio 
features extracted from the chorus? This project addresses the music 
industry's challenge of identifying potential hits through data-driven 
methods rather than subjective judgment.

APPROACH & METHODOLOGY
----------------------
We developed a comprehensive machine learning pipeline:

1. DATA COLLECTION: 41,106 songs from 1960s-2010s with Billboard chart data
2. FEATURE ENGINEERING: 66 features including audio characteristics and interactions
3. MODEL TRAINING: 6 algorithms (SVM, Logistic Regression, Neural Networks, etc.)
4. EVALUATION: Comprehensive metrics and visualization

KEY RESULTS
-----------
• BEST MODEL: Support Vector Machine (SVM)
• ACCURACY: 79.8% on test dataset
• KEY INSIGHT: Instrumentalness ratios are most important predictors
• BALANCED DATASET: 50% hits, 50% non-hits (30,829 train, 10,277 test)

TOP 5 PREDICTIVE FEATURES
--------------------------
1. Instrumentalness-Valence Ratio (31.1%)
2. Instrumentalness-Danceability Ratio (13.2%) 
3. Acousticness (6.9%)
4. Energy-Danceability Interaction (4.6%)
5. Danceability (3.8%)

IMPLEMENTATION OVERVIEW
-----------------------
- Python-based pipeline with scikit-learn
- Feature engineering for audio characteristics
- Comprehensive model evaluation
- Visualization and business insights
- Working prediction system

CHALLENGES & SOLUTIONS
----------------------
CHALLENGE: High-dimensional feature space
SOLUTION: Regularization and feature importance analysis

CHALLENGE: Imbalanced model performance  
SOLUTION: Ensemble of multiple algorithms

CHALLENGE: Feature engineering complexity
SOLUTION: Systematic feature creation and selection

CONCLUSION & IMPACT
-------------------
This project successfully demonstrates that machine learning can 
predict hit songs with 79.8% accuracy using audio features. The 
system provides valuable insights for the music industry, enabling:

• Data-driven song selection and optimization
• Reduced risk in music production investments
• Understanding of evolving musical preferences
• Democratized access to hit prediction capabilities

FUTURE WORK
-----------
• Real-time Spotify API integration
• Lyric sentiment analysis integration  
• Mobile application development
• Multi-genre specific models
• Industry partnership and deployment

CONTACT
-------
GitHub Repository: [Your Repository URL]
"""
    return template

def save_writeup_template():
    """Save write-up template to file."""
    reports_dir = Path("reports/final_report")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    template = create_writeup_template()
    writeup_file = reports_dir / "one_page_writeup.md"
    
    with open(writeup_file, 'w') as f:
        f.write(template)
    
    print(f"✅ One-page write-up template saved: {writeup_file}")
    return writeup_file

def main():
    print("📝 CREATING ONE-PAGE WRITE-UP TEMPLATE")
    print("=" * 50)
    
    writeup_file = save_writeup_template()
    
    print(f"\n📄 WRITE-UP TEMPLATE READY!")
    print("=" * 30)
    print(f"📍 File: {writeup_file}")
    print(f"📋 Sections: Problem, Approach, Results, Conclusion")
    print(f"🎯 Format: Ready for PDF conversion")
    
    print(f"\n💡 CONVERSION TO PDF:")
    print("=" * 30)
    print("1. Open the markdown file in VS Code")
    print("2. Install 'Markdown PDF' extension")
    print("3. Right-click → 'Markdown PDF: Export (pdf)'")
    print("4. Save as 'hit_song_prediction_writeup.pdf'")
    print("5. Submit the PDF with your repository URL")

if __name__ == "__main__":
    main()
