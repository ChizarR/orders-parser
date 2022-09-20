from pathlib import Path
from typing import NamedTuple

from bs4 import BeautifulSoup


class MainParams(NamedTuple):
    dimensions: list
    containers: list



def parse_data(html: str):
    dimension, container = _get_main_params(html)
    _get_dimensions_info(dimension)
    _get_container_info(container)


def _get_main_params(html: str):
    soup = BeautifulSoup(html, "lxml")
    dimensions = soup.find_all(
        "div", class_="attribute-group",
        attrs={"data-display-name": "Dimensions"}
    )
    containers = soup.find_all(
        "div", class_="attribute-group",
        attrs={"data-display-name": "Container Information"}
    )
    return MainParams(
        dimensions,
        containers
    )



def _get_dimensions_info(dimensions):
    params = []
    for dimension in dimensions:
        clean_params = dimension.find_all("li")
        for param in clean_params:
            key = param.find("dt").text
            value = param.find("dd").find("span").text
            params.append({
                key: value
            })
        print(params)
    print()


def _get_container_info(containers):
    container_info = []
    for container in containers:
        data = container.find_all("li")
        for param in data:
            key = param.find("dt")
            value = param.find("dd")
            container_info.append({key.text: value.text})
        print(container_info)

