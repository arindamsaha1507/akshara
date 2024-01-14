"""Module for API calls."""

from fastapi import FastAPI

from akshara import varnakaarya as vk

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
