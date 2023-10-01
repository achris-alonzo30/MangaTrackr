from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from src.app import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import codecs
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
csrf = CSRFProtect(app)
WEBSITE_URL = "https://mangakakalot.com"


class SearchMangaTitle(FlaskForm):
    search_manga_title = StringField("Enter Manga Title", validators = [DataRequired()])
    submit = SubmitField("Search")


class AddManga(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    submit = SubmitField("Add Manga")


@app.route("/", methods = ["POST", "GET"])
def search_manga():
    form = SearchMangaTitle()

    if form.validate_on_submit():
        manga_title = form.search_manga_title.data

        driver = utils.initialize_driver()
        driver.get(WEBSITE_URL)

        if driver.title:
            print("Successfully accessed the website.")

            # Locate the search bar element
            search_mangas = driver.find_element(By.ID, 'search_story')

            if search_mangas:
                search_mangas.clear()

                cleaned_title = utils.clean_manga_title(manga_title)
                search_mangas.send_keys(cleaned_title.title())
                search_mangas.send_keys(Keys.RETURN)

                time.sleep(3)

                # Get the page source after waiting
                page_source = driver.page_source

                # Use BeautifulSoup to parse the page source
                soup = BeautifulSoup(page_source, 'html.parser')

                # Find all elements with class 'story_item'
                story_item_elements = soup.find_all('div', class_ = 'story_item')

                # Initialize a list to store the extracted data
                extracted_data = []

                for story_item in story_item_elements:
                    # Find the image source inside this 'story_item' div
                    image_src = story_item.find('img')['src']

                    # Find the 'story_item_right' div inside this 'story_item'
                    story_item_right = story_item.find('div', class_ = 'story_item_right')

                    # Find the title, author, and view_count inside the 'story_item_right'
                    title = story_item_right.find('h3', class_ = 'story_name').a.text
                    author = story_item_right.find('span').text
                    view_count = story_item_right.find_all('span')[2].text

                    # Create a dictionary to store the extracted data
                    data = {
                        'image_src': image_src,
                        'title': title,
                        'author': author,
                        'view_count': view_count
                    }

                    # Append the data to the list
                    extracted_data.append(data)

                extracted_data_json = json.dumps(extracted_data)
                if extracted_data_json:
                    return redirect(url_for('choose_manga', extracted_data = extracted_data_json))

        else:
            print("Search bar not found on the website.")

    else:
        print("Failed to access the website.")

    return render_template("search_manga.html", form = form)


@app.route("/choose_manga", methods=["GET", "POST"])
def choose_manga():
    form = AddManga()
    extracted_data_json = request.args.get('extracted_data')
    extracted_data = json.loads(extracted_data_json) if extracted_data_json else []

    if request.method == "POST":
        title = request.form.get("title")

        # Get the current directory where server.py is located
        current_directory = os.path.dirname(__file__)

        # Construct the path to manga_list.json using the current directory
        file_path = os.path.join(current_directory, "uploads", "files", "manga_list.json")

        with codecs.open(file_path, 'r', 'utf-8-sig') as json_file:
            manga_list = json.load(json_file)

        if title not in manga_list:
            manga_list.append(title)
            flash(f"Manga: {title} has successfully been added to your manga list.")
        else:
            flash(f"Manga: {title} is already in your manga list.")

            # Write the updated manga_list back to the JSON file
        with codecs.open(file_path, 'w', 'utf-8-sig') as json_file:
            json.dump(manga_list, json_file, ensure_ascii = False, indent = 4)

        return redirect(url_for('choose_manga', ))

    return render_template("choose_manga.html", form = form, extracted_data = extracted_data)


if __name__ == '__main__':
    app.run(debug = True)
