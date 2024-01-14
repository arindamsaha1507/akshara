"""Module for API calls."""

from fastapi import FastAPI

from akshara import varnakaarya as vk

app = FastAPI()

@app.get("/vinyaasa/{word}")
async def vinyaasa(word: str):
    """Return the vinyaasa of a word."""

    vinyaasa = vk.get_vinyaasa(word)

    return {"vinyaasa": vinyaasa}

@app.get("/shabda/{letters}")
async def shabda(letters: str):
    """Return the shabda of a list of letters."""

    letters = letters.split(",")

    shabda = vk.get_shabda(letters)

    return {"word": shabda}