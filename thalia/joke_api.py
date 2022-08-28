from logging import getLogger
from pprint import pformat
from random import randint

from pyjokes import get_joke as pyjoke_get_joke
from requests import get
from requests import RequestException
from requests import Response


_LOGGER = getLogger(__name__)


def get_geek_joke() -> str:
    randnum = round(randint(1, 3))

    joke_method = {
        1: _from_dev_joke_api,
        2: _from_joke_api,
        3: _from_pyjoke,
    }[randnum]
    try:
        return joke_method()
    except Exception:
        _LOGGER.exception("Exception occured while trying to call a joke API.")

    return _from_pyjoke()


def _from_dev_joke_api() -> str:
    response = get("https://backend-omega-seven.vercel.app/api/getjoke", timeout=2)

    assert response.status_code == 200

    data = response.json()
    question, punchline = data[0].values()

    return f"{question}\n{punchline}"


def _from_joke_api() -> str:
    response = get("https://v2.jokeapi.dev/joke/Programming", timeout=2)

    _validate_request_response(response)

    data = response.json()

    if data.get("joke"):
        return data["joke"]
    else:
        question = data["setup"]
        punchline = data["delivery"]
        return f"{question}\n{punchline}"


def _from_pyjoke():
    return pyjoke_get_joke(language="en", category="neutral")


def _validate_request_response(response: Response) -> None:
    json_res = response.json()

    error = json_res.get("error")
    error = bool(error) if error else None

    if response.status_code != 200 or error:
        raise RequestException(
            f"Received response status {response.status_code}:\n" + pformat(json_res)
        )
