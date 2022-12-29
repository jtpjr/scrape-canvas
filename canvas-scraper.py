#!bin/python3
import argparse
import os
import re

from pathvalidate import sanitize_filename
from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.exceptions import Unauthorized, ResourceDoesNotExist, Forbidden, ResourceDoesNotExist
from canvasapi.file import File
from canvasapi.module import Module, ModuleItem


def extract_files(text):
    text_search = re.findall("/files/(\\d+)", text, re.IGNORECASE)
    groups = set(text_search)
    return groups
    
#---------------------------------------------------------
#Under construction:

def extract_video(text): #Extracts videos that are uploaded to canvas (instructure)
    #Currently only handles linked videos, and does not download, only provide link.

                                                
    linked = re.findall(r"(http:|https:[^\s]*?instructuremedia.com/embed/([a-z\-0-9]+))", text, re.IGNORECASE)
    #Returnerar innehållet inom paranteserna, dvs lista med (länk, id)
    longRegex = r"(http:|https:[^\s]*?canvas\.[^\s]*?\/courses\/[\d+][^\s]*?\/external_tools\/retrieve[^\s]*?instructuremedia\.com[^\s]+)"
    embedded = link_follow(re.findall(longRegex, text, re.IGNORECASE))
    
    videos = linked; embedded
    
    return videos
    
def link_follow(link):
    #TODO magi
    #Handle following links that require authentication, such as redirects (see issue #2 github)
    return ""

#Purpouse: handle indent based hiearchy
def posToPath(items, basePath): #Should create a list containing paths corres objects
    items.sort(key=lambda x: x.position, reverse=True)

    posPath = []

    #logic and recurPath()

    return posPath

def recurPath(items, posPath, path):
    #Recursive traversal
    #Problem: items is not list, but paginatedList (from canvasapi)
    #if items ...
    return ""

#Proper hiearchy may need revision of how folders are created -> change sequence of events in main script?
#----------------------------------------------------------

def get_course_files(course):
    modules = course.get_modules()

    files_downloaded = set() # Track downloaded files for this course to avoid duplicates
    
    videos_downloaded = set() # Track downloaded videos from instructuremedia to avoid duplicates
    
    for module in modules:
        module: Module = module
        module_items = module.get_module_items()
        for item in module_items:
            item: ModuleItem = item
            
            try:
                path = f"{output}/" \
                    f"{sanitize_filename(course.name)}/" \
                    f"{sanitize_filename(module.name)}/"
            except Exception as e:
                print(e)
                continue
            if not os.path.exists(path):
                os.makedirs(path)

            item_type = item.type
            print(f"{course.name} - "
                  f"{module.name} - "
                  f"{item.title} ({item_type})")

            if item_type == "File":
                file = canvas.get_file(item.content_id)
                files_downloaded.add(item.content_id)
                file.download(path + sanitize_filename(file.filename))
            elif item_type == "Page":
                page = course.get_page(item.page_url)

                #Error if placed in below try statement + done once
                nicetitle = item.title.replace("\/", " ") #Replace / with space. ex: "1/2" -> "1 2" instead of -> "12"
                
                try: #Subfolders for each page contents
                    pagepath = f"{output}/" \
                        f"{sanitize_filename(course.name)}/" \
                        f"{sanitize_filename(module.name)}/" \
                        f"{sanitize_filename(nicetitle)}/"
                except Exception as e:
                    print(e)
                    continue
                if not os.path.exists(pagepath):
                    os.makedirs(pagepath)
                with open(pagepath + sanitize_filename(nicetitle) + ".html", "w", encoding="utf-8") as f:
                    f.write(page.body or "")
                files = extract_files(page.body or "")
                for file_id in files:
                    if file_id in files_downloaded:
                        continue
                    try:
                        file = course.get_file(file_id)
                        files_downloaded.add(file_id)
                        file.download(pagepath + sanitize_filename(file.filename))
                    except ResourceDoesNotExist:
                        pass
#--------------------------------------------------------------- IN CONSTRUCTION!
                videos = extract_video(page.body or "") #Videos hosted on instructuremedia.com
                for video in videos:
                    print(video[0]) #debug
                    if video[1] in videos_downloaded:
                        continue
                    try:
                        #fuya_downloader(video[0]) #TODO
                        videos_downloaded.add(video[1])
                    except ResourceDoesNotExist:
                        pass
#--------------------------------------------------------------- 
            elif item_type == "ExternalUrl":
                url = item.external_url
                with open(path + sanitize_filename(item.title) + ".url", "w") as f:
                    f.write("[InternetShortcut]\n")
                    f.write("URL=" + url)
            elif item_type == "Assignment":
                assignment = course.get_assignment(item.content_id)
                with open(path + sanitize_filename(item.title) + ".html", "w", encoding="utf-8") as f:
                    f.write(assignment.description or "")
                files = extract_files(assignment.description or "")
                for file_id in files:
                    if file_id in files_downloaded:
                        continue
                    try:
                        file = course.get_file(file_id)
                        files_downloaded.add(file_id)
                        file.download(path + sanitize_filename(file.filename))
                    except ResourceDoesNotExist:
                        pass

    try:
        files = course.get_files()
        for file in files:
            file: File = file
            if not file.id in files_downloaded:
                print(f"{course.name} - {file.filename}")
                path = f"{output}/{sanitize_filename(course.name)}/" \
                    f"{sanitize_filename(file.filename)}"
                file.download(path)
    except Unauthorized:
        pass

    #debug2
    print("Downloaded:")
    print(videos_downloaded)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download all content from Canvas")
    parser.add_argument("url", help="URL to the Canvas website, e.g. https://canvas.utwente.nl")
    parser.add_argument("token", help="Token generated in the settings page on Canvas")
    parser.add_argument("output", help="Path to the output folder, e.g. output/")
    parser.add_argument("courses", help="Comma-separated course IDs or 'all'", nargs="?", const="all")
    args = parser.parse_args()

    # Handle args
    output = args.output.rstrip("/") + "/"

    if args.courses is None:
        args.courses = "all"
        print("No courses specified. Scraping all courses.")

    canvas = Canvas(args.url, args.token)

    courses = [] # courses to scrape

    # Select courses to scrape, default to all
    if args.courses != "all":
        courses = []
        ids = args.courses.split(",")
        for id in ids:
            courses.append(canvas.get_course( int(id) ))
    else:
        courses = canvas.get_courses()

    # Perform scrape
    for course in courses:
        course: Course = course
        try:
            get_course_files(course)
        except Forbidden:
                continue
        except ResourceDoesNotExist:
                continue
