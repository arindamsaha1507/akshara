# Akshara

### Helps you spell!

![Linting Tests](https://github.com/arindamsaha1507/akshara/actions/workflows/pylint.yml/badge.svg)
![Code Tests](https://github.com/arindamsaha1507/akshara/actions/workflows/pytest.yml/badge.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/arindamsaha1507/akshara)
![GitHub last commit](https://img.shields.io/github/last-commit/arindamsaha1507/akshara)

Akshara is a tool for all your spelling needs. The package offers functions to:

1. Spell any given word (or any string) in Devanagari script.
2. Construct a word from a given spelling.
3. Count the number of svaras in a string.
4. Count the number of sentences in a string.
5. Obtain the syllables of a word.

# Installation

Latest version of akshara can be directly installed from PyPI using

```bash
pip3 install akshara
```

# Usage

## Load the varnakaarya module

```python
import akshara.varnakaarya as vk
```

## Obtain spelling (vinyaasa) of a word

```python
a = vk.get_vinyaasa("राम")       # a = ['र्', 'आ', 'म्', 'अ']
b = vk.get_vinyaasa("गमॢँ")       # b = ['ग्', 'अ', 'म्', 'ऌँ']
c = vk.get_vinyaasa("स पठति ।")  # c = ['स्', 'अ', ' ', 'प्', 'अ', 'ठ्', 'अ', 'त्', 'इ', ' ', '।']
```

## Obtain syllables (akshara) of a word

```python
a = vk.get_akshara("राम")       # a = ['रा', 'म']
b = vk.get_akshara("गमॢँ")       # b = ['ग', 'मॢँ']
c = vk.get_akshara("पठति")      # c = ['प', 'ठ', 'ति']
```

## Create a word (shabda) from a given vinyaasa

```python
d = vk.get_shabda(['स्', 'अ', 'ं', 'स्', 'क्', 'ऋ', 'त्' ,'अ', 'म्'])    # d = 'संस्कृतम्'
e = vk.get_shabda(['श्', 'इ', 'व्', 'अ', 'ः'])                        # e = 'शिवः'
f = vk.get_shabda(['द्', 'ए', 'व्', 'अ', 'द्', 'अ', 'त्', 'त्', 'अ३'])  # f = देवदत्त३
```

## Count svaras, vyanjanas, ayogavaahas and vaakyas

```python
g = "बुद्धं शरणं गच्छामि । धर्मं शरणं गच्छामि । सङ्घं शरणं गच्छामि ॥"

num_svaras = vk.count_svaras(g)            # num_svaras = 24
num_vyanjanas = vk.count_vyanjanas(g)      # num_vyanjanas = 30
num_ayogavaahas = vk.count_ayogavaahas(g)  # num_ayogavaahas = 6
num_varnas = vk.count_varnas(g)            # num_varnas = 60
num_vaakyas = vk.count_vaakyas(g)          # num_vaakyas = 3
```
