import time
from datetime import date
from io import StringIO
from pathlib import Path
import shutil
import tempfile

import pandas as pd
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


URL = "https://www.pcso.gov.ph/searchlottoresult.aspx"
OUTPUT_CSV = "pcso_lotto_results.csv"
BASE_DIR = Path(__file__).resolve().parent
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")

    chrome_profile_dir = Path(
        tempfile.mkdtemp(prefix="pcso-chrome-profile-", dir=BASE_DIR)
    )

    chrome_args = [
        "--window-size=1400,1000",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--no-first-run",
        "--no-default-browser-check",
        "--remote-debugging-port=0",
        f"--user-agent={USER_AGENT}",
        f"--user-data-dir={chrome_profile_dir}",
        f"--disk-cache-dir={chrome_profile_dir / 'cache'}",
    ]

    for argument in chrome_args:
        options.add_argument(argument)

    try:
        driver = webdriver.Chrome(options=options)
    except (SessionNotCreatedException, WebDriverException) as exc:
        shutil.rmtree(chrome_profile_dir, ignore_errors=True)
        raise RuntimeError(
            "Chrome could not start for Selenium. Close any stuck Chrome or "
            "chromedriver processes, make sure Chrome is installed and updated, "
            "then run the scraper again. Original Selenium error: "
            f"{exc.__class__.__name__}: {exc.msg}"
        ) from exc

    driver.pcso_chrome_profile_dir = chrome_profile_dir
    return driver


def cleanup_driver(driver):
    chrome_profile_dir = getattr(driver, "pcso_chrome_profile_dir", None)

    try:
        driver.quit()
    finally:
        if chrome_profile_dir is not None:
            shutil.rmtree(chrome_profile_dir, ignore_errors=True)


def set_select_by_index(selects, index, visible_text):
    Select(selects[index]).select_by_visible_text(str(visible_text))


def scrape_date_range(driver, start_date, end_date):
    if start_date > end_date:
        return pd.DataFrame()

    driver.get(URL)
    time.sleep(2)

    selects = driver.find_elements(By.TAG_NAME, "select")

    if len(selects) < 7:
        page_text = driver.find_element(By.TAG_NAME, "body").text[:300]
        if "access denied" in page_text.lower() or "access denied" in driver.title.lower():
            raise RuntimeError(
                "PCSO returned an Access Denied page instead of the lotto search "
                "form. Try again later or use a different network if this persists."
            )

        raise RuntimeError(
            f"Expected at least 7 dropdowns, found {len(selects)}. "
            f"Page title: {driver.title!r}. Page text: {page_text!r}"
        )

    # Dropdown order on the page:
    # 0 = From Month
    # 1 = From Day
    # 2 = From Year
    # 3 = To Month
    # 4 = To Day
    # 5 = To Year
    # 6 = Lotto Game
    set_select_by_index(selects, 0, MONTHS[start_date.month - 1])
    set_select_by_index(selects, 1, start_date.day)
    set_select_by_index(selects, 2, start_date.year)

    set_select_by_index(selects, 3, MONTHS[end_date.month - 1])
    set_select_by_index(selects, 4, end_date.day)
    set_select_by_index(selects, 5, end_date.year)

    # Scrape all lotto games.
    set_select_by_index(selects, 6, "All Games")

    # Click Search button.
    buttons = driver.find_elements(
        By.XPATH, "//input[@type='submit' or @type='button']"
    )
    search_button = None

    for button in buttons:
        value = (button.get_attribute("value") or "").lower()
        if "search" in value or "view" in value:
            search_button = button
            break

    if search_button is None:
        # Fallback: try any button containing "Search" text.
        search_button = driver.find_element(
            By.XPATH,
            "//*[self::button or self::input][contains(translate(., 'SEARCH', 'search'), 'search')]",
        )

    search_button.click()
    time.sleep(3)

    tables = pd.read_html(StringIO(driver.page_source))

    results = []
    expected_cols = {
        "LOTTO GAME",
        "COMBINATIONS",
        "DRAW DATE",
        "JACKPOT (PHP)",
        "WINNERS",
    }

    for table in tables:
        table.columns = [str(col).strip().upper() for col in table.columns]

        if expected_cols.issubset(set(table.columns)):
            results.append(table)

    if not results:
        print(f"No result table found for {start_date} to {end_date}.")
        return pd.DataFrame()

    df = pd.concat(results, ignore_index=True)

    # Normalize column names.
    df = df.rename(
        columns={
            "LOTTO GAME": "lotto_game",
            "COMBINATIONS": "combinations",
            "DRAW DATE": "draw_date",
            "JACKPOT (PHP)": "jackpot_php",
            "WINNERS": "winners",
        }
    )

    df["scraped_range_start_year"] = start_date.year
    df["scraped_range_end_year"] = end_date.year

    return df


