"""
Final organization and cleanup script.
"""

from pathlib import Path
import shutil
import os

def organize_final_structure():
    """Organize all files into proper structure."""
    print("📁 FINAL PROJECT ORGANIZATION")
    print("=" * 50)
    
    # Move scripts to scripts directory
    scripts_to_move = [
        'check_data.py', 'convert_to_pdf.py', 'create_one_page_writeup.py',
        'create_presentation_fixed.py', 'final_submission.py', 
        'generate_final_report.py', 'practice_presentation_fixed.py',
        'run_tests.py', 'submission_checklist.py', 'test_trained_models.py',
        'setup_environment.sh', 'setup.py'
    ]
    
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(exist_ok=True)
    
    moved_count = 0
    for script in scripts_to_move:
        if Path(script).exists():
            shutil.move(script, scripts_dir / script)
            print(f"✅ Moved: {script} -> scripts/")
            moved_count += 1
    
    print(f"\n📦 Organized {moved_count} script files")
    
    # Verify final structure
    print(f"\n📁 FINAL PROJECT STRUCTURE:")
    print("=" * 30)
    for item in sorted(Path('.').iterdir()):
        if item.name not in ['.git', 'venv', '__pycache__'] and item.is_dir():
            print(f"📁 {item.name}/")
            for subitem in sorted(item.iterdir()):
                if subitem.is_file():
                    print(f"   📄 {subitem.name}")
    
    return True

def create_final_checklist():
    """Create final submission checklist."""
    print(f"\n✅ FINAL SUBMISSION CHECKLIST")
    print("=" * 40)
    
    checklist = {
        "Source Code": Path("src").exists(),
        "Trained Models": Path("models/saved_models").exists(),
        "Documentation": Path("README.md").exists(),
        "Requirements": Path("requirements.txt").exists(),
        "Final Report": Path("reports/final_report/final_project_report.md").exists(),
        "One-Page Write-up": Path("reports/final_report/one_page_writeup.md").exists(),
        "Visualizations": Path("reports/figures").exists(),
        "Presentation": Path("docs/presentation").exists(),
        "Scripts Organized": Path("scripts").exists()
    }
    
    all_complete = True
    for item, complete in checklist.items():
        status = "✅" if complete else "❌"
        print(f"{status} {item}")
        if not complete:
            all_complete = False
    
    return all_complete

def main():
    print("🎵 HIT SONG PREDICTION - FINAL ORGANIZATION")
    print("=" * 60)
    
    # Organize files
    organize_final_structure()
    
    # Check completion
    ready = create_final_checklist()
    
    if ready:
        print(f"\n🎉 PROJECT IS COMPLETELY ORGANIZED AND READY FOR SUBMISSION!")
    else:
        print(f"\n⚠️  Some items need attention before submission.")
    
    print(f"\n🚀 FINAL COMMANDS TO RUN:")
    print("=" * 30)
    print("1. git add .")
    print("2. git commit -m 'Final organized project structure'")
    print("3. git push origin main")
    print("4. Convert reports/final_report/one_page_writeup.md to PDF")
    print("5. Submit GitHub URL + PDF before October 13, 2025")

if __name__ == "__main__":
    main()
