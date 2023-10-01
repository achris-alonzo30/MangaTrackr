import json
import time
import codecs
import re
from utils import clean_manga_title, initialize_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

WEBSITE_URL = "https://mangakakalot.com"


def get_latest_chapter_info(driver, manga_title):
    try:
        search_mangas = driver.find_element(By.ID, 'search_story')

        if search_mangas:
            search_mangas.clear()
            cleaned_title = clean_manga_title(manga_title)
            search_mangas.send_keys(cleaned_title.title())
            search_mangas.send_keys(Keys.RETURN)
            time.sleep(3)

            latest_chapter_element = driver.find_element(By.CSS_SELECTOR, '.story_chapter a')
            latest_chapter_url = latest_chapter_element.get_attribute("href")
            latest_chapter_text = latest_chapter_element.text.strip()

            match = re.search(r'Chapter (\d+)', latest_chapter_text)
            if match:
                latest_chapter_text = "Chapter " + match.group(1)
            else:
                latest_chapter_text = "N/A"

            return latest_chapter_url, latest_chapter_text
        else:
            print("Search bar not found on the website.")
    except Exception as e:
        print(e)
    return "N/A", "N/A"


def main():

    driver = initialize_driver()
    # Open the website using the WebDriver
    driver.get(WEBSITE_URL)

    # Check if the request was successful (status code 200)
    if driver.title:
        print("Successfully accessed the website.")

        # Read the JSON file containing manga titles
        file_path = "../../uploads/files/manga_list.json"
        with codecs.open(file_path, 'r', 'utf-8-sig') as json_file:
            manga_list = json.load(json_file)

        manga_info_list = []  # To store manga information

        # Loop through the manga titles
        for manga_title in manga_list:
            latest_chapter_url, latest_chapter_text = get_latest_chapter_info(driver, manga_title)

            # Store manga information in a dictionary
            manga_info = {
                manga_title: {
                    "latest_chapter_url": latest_chapter_url,
                    "latest_chapter_text": latest_chapter_text
                }
            }

            manga_info_list.append(manga_info)

        try:
            # Save manga information to the JSON file
            with open("../../uploads/files/manga_info.json", "w") as output_file:
                json.dump(manga_info_list, output_file, indent=4)
                print("Manga information saved to 'uploads/files/manga_info.json'.")
        except Exception as e:
            print(e)
    else:
        print("Failed to access the website.")

    # Close the WebDriver
    driver.quit()


if __name__ == "__main__":
    main()
