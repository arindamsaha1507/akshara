"""Module for API calls."""

from fastapi import FastAPI, Query
from akshara import varnakaarya as vk
from akshara.varna import Varnamaalaa

app = FastAPI()


@app.get("/vinyaasa")
async def api_vinyaasa(
    word: str = Query(..., description="The word to compute the vinyaasa for")
):
    """Return the vinyaasa of a word."""
    try:
        vinyaasa = vk.get_vinyaasa(word)
        status = "success"
    except AssertionError:
        vinyaasa = None
        status = "failure"

    return {"vinyaasa": vinyaasa, "status": status}


@app.get("/akshara")
async def api_akshara(
    word: str = Query(..., description="The word to compute the akshara for")
):
    """Return the akshara of a word."""

    try:
        varnas = vk.get_vinyaasa(word)
        status = "success"
    except AssertionError:
        return {"akshara": None, "status": "failure"}

    vn = Varnamaalaa()
    index_svara = [i for i, x in enumerate(varnas) if x in vn.svara]

    akshara = []
    start = 0
    for i in index_svara:
        akshara.append(vk.get_shabda(varnas[start : i + 1]))
        start = i + 1

    if index_svara and index_svara[-1] != len(varnas) - 1:
        akshara[-1] = vk.get_shabda(varnas[index_svara[-2] + 1 :])

    return {"akshara": akshara, "status": status}


@app.get("/shabda")
async def api_shabda(
    letters: str = Query(
        ..., description="Comma-separated letters to compute the shabda for"
    )
):
    """Return the shabda of a list of letters."""
    try:
        letter_list = letters.split(",")
        shabda = vk.get_shabda(letter_list)
        status = "success"
    except AssertionError:
        shabda = None
        status = "failure"

    return {"word": shabda, "status": status}
