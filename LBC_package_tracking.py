from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
import requests
import time


tracking_number = '' #input your tracking number
sender_email = "" #sender email
password = "" #email password
receiver_email = "" #receiver email
frequency = 1800 # seconds

msg = EmailMessage()
msg['Subject'] = 'LBC Package Tracking for ' + tracking_number
msg['From'] = sender_email
msg['To'] = receiver_email

def sendemail(sender_email, password, message):
	server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
	server.login(sender_email, password)
	server.send_message(message)
	server.quit()

#Set Chrome as webdriver
driver = webdriver.Chrome(executable_path='  ') #place your webdriver exe path here
#Go to URL
driver.get("https://www.lbcexpress.com/track/") # LBC tracking page

#Find text box to input tracking number
inputTrackingNumber = driver.find_element_by_id("inputTrackingSearchForm")
#Input tracking number to text box
inputTrackingNumber.send_keys(tracking_number)

len_details = 0

while True:
	#Find button to search for tracking number then click it
	driver.find_element_by_css_selector("div[class='tt-sec-2 btntrackingSearchForm']").click()

	#Time delay to make sure page loads and URL is updated
	time.sleep(3)

	#Get current URL
	strUrl = driver.current_url
	#print(strUrl)

	#Get HTML of URL
	htmlcode = requests.get(strUrl)
	#print(r.content)

	#Create BeautifulSoup object
	soup = BeautifulSoup(htmlcode.content, 'html.parser')

	#Find the package tracking details such as date and status.
	tracking_details = soup.find_all('div', 'mobile-tracking-div2')
	details = []
	
	#Gets only the text
	for each in tracking_details:
	    details.append(str(each.get_text()))

	#Checks new updates. If new update then send to email.
	if len(details) > len_details:
		msg.set_content(''.join(details))
		sendemail(sender_email, password, msg)
	len_details = len(details)

	#Continue loop every X time
	time.sleep(frequency) #in seconds
