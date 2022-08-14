import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# # VARIABLES
SLEEP_TIME = 0.1

# # Driver Initialization
chrome_driver_path = "C:\Development\chromedriver.exe"

# # WINDOW SCROLL
def windowScroll(driver):
    """
    Scrolls webdriver window to load the full playlist items
    """
    win_length = driver.execute_script(
        'return document.getElementById("primary").scrollHeight;'
    )
    scroll_pt = 0
    while scroll_pt < win_length:
        driver.execute_script("window.scrollBy(0, 100)")
        scroll_pt += 100
        time.sleep(SLEEP_TIME)


def getElements(driver, cssSelector):
    elements = driver.find_elements(By.CSS_SELECTOR, value=cssSelector)
    return elements


def main(index, webURL):
    # Load Webpage
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(webURL)
    windowScroll(driver)

    # # GET ELEMENTS
    playlist_title = getElements(driver, "h1#title")[0]
    vid_times = getElements(
        driver, ".ytd-thumbnail span#text.ytd-thumbnail-overlay-time-status-renderer"
    )
    vid_titles = getElements(driver, "h3 a#video-title")

    # # ANALYSIS
    if len(vid_times) != len(vid_titles):
        print("The list lengths don't match.")
        return

    n_vids = len(vid_times)
    t_len = 0
    avg_len = 0

    for time in vid_times:
        timelist = str(time.text).split(":")
        t_len += float(timelist[-1]) / 3600
        t_len += float(timelist[-2]) / 60
        if len(timelist) == 3:
            t_len += float(timelist[0])

    avg_len = t_len / n_vids

    with open(
        f"./exportedData/{index}. {playlist_title.text}.json", mode="w", encoding="utf8"
    ) as file:
        file.write("{\n")
        file.write(f'\t"title" : "{playlist_title.text}",\n')
        file.write(f'\t"total videos" : "{n_vids}",\n')
        file.write(f'\t"total length" : "{t_len} hrs",\n')
        file.write(f'\t"average length per vid" : "{avg_len * 60} mins",\n')
        file.write('\t"videos": [\n')
        for i in range(n_vids):
            file.write("\t\t{\n")
            file.write(f'\t\t\t"index": "{i+1}",\n')
            title = vid_titles[i].text.replace('"', '\\"')
            file.write(f'\t\t\t"title": "{title}",\n')
            file.write(f'\t\t\t"time": "{vid_times[i].text}"\n')
            if i != n_vids - 1:
                file.write("\t\t},\n")
            else:
                file.write("\t\t}\n")
        file.write("\t]\n")
        file.write("}\n")

    print("SUCCESS !!!")
    driver.quit()


if __name__ == "__main__":
    with open("./links.txt", mode="r", encoding="utf8") as file:
        links = file.readlines()

    print(links)

    links = [
        link[:72]
        for link in links
        if link[:38] == "https://www.youtube.com/playlist?list=" and len(link) > 39
    ]

    print(links)

    start = time.time()
    for i in range(len(links)):
        st = time.time()
        main(i + 1, links[i])
        en = time.time()
        print(
            f"------------\nPlaylist {i+1} analysis finished in {en - st} s.\n------------"
        )
    end = time.time()
    print(f"------------\nProcess finished in {end - start} s.\n------------")
