import json, os
from urllib.request import Request, urlopen


class Discord:
    @classmethod
    def send(cls, message):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
        }
        data = {"content": message}

        request = Request(
            os.getenv("WEBHOOK_URL", ""),
            data=json.dumps(data).encode("utf-8"),
            headers=headers
        )

        with urlopen(request) as response:
            assert response.status == 204
