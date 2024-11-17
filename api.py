"""Module for API calls."""

from fastapi import FastAPI

from akshara import varnakaarya as vk
from akshara.varna import Varnamaalaa

app = FastAPI()


@app.get("/vinyaasa/{word}")
async def api_vinyaasa(word: str):
    """Return the vinyaasa of a word."""

    try:
        vinyaasa = vk.get_vinyaasa(word)
        status = "success"
    except AssertionError:
        vinyaasa = None
        status = "failure"

    return {"vinyaasa": vinyaasa, "status": status}


@app.get("/akshara/{word}")
async def api_akshara(word: str):
    """Return the akshara of a word."""

    try:
        varnas = vk.get_vinyaasa(word)
        status = "success"
    except AssertionError:
        akshara = None
        status = "failure"

    vn = Varnamaalaa()
    # num_svaras = sum(1 for x in varnas if x in vn.svara)
    index_svara = [i for i, x in enumerate(varnas) if x in vn.svara]

    akshara = []
    start = 0
    for i in index_svara:
        akshara.append(vk.get_shabda(varnas[start : i + 1]))
        start = i + 1

    if index_svara[-1] != len(varnas) - 1:
        akshara[-1] = vk.get_shabda(varnas[index_svara[-2] + 1 :])

    return {"akshara": akshara, "status": status}


@app.get("/shabda/{letters}")
async def api_shabda(letters: str):
    """Return the shabda of a list of letters."""

    letters = letters.split(",")

    try:
        shabda = vk.get_shabda(letters)
        status = "success"
    except AssertionError:
        shabda = None
        status = "failure"

    return {"word": shabda, "status": status}
