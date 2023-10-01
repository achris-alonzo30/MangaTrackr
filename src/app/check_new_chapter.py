import json
import time
import codecs
import re
from send_email import send_manga_update
from utils import clean_manga_title, initialize_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Define the website URL
WEBSITE_URL = "https://mangakakalot.com"
RECIPIENT_EMAIL = "mangapickr@gmail.com" # learn how to save in environment variable


def update_manga_info(manga_info_lists):
    driver = initialize_driver()
    # Open the website using the WebDriver
    driver.get(WEBSITE_URL)

    # Check if the request was successful (status code 200)
    if driver.title:
        print("Successfully accessed the website.")

        # Loop through the list of manga info dictionaries
        for manga_data in manga_info_lists:
            # Get manga title and its data
            manga_title = list(manga_data.keys())[0]
            manga_data = manga_data[manga_title]

            # Locate the search bar (inside the loop)
            search_mangas = driver.find_element(By.ID, 'search_story')

            # Check if the search bar element was found
            if search_mangas:
                # Clear the search bar by sending an empty string
                search_mangas.clear()

                # Clean the manga title
                cleaned_title = clean_manga_title(manga_title)

                # Enter the cleaned manga title into the search bar
                search_mangas.send_keys(cleaned_title.title())

                # Simulate pressing the Enter key to submit the search
                search_mangas.send_keys(Keys.RETURN)

                # Simulate a brief delay (adjust as needed)
                time.sleep(3)  # Delay for 3 seconds

                try:
                    latest_chapter_element = driver.find_element(By.CSS_SELECTOR, '.story_chapter a')
                    latest_chapter_text = latest_chapter_element.text.strip()

                    # Extract the chapter number using regular expressions
                    match = re.search(r'Chapter (\d+)', latest_chapter_text)
                    if match:
                        latest_chapter_text = "Chapter " + match.group(1)
                    else:
                        latest_chapter_text = "N/A"

                    # Split the latest_chapter_text on space and get the last part as the chapter number
                    chapter_parts = latest_chapter_text.split()
                    if len(chapter_parts) > 1:
                        website_chapter_number = int(chapter_parts[-1])  # Assuming chapter number is at the end
                    else:
                        website_chapter_number = None  # Handle cases where the format is unexpected

                    our_current_chapter_number = int(
                        manga_data["latest_chapter_text"].split()[-1])  # Assuming chapter number is at the end

                    if website_chapter_number > our_current_chapter_number:
                        # Update the manga data with the new information
                        manga_data["latest_chapter_url"] = latest_chapter_element.get_attribute("href")
                        manga_data["latest_chapter_text"] = latest_chapter_text

                        if manga_data["latest_chapter_url"] and manga_data["latest_chapter_text"]:
                            message = f"{manga_title} has a new chapter! {manga_data['latest_chapter_text']}.\n " \
                                      f"Here is the link: {manga_data['latest_chapter_url']}.\n"
                            print(message)

                            send_manga_update(message_update = message, recipient_email = RECIPIENT_EMAIL)

                    else:
                        print(f"No new chapter found for {manga_title}. You're updated to the latest chapter.")

                except Exception as e:
                    print(e)

            else:
                print("Search bar not found on the website.")

    else:
        print("Failed to access the website.")

    # Update the JSON file with the new manga information
    file_path = "../../uploads/files/manga_info.json"
    with codecs.open(file_path, "w", "utf-8-sig") as json_file:
        json.dump(manga_info_list, json_file, indent = 4, ensure_ascii = False)


if __name__ == "__main__":
    # Read the JSON file containing manga titles
    file_path = "../../uploads/files/manga_info.json"
    with codecs.open(file_path, "r", "utf-8-sig") as json_file:
        manga_info_list = json.load(json_file)

    # Update manga information
    update_manga_info(manga_info_list)
