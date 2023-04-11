from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys


# 1.Link of post
link = "https://www.facebook.com/groups/chomuabanphukiendienthoai/posts/1252357321930022/"

# 2.Driver browser
browser = webdriver.Edge(executable_path="./msedgedriver.exe")

# 3. Open browser with link provided
browser.get(link)

sleep(5)

# 4. Get more comments
more_comments = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/span/span")
more_comments.click()

sleep(5)

browser.close()