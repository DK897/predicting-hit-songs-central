from setuptools import setup, find_packages

setup(
    name="hit_song_prediction",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.5.3",
        "numpy>=1.24.3",
        "scikit-learn>=1.2.2",
        "matplotlib>=3.7.1",
        "seaborn>=0.12.2",
        "xgboost>=1.7.5",
    ],
    python_requires=">=3.8",
)