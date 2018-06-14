#-*- conding:utf-8 -*-
import time
from os import listdir
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = 'josuejoshua@163.com'
PASSWORD = 'll@1314woaini'
TEMPLATES_FOLDER = 'templates/'

class CrackWeiboLogin():
	def __init__(self):
		self.browser = webdriver.Chrome()
		self.wait = WebDriverWait(self.browser, 10)
		self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
		self.username = USERNAME
		self.password = PASSWORD

	def __del__(self):
		self.browser.close()

	def open(self):
		self.browser.get(self.url)
		username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
		password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
		submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
		username.send_keys(self.username)
		password.send_keys(self.password)
		submit.click()

	def get_position(self):
		try:
			img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
		except TimeoutException:
			print('未出现验证码')
			self.open()
		time.sleep(3)
		location = img.location
		size = img.size
		top, bottom, left, right = location['y'], location['y'] + size['height'], \
		                           location['x'], location['x'] + size['width']
		return (top, bottom, left, right)

	def get_screenshot(self):
		screenshot = self.browser.get_screenshot_as_png()
		screenshot = Image.open(BytesIO(screenshot))
		return screenshot

	def get_image(self, name='captcha.png'):
		top, bottom, left, right = self.get_position()
		print('验证码位置', top, bottom, left, right)
		screenshot = self.get_screenshot()
		# screenshot.save('screen')
		captcha = screenshot.crop((left, top, right, bottom))
		captcha.save(name)
		return captcha

	def detect_image(self, image):
		for template_name in listdir(TEMPLATES_FOLDER):
			print('正在匹配', template_name)
			template = Image.open(TEMPLATES_FOLDER + template_name)
			if self.same_image(image, template):
				numbers = [int(number) for number in list(template_name.split('.')[0])]
				print('拖动顺序', numbers)
				return numbers

	def is_pixel_equal(self, image1, image2, x, y):
		pixel1 = image1.load()[x, y]
		pixel2 = image2.load()[x, y]
		threshold = 20
		if abs(pixel1[0] - pixel2[0])<threshold and abs(pixel1[1] - pixel2[1])<threshold and abs(
				pixel1[2] - pixel2[2])<threshold:
			return True
		else:
			return False

	def same_image(self, image, template):
		threshold = 0.99
		count = 0
		for x in range(image.width):
			for y in range(image.height):
				if self.is_pixel_equal(image, template, x, y):
					count += 1
		result = float(count) / (image.width * image.height)
		if result > threshold:
			print('匹配成功')
			return True
		return False

	def move(self, numbers):
		circles = self.browser.find_elements_by_css_selector('.patt-wrap .patt-circ')
		dx = dy = 0
		for index in range(4):
			print(index)
			print('numbers', numbers[index])
			circle = circles[numbers[index]]
			if index == 0:
				ActionChains(self.browser)\
					.move_to_element_with_offset(circle, circle.size['width'] / 2, circle.size['height'] / 2)\
					.click_and_hold().perform()
			else:
				times = 30
				for i in range(times):
					ActionChains(self.browser).move_by_offset(dx / times, dy / times).perform()
					time.sleep(1 / times)
			if index == 3:
				ActionChains(self.browser).release().perform()
			else:
				dx = circles[numbers[index+1]].location['x'] - circle.location['x']
				dy = circles[numbers[index+1]].location['y'] - circle.location['y']

	def crack(self):
		self.open()
		image = self.get_image('captcha.png')
		numbers = self.detect_image(image)
		self.move(numbers)
		time.sleep(10)
		print('识别结束')


if __name__ == '__main__':
    crack = CrackWeiboLogin()
    crack.crack()