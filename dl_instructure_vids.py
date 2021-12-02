from selenium import webdriver
import time
import urllib.request

USERNAME=""
PASSWORD=""
COURSE_URL=""
MODULE_ID_STRING=""

driver = webdriver.Firefox()



driver.get(COURSE_URL)

driver.find_element_by_id("username").send_keys(USERNAME)


driver.find_element_by_id("password").send_keys(PASSWORD)

driver.find_element_by_name("_eventId_proceed").click()

time.sleep(3)

element_list = []

for e in driver.find_elements_by_xpath("//a[contains(text(), '" + MODULE_ID_STRING + "')]"):
    lecture_link = e.get_attribute("href")
    name = e.get_attribute("title")
    print(name)
    if name != "":
        element_list.append((name, lecture_link))


for e in element_list:
    print(e)
    driver.get(e[1])
    part_elements = driver.find_elements_by_xpath("//*[contains(@href,'lu.instructuremedia.com/embed/')]")

    part_links = []

    for f in part_elements:
        part_links.append(f.get_attribute("href"))

    for i in range(len(part_links)):
        driver.get(part_links[i])
        time.sleep(4)

        source_element = driver.find_element_by_tag_name("source")

        src = source_element.get_attribute("src")
        urllib.request.urlretrieve(src, e[0].replace(r"/", "&") + " Part " + str(i + 1) + ".mp4") 

    time.sleep(3)

driver.quit()