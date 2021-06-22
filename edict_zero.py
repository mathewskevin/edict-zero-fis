#import webbrowser
import pdb, time, random, os
import pandas as pd
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pyautogui as pygui

site_name = 'https://edictzero.wordpress.com/'

# calculate random time to simulate human input
def rand_wait(lower, upper):
	time.sleep(random.uniform(lower, upper))

browser = webdriver.Firefox()
browser.get(site_name)
browser.maximize_window()

# get sidebar
sidebar = browser.find_element_by_css_selector('div[id=\'sidebar\']')
html_sidebar = sidebar.get_attribute('innerHTML')
soup_sidebar = BeautifulSoup(html_sidebar, 'html.parser')

# get sidebar links
hyperlinks = soup_sidebar.find_all('a')
df_hyperlinks_str = pd.DataFrame([str(i) for i in hyperlinks])
df_hyperlinks_str = df_hyperlinks_str[df_hyperlinks_str[0].str.contains('.mp3')] # use dataframe for filtering
text_list = []
for i in df_hyperlinks_str.index:
	text_list.append(hyperlinks[i].text)

# starting items
text_list = [i for i in text_list if i != 'MP3']
starting_name = [i for i in text_list if '203' in i][0]
starting_index = text_list.index(starting_name)
text_list = text_list[starting_index:]

# cycle through links & download mp3s
for i in text_list:
	# check directory list
	download_start = os.listdir(r'C:\Users\Kevin\Downloads')
	download_start = [i for i in download_start if i.endswith('.mp3')]
	print('saving', i)
	
	text_button = browser.find_element_by_link_text(i.strip())
	
	# https://stackoverflow.com/questions/41744368/scrolling-to-element-using-webdriver
	#actions = ActionChains(browser)
	#actions.move_to_element(text_button).perform()
	
	rand_wait(1,3); browser.execute_script("arguments[0].scrollIntoView();", text_button)
	rand_wait(1,3); text_button.click()
	rand_wait(3,4); pygui.press('space')
	rand_wait(1,2); pygui.moveTo(965,565)
	rand_wait(1,2); pygui.rightClick()
	
	# click save audio
	audio_saved = False
	print('\tgetting audio...')
	while audio_saved is False:
		try:
			rand_wait(1,2); pygui.click('save_audio.png') # click save audio
			audio_saved = True
		except:
			pass
	
	# click save
	audio_saved = False
	print('\twaiting for explorer...')
	while audio_saved is False:
		try:
			rand_wait(1,2); pygui.click('save_button.png') # click save in explorer
			audio_saved = True
		except:
			pass
	
	# wait for file to download
	audio_saved = False
	print('\tdownloading...')
	while audio_saved is False:
		time.sleep(0.5)
		download_current = os.listdir(r'C:\Users\Kevin\Downloads')
		download_current_mid = [i for i in download_current if i.endswith('.part')] 
		if len(download_current_mid) == 0:
			download_current = [i for i in download_current if i.endswith('.mp3')]
			if len(download_current) > len(download_start):
				audio_saved = True
	
	print('\tsaved', i)
	rand_wait(1,2); browser.back()
	rand_wait(1,4)

browser.close()
print('done.')