def scrape_range(driver, from_year, to_year=None):
    if to_year is None:
        to_year = from_year

    if to_year == date.today().year:
        end_date = date.today()
    else:
        end_date = date(to_year, 12, 31)

    return scrape_date_range(driver, date(from_year, 1, 1), end_date)


def clean_results(df):
    if df.empty:
        return df

    df = df.copy()

    df["draw_date"] = pd.to_datetime(df["draw_date"], errors="coerce")
    df["jackpot_php"] = (
        df["jackpot_php"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .replace("nan", None)
    )
    df["jackpot_php"] = pd.to_numeric(df["jackpot_php"], errors="coerce")
    df["winners"] = pd.to_numeric(df["winners"], errors="coerce")

    df = df.drop_duplicates(
        subset=["lotto_game", "combinations", "draw_date", "jackpot_php", "winners"]
    )

    return df.sort_values(["draw_date", "lotto_game"], ascending=[False, True])


def save_results(df, output_csv=OUTPUT_CSV):
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")


def scrape_full_history(output_csv=OUTPUT_CSV):
    driver = setup_driver(headless=True)

    all_results = []

    try:
        # PCSO page dropdown currently starts at 2016.
        current_year = date.today().year

        for year in range(2016, current_year + 1):
            print(f"Scraping {year}...")
            df = scrape_range(driver, year, year)

            if not df.empty:
                all_results.append(df)
                print(f"  Found {len(df)} rows.")

            time.sleep(1)

    finally:
        cleanup_driver(driver)

    if not all_results:
        print("No lotto results scraped.")
        return

    final_df = clean_results(pd.concat(all_results, ignore_index=True))
    save_results(final_df, output_csv)

    print(f"\nDone. Saved {len(final_df)} rows to {Path(output_csv).resolve()}")
    return final_df


def scrape_increment(start_date, end_date):
    driver = setup_driver(headless=True)

    try:
        print(f"Scraping updates from {start_date} to {end_date}...")
        return scrape_date_range(driver, start_date, end_date)
    finally:
        cleanup_driver(driver)


def update_history_csv(output_csv=OUTPUT_CSV, today=None):
    output_path = Path(output_csv)
    today = today or date.today()

    if not output_path.exists():
        return scrape_full_history(output_csv)

    existing_df = pd.read_csv(output_path)
    existing_df["draw_date"] = pd.to_datetime(existing_df["draw_date"], errors="coerce")
    latest_draw_date = existing_df["draw_date"].max()

    if pd.isna(latest_draw_date):
        return scrape_full_history(output_csv)

    start_date = latest_draw_date.date()
    if start_date > today:
        print(f"{output_path.name} is already updated through {latest_draw_date.date()}.")
        return existing_df

    new_df = scrape_increment(start_date, today)
    if new_df.empty:
        print(f"No new results found from {start_date} to {today}.")
        return existing_df

    final_df = clean_results(pd.concat([existing_df, new_df], ignore_index=True))
    save_results(final_df, output_csv)

    print(
        f"Updated {output_path.name}: added {len(new_df)} scraped rows, "
        f"{len(final_df)} total rows."
    )
    return final_df


def main():
    update_history_csv(OUTPUT_CSV)


if __name__ == "__main__":
    main()
