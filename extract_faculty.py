import requests
import re
import csv
from bs4 import BeautifulSoup


def save_to_csv(faculty_list, filename):
    keys = faculty_list[0].keys()
    with open(filename, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(faculty_list)


def extract_faculty():
    base_url = "https://dsi.udel.edu/faculty/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    url_regex = re.compile(r"(https?://[^\s]+)")
    title_regex = re.compile(r"professor|assistant|associate|lecturer|instructor|research")

    faculty_council_list = []
    resident_faculty_list = []
    affiliated_faculty_list = []
    adjunct_faculty_list = []

    for faculty_council in soup.select(".et_pb_module.et_pb_text.et_pb_text_1"):
        name = ""
        for i, faculty in enumerate(faculty_council.select(".listing_list")):
            if i % 2 == 0:
                name = faculty.text
            else:
                email = ""
                link = ""
                department = ""
                title = ""
                for f in faculty.text.splitlines():
                    if "college of" in f.lower():
                        department = f
                    if title_regex.search(f.lower()):
                        title = f
                    if email_regex.search(f):
                        email = f
                    if url_regex.search(f):
                        link = f
                faculty_dict = {
                    "name": name,
                    "email": email,
                    "link": link,
                    "department": department,
                    "title": title,
                }
                faculty_council_list.append(faculty_dict)
    save_to_csv(faculty_council_list, "data/faculty_council.csv")

    for resident_faculty in soup.select(".et_pb_module.et_pb_text.et_pb_text_2"):
        name = ""
        for i, faculty in enumerate(resident_faculty.select(".listing_list")):
            if i % 2 == 0:
                name = faculty.text
            else:
                email = ""
                link = ""
                for f in faculty.text.splitlines():
                    if email_regex.search(f):
                        email = f
                    if url_regex.search(f):
                        link = f
                faculty_dict = {
                    "name": name,
                    "email": email,
                    "link": link,
                }
                resident_faculty_list.append(faculty_dict)
    save_to_csv(resident_faculty_list, "data/resident_faculty.csv")

    for affiliated_faculty in soup.select(".et_pb_module.et_pb_text.et_pb_text_3"):
        name = ""
        for i, faculty in enumerate(affiliated_faculty.select(".listing_list")):
            if i % 2 == 0:
                name = faculty.text
            else:
                email = ""
                link = ""
                for f in faculty.text.splitlines():
                    if email_regex.search(f):
                        email = f
                    if url_regex.search(f):
                        link = f
                faculty_dict = {
                    "name": name,
                    "email": email,
                    "link": link,
                }
                affiliated_faculty_list.append(faculty_dict)
    save_to_csv(affiliated_faculty_list, "data/affiliated_faculty.csv")

    for adjunct_faculty in soup.select(".et_pb_module.et_pb_text.et_pb_text_4"):
        name = ""
        for i, faculty in enumerate(adjunct_faculty.select(".listing_list")):
            if i % 2 == 0:
                name = faculty.text
            else:
                email = ""
                link = ""
                for f in faculty.text.splitlines():
                    if email_regex.search(f):
                        email = f
                    if url_regex.search(f):
                        link = f
                faculty_dict = {
                    "name": name,
                    "email": email,
                    "link": link,
                }
                adjunct_faculty_list.append(faculty_dict)
    save_to_csv(adjunct_faculty_list, "data/adjunct_faculty.csv")


if __name__ == "__main__":
    extract_faculty()
