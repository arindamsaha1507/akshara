"""Contructs a list of varnas with all properties"""

import pandas as pd
import yaml

with open('varna.yml', 'r', encoding='utf-8') as file:
    dd = yaml.safe_load(file)

print(len(dd.keys()))
