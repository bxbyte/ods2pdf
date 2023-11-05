import typing

import os.path as path
from json import dump, load
from contextlib import contextmanager

import dialog


ENCODING = "utf-8"
CONFIG_PATH = f"{dialog.CONFIG_DIR_PATH}/o2p.json"


class CurrentConfig(typing.TypedDict):
    template_b64: str
    table: tuple[tuple[str, str, str, str], ...]


@contextmanager
def load_config() -> typing.Iterator[CurrentConfig]:
    data = dict(
        template_b64="",
        table={}
    )
    if path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            try:
                data.update(load(file))
            except ValueError:
                ...
    try:
        try:
            yield data
        except Exception as error:
            raise error
    finally:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
            file.seek(0)
            dump(data, file, indent=4)
            file.truncate()
