import json, datetime, re
from pathlib import Path
from typing import Union
from lib.discord import Discord


class ParkInfo:
    RE_PATTERN = r":(\w+):`(\d+)鯖 (\d+)番 ⏰(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})`"

    def __init__(self, notification_text: str):
        self.__notification_text = notification_text

        info = self._convert_text_to_park_info()

        self.__emoji: str = info["emoji"]
        self.__server: str = info["server"]
        self.__no: str = info["no"]
        self.__war_start_at: datetime.datetime = info["war_start_at"]

    def __str__(self):
        return self.__notification_text

    @property
    def emoji(self) -> str:
        return self.__emoji

    @property
    def server(self) -> str:
        return self.__server

    @property
    def no(self) -> str:
        return self.__no

    @property
    def war_start_at(self) -> datetime.datetime:
        return self.__war_start_at

    @classmethod
    def convert_text_to_list(cls, park_list_text: str) -> []:
        lines = park_list_text.splitlines()
        park_info_list = []

        for line in lines:
            match = re.match(cls.RE_PATTERN, line)

            if not match:
                continue

            park_info_list.append(ParkInfo(line))

        return park_info_list

    def _convert_text_to_park_info(self) -> Union[dict, None]:
        match = re.match(ParkInfo.RE_PATTERN, self.__notification_text)

        if not match:
            return None

        return {
            "emoji": match.group(1),
            "server": match.group(2),
            "no": match.group(3),
            "war_start_at": datetime.datetime.strptime(match.group(4), "%Y/%m/%d %H:%M:%S")
        }


class AramHistory:
    def __init__(self, json_str: str):
        self.__json_str = json_str
        self.__data = json.loads(json_str)

        self.__server = self.__data["server"]
        self.__no = self.__data["no"]
        self.__war_start_at = datetime.datetime.strptime(self.__data["war_start_at"], "%Y/%m/%d %H:%M:%S")
        self.__aram_type = int(self.__data["aram_type"])

    def __str__(self):
        return f"{self.__server}鯖 {self.__no}番 ⏰{self.__war_start_at} {self.__aram_type}"

    @property
    def server(self):
        return self.__server

    @property
    def no(self):
        return self.__no

    @property
    def war_start_at(self):
        return self.__war_start_at

    @property
    def aram_type(self):
        return self.__aram_type

    @classmethod
    def convert_text_to_list(cls, aram_history_text: str) -> []:
        lines = aram_history_text.splitlines()
        return [AramHistory(line) for line in lines]

    @classmethod
    def save(cls, file_path: Path, server: str, no: str, war_start_at: datetime.datetime, aram_type: int):
        aram_history = json.dumps({
            "server": server,
            "no": no,
            "war_start_at": war_start_at.strftime("%Y/%m/%d %H:%M:%S"),
            "aram_type": aram_type
        })

        with open(file_path, "a", encoding="utf-8") as f:
            print(aram_history, file=f)


class Aram:
    ARAM_TYPE_LIST = [30, 5, 1]

    def __init__(self, park_list_path: Path, aram_history_path: Path):
        self.__aram_history_path = aram_history_path
        self.__park_list = ParkInfo.convert_text_to_list(park_list_path.read_text(encoding="utf-8"))
        self.__aram_histories = AramHistory.convert_text_to_list(aram_history_path.read_text(encoding="utf-8"))

    def exec(self):
        now = datetime.datetime.now()

        for park in self.__park_list:
            if park.war_start_at < now:
                continue

            current_histories = [h.aram_type for h in self.__aram_histories if h.war_start_at == park.war_start_at]

            aram_type_list = list(set(self.ARAM_TYPE_LIST) - set(current_histories))

            for aram_type in aram_type_list:
                if now >= park.war_start_at - datetime.timedelta(minutes=aram_type):
                    AramHistory.save(self.__aram_history_path, park.server, park.no, park.war_start_at, aram_type)
                    Discord.send(message=f"@here {park} @約{aram_type}分前")
                    print("@here", park, f"@{aram_type}分前")
