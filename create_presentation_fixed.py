"""
Generate content for project presentation slides - FIXED VERSION.
"""

from pathlib import Path

def create_presentation_content():
    """Create presentation slide content."""
    
    slides = {
        "slide1": {
            "title": "Hit Song Prediction Using Machine Learning",
            "content": """
🎵 UE23CS352A Machine Learning Mini-Project

TEAM MEMBERS:
- [Your Name] - [Your SRN]
- [Partner's Name] - [Partner's SRN]

PROJECT OVERVIEW:
Predicting hit songs using audio features with 79.8% accuracy
"""
        },
        "slide2": {
            "title": "Problem Statement & Motivation",
            "content": """
PROBLEM:
Can we predict hit songs based solely on audio features?

MOTIVATION:
- Music industry invests billions in song production
- Traditional A&R is subjective and risky
- Data-driven approach can reduce uncertainty
- Understand what makes songs popular
"""
        },
        "slide3": {
            "title": "Dataset & Methodology",
            "content": """
DATASET:
- 41,106 songs from 1960s-2010s
- Billboard charts + audio features
- Balanced: 50% hits, 50% non-hits

METHODOLOGY:
1. Data Collection & Preprocessing
2. Feature Engineering (66 features)
3. Model Training (6 algorithms)
4. Evaluation & Visualization
"""
        },
        "slide4": {
            "title": "Feature Engineering",
            "content": """
FEATURES CREATED:

BASE FEATURES (14):
- danceability, energy, valence, tempo
- acousticness, instrumentalness, loudness
- speechiness, liveness, duration, etc.

ENGINEERED FEATURES (52):
- Feature interactions and ratios
- Temporal characteristics  
- Decade encodings
- Composite features
"""
        },
        "slide5": {
            "title": "Model Performance",
            "content": """
ACCURACY RESULTS:

🏆 SVM: 79.8% ✅
Logistic Regression: 75.7%
Neural Network: 69.8%
Random Forest: 62.1%
Gradient Boosting: 58.7%
XGBoost: 53.4%

KEY INSIGHT:
SVM performed best with complex feature relationships
"""
        },
        "slide6": {
            "title": "Key Findings",
            "content": """
WHAT MAKES A HIT SONG? 🔍

TOP 5 IMPORTANT FEATURES:
1. Instrumentalness-Valence Ratio (31.1%)
2. Instrumentalness-Danceability Ratio (13.2%)
3. Acousticness (6.9%)
4. Energy-Danceability Interaction (4.6%)
5. Danceability (3.8%)

INSIGHT:
Instrumental arrangement quality is most important!
"""
        },
        "slide7": {
            "title": "Visualizations & Insights",
            "content": """
GENERATED ANALYSIS:

📈 Model Comparison Charts
📊 Feature Importance Plots
🎯 ROC Curves & Confusion Matrices
📅 Decade-wise Hit Rate Analysis

BUSINESS VALUE:
- Clear insights into popular song characteristics
- Data-driven song optimization guidance
- Reduced risk in music production investments
"""
        },
        "slide8": {
            "title": "Live Demonstration",
            "content": """
PREDICTION SYSTEM WORKING:

Sample Song Analysis:
- "Dance Pop" -> 87% HIT probability ✅
- "Acoustic Ballad" -> 23% HIT probability ❌

REAL-TIME PREDICTION:
Input audio features -> Instant hit prediction
With confidence scores and feature insights
"""
        },
        "slide9": {
            "title": "Business Applications",
            "content": """
INDUSTRY IMPACT:

🎯 Record Labels:
- Early hit identification
- Portfolio optimization
- A&R decision support

🎵 Artists & Producers:
- Song arrangement guidance
- Feature optimization
- Market trend analysis

💰 Investors:
- Data-driven music investments
- Risk assessment
- Market analysis
"""
        },
        "slide10": {
            "title": "Conclusion & Future Work",
            "content": """
CONCLUSION:
✅ Successfully predicted hits with 79.8% accuracy
✅ Identified key audio features for popularity
✅ Built working prediction system
✅ Provided music industry insights

FUTURE WORK:
- Real-time Spotify API integration
- Lyric sentiment analysis
- Mobile app development
- Multi-genre specific models

THANK YOU! 🎵
Questions?
"""
        }
    }
    
    return slides

def save_presentation_content():
    """Save presentation content to files."""
    presentation_dir = Path("docs/presentation")
    presentation_dir.mkdir(parents=True, exist_ok=True)
    
    slides = create_presentation_content()
    
    # Save individual slides
    for slide_name, slide_content in slides.items():
        slide_file = presentation_dir / f"{slide_name}.txt"
        with open(slide_file, 'w') as f:
            f.write(f"TITLE: {slide_content['title']}\n\n")
            f.write(slide_content['content'])
    
    # Save combined presentation
    combined_file = presentation_dir / "full_presentation.txt"
    with open(combined_file, 'w') as f:
        f.write("HIT SONG PREDICTION - FULL PRESENTATION\n")
        f.write("=" * 50 + "\n\n")
        
        for slide_name, slide_content in slides.items():
            f.write(f"SLIDE: {slide_content['title']}\n")
            f.write("-" * 30 + "\n")
            f.write(slide_content['content'])
            f.write("\n" + "=" * 50 + "\n\n")
    
    print(f"✅ Presentation content saved to: {presentation_dir}/")
    return combined_file

def main():
    print("🎤 GENERATING PRESENTATION CONTENT - FIXED")
    print("=" * 50)
    
    presentation_file = save_presentation_content()
    
    print(f"\n📊 PRESENTATION READY!")
    print("=" * 30)
    print(f"📍 File: {presentation_file}")
    print(f"📋 Slides: 10 comprehensive slides")
    print(f"🎯 Content: Problem to solution with demo")
    
    print(f"\n💡 PRESENTATION TIPS:")
    print("=" * 30)
    print("- Practice with the live demo")
    print("- Focus on business impact")
    print("- Highlight the 79.8% accuracy achievement")
    print("- Show feature importance insights")
    print("- Prepare for technical questions")

if __name__ == "__main__":
    main()
