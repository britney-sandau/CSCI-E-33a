from django.shortcuts import render
from . import util
import markdown
from markdown2 import Markdown
import random

# Global variable used throughout
markdowner = Markdown()


def index(request):
    # Function used to display the main page.

    return render(request, "encyclopedia/index.html", {
        # Uses utility to display any created pages.
        "pages": util.list_entries()
    })


def new_page(request):
    # Function to display new page.

    return render(request, "encyclopedia/new_page.html")


def entry_page(request, title):
    # Function to test if a page has been created or is new.

    # Variable to get the title of a wiki page.
    create_page = util.get_entry(title)

    # Checks to see if wiki page exists, will return error if it does.
    if create_page is None:
        return render(request, "encyclopedia/error.html", {
            "page_name": title
        })

    # Adds the page if it is new and displays it.
    else:
        return render(request, "encyclopedia/entry.html", {
            "page": markdown_page(title),
            "page_name": title
        })


def markdown_page(title):
    # Function to display markdown pages in html.

    # variable to get the title of the page.
    page = util.get_entry(title)
    # Variable that uses markdown library to convert to html.
    html = markdown.markdown(page)
    return html if page else None


def search_page(request):
    # Function that checks to see if a page has been previously created

    if request.method == "GET":
        # Variable that gets the parsed url items after the "q"
        input = request.GET.get("q")

        # Variable to get the page if it has been created.
        pages = util.list_entries()
        # List to hold all created pages.
        search_pages = []
        # Variable that contains the html version of the markdown page.
        html = markdown_page(input)

        ''' Loops to convert title of page to upper case to check if it exists.
        Returns error message if it does. Will search for any letter in page title.
        Will also add the newly created page to the list of pages.'''
        for page in pages:

            if input.upper() in page.upper():
                search_pages.append(page)

        for page in pages:

            if input.upper() == page.upper():
                return render(request, "encyclopedia/entry.html", {
                    "page": html,
                    "page_name": input
                })

            elif search_pages != []:
                return render(request, "encyclopedia/search.html", {
                    "pages": search_pages
                })

            else:
                return render(request, "encyclopedia/error.html", {
                    "page_name": input
                })


def save_page(request):
    # Function to save a page.

    if request.method == "POST":
        pages = util.list_entries()
        input_title = request.POST["title"]
        input_text = request.POST["text"]
        html = markdown_page(input_title)
        double = "false"

        # Checks to see if page is a duplicate.
        for page in pages:

            if input_title.upper() == page.upper():
                double = "true"

        if double == "true":
            return render(request, "encyclopedia/double.html", {
                "page": html,
                "page_name": input_title
            })

        else:
            util.save_entry(input_title, input_text)
            create_page = util.get_entry(input_title)
            return render(request, "encyclopedia/entry.html", {
                "page": markdowner.convert(create_page),
                "page_name": input_title
            })


def edit_page(request):
   # Function to process the page once the edit button has been submitted.
    if request.method == "POST":
        input_title = request.POST["title"]
        text = util.get_entry(input_title)
        return render(request, "encyclopedia/edit.html", {
            "page": text,
            "page_name": input_title
        })


def update_page(request):
 # Function to update an existing page.
    if request.method == "POST":
        page_name = request.POST["title"]
        page = request.POST["text"]
        util.save_entry(page_name, page)
        html = markdown_page(page_name)
        return render(request, "encyclopedia/entry.html", {
            "page": html,
            "page_name": page_name
        })


def random_page(request):
    # Function to randomly display an existing page.
    pages = util.list_entries()
    random_page = random.choice(pages)
    html = markdown_page(random_page)
    return render(request, "encyclopedia/entry.html", {
        "page": html,
        "page_name": random_page
    })
