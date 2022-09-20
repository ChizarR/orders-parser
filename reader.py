from pathlib import Path

import openpyxl


def read_data(path_to_file: Path) -> dict:
    order = {}
    xlsx_data = openpyxl.load_workbook(path_to_file)
    sheet = xlsx_data.active
    dimensions = _parse_dimensions(sheet.dimensions)
    values = sheet[dimensions]

    index = 0
    for article, _, quantity in values:
        order[index] = {
            "article": _parse_article(article.value),
            "quantity": quantity.value
        }
        index += 1

    return order


def _parse_dimensions(raw_dimensions: str):
    dimensions = list(raw_dimensions)
    dimensions[1] = "2"
    return "".join(dimensions)


def _parse_article(raw_article: str) -> str:
    try:
        article = raw_article.split("(")
        return article[0] 
    except:
        return raw_article
        

def test():
    data = read_data(Path("./order.xlsx"))
    print(data)


if __name__ == "__main__":
    test()
