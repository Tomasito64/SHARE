## Overview

SHARE/
│
├── data/                       # (not tracked by git) folder with all data
│   ├──sharew1_[...]/
│   ├──sharew2_[...]/
│   ├──sharew3_[...]/
│   ├──sharew4_[...]/
│   ├──sharew5_[...]/
│   ├──sharew6_[...]/
│   ├──sharew7_[...]/
│   ├──sharew8_[...]/
│   └── concat/                  # (not tracked by git) folder with merged datasets
│       ├── concatwave1.csv.gz
│       ├── concatwave2.csv.gz
│       ├── concatwave3.csv.gz
│       ├── concatwave4.csv.gz
│       ├── concatwave5.csv.gz
│       ├── concatwave6.csv.gz
│       ├── concatwave7.csv.gz
│       └── concatwave8.csv.gz
│
├── src/
│   └── notebooks/
│       ├── Format.ipynb         # SCRIPT TO DELETE?
│       └── merge.ipynb          # script for merging and savings all new files
│
├── .gitignore
├── README.md
└── desktop.ini