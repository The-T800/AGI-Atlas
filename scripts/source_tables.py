"""只提取 HTML 表格，保留源单元格文本供审阅。"""

from html.parser import HTMLParser


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []

    def handle_data(self, value):
        if self.cell is not None:
            self.cell.append(value)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            if self.row is not None:
                self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.table is not None:
                self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


if __name__ == "__main__":
    import sys
    from pathlib import Path

    for name in sys.argv[1:]:
        parser = Tables()
        parser.feed(Path(f"data/research/sources/{name}.txt").read_text(encoding="utf-8"))
        print(name)
        for i, table in enumerate(parser.tables):
            print("TABLE", i)
            for row in table:
                print(" | ".join(row))
