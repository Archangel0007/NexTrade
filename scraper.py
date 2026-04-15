import requests
from bs4 import BeautifulSoup


URL = "https://www.screener.in/company/RELIANCE/consolidated/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_html(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def extract_top_ratios(html):
    soup = BeautifulSoup(html, "html.parser")
    ratios = {}

    items = soup.select("#top-ratios li")

    for item in items:
        name_elem = item.select_one(".name")
        value_elem = item.select_one(".value")

        if not name_elem or not value_elem:
            continue

        name = name_elem.get_text(strip=True)
        value = value_elem.get_text(" ", strip=True)

        ratios[name] = value

    return ratios

def extract_profit_loss_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table_data = {}

    table = soup.select_one("#profit-loss table.data-table")
    if not table:
        return table_data

    # headers (years)
    headers = [th.get_text(strip=True) for th in table.select("thead th")[1:]]

    # rows
    for row in table.select("tbody tr"):
        cols = row.select("td")
        if not cols:
            continue

        row_name = cols[0].get_text(strip=True)
        values = [td.get_text(strip=True) for td in cols[1:]]

        table_data[row_name] = dict(zip(headers, values))

    return table_data

def extract_balance_sheet_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table_data = {}

    table = soup.select_one("#balance-sheet table.data-table")
    if not table:
        return table_data

    # headers (years)
    headers = [th.get_text(strip=True) for th in table.select("thead th")[1:]]

    # rows
    for row in table.select("tbody tr"):
        cols = row.select("td")
        if not cols:
            continue

        row_name = cols[0].get_text(strip=True)
        values = [td.get_text(strip=True) for td in cols[1:]]

        table_data[row_name] = dict(zip(headers, values))

    return table_data

def extract_ratios_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table_data = {}

    table = soup.select_one("#ratios table.data-table")
    if not table:
        return table_data

    # headers (years)
    headers = [th.get_text(strip=True) for th in table.select("thead th")[1:]]

    # rows
    for row in table.select("tbody tr"):
        cols = row.select("td")
        if not cols:
            continue

        row_name = cols[0].get_text(strip=True)
        values = [td.get_text(strip=True) for td in cols[1:]]

        table_data[row_name] = dict(zip(headers, values))

    return table_data

def extract_shareholding(html):
    soup = BeautifulSoup(html, "html.parser")

    def parse_table(table):
        data = {}
        headers = [th.get_text(strip=True) for th in table.select("thead th")[1:]]

        for row in table.select("tbody tr"):
            cols = row.select("td")
            if not cols:
                continue

            row_name = cols[0].get_text(strip=True)
            values = [td.get_text(strip=True) for td in cols[1:]]

            data[row_name] = dict(zip(headers, values))

        return data

    result = {}

    # Quarterly
    q_table = soup.select_one("#quarterly-shp table")
    if q_table:
        result["quarterly"] = parse_table(q_table)

    # Yearly
    y_table = soup.select_one("#yearly-shp table")
    if y_table:
        result["yearly"] = parse_table(y_table)

    return result

def main():
    html = fetch_html(URL)

    print("=== TOP RATIOS ===")
    for k, v in extract_top_ratios(html).items():
        print(f"{k}: {v}")

    print("\n=== PROFIT & LOSS ===")
    for row, data in extract_profit_loss_table(html).items():
        print(f"\n{row}:")
        for year, value in data.items():
            print(f"  {year}: {value}")

    print("\n=== BALANCE SHEET ===")
    for row, data in extract_balance_sheet_table(html).items():
        print(f"\n{row}:")
        for year, value in data.items():
            print(f"  {year}: {value}")

    print("\n=== RATIOS ===")
    for row, data in extract_ratios_table(html).items():
        print(f"\n{row}:")
        for year, value in data.items():
            print(f"  {year}: {value}")

    print("\n=== SHAREHOLDING ===")
    sh = extract_shareholding(html)

    for period, table in sh.items():
        print(f"\n-- {period.upper()} --")
        for row, data in table.items():
            print(f"\n{row}:")
            for col, val in data.items():
                print(f"  {col}: {val}")

if __name__ == "__main__":
    main()