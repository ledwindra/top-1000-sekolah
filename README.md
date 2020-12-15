# About

This repository aims to open source the data of top 1000 schools with highest
average score TPS UTBK in 2020. It structures the HTML format into a dataframe,
which can be readable for analysis.

Following are the documentations in respective language:
- [Bahasa Indonesia]()
- [English]()

# Do it locally

```bash
git clone https://github.com/ledwindra/top-1000-sekolah.git
cd top-1000-sekolah
```

Activate virtual environment and install dependencies.

```bash
# create virtual environment
python -m venv. venv

# activate virtual environment
source .venv/bin/activate

# upgrade package manager and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# run script
python --version # minimum python3.6 because of the f-string
python src/summary.py
python src/school_detail.py
```

Type `deactivate` to exit from the virtual environment.

# Data
Each data is located under `data` directory and is saved in a `.csv` format.