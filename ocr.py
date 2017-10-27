
#!/usr/bin/python3
import pymysql
import os, glob
import re
import nltk
from nltk.corpus import stopwords
import enchant
import argparse

	

import traceback
import logging

d = enchant.Dict("en_US")
sw = set(stopwords.words('english'))
OUTPUT_DIR_TESSERACT = "/home/frank/youtube_data"
OUTPUT_DIR_OCRSPACE= "/home/frank/youtube_data_cloud"

db = pymysql.connect("localhost","root","123456","video_ocr")

cursor = db.cursor()

def insert_video():
	for file in glob.glob("*.mp4"):
		print(file)
		title = file
		url = os.path.abspath(file)
		sql = """INSERT INTO video_ocr(title,url) VALUES ('"""+title+"""','"""+url+"""')"""
		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			db.rollback()

def string_handle(sentence):
	sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence)
	words = [w for w in sentence.split() if w not in sw]
	for word in words:
		if d.check(word):
			print(1)
		else:
			print(word)
			words.remove(word)
	return words

def insert_keyword():
	sum1=0
	for dir in glob.glob(OUTPUT_DIR_OCRSPACE+"/*/"):
		print(dir)
		# sql="""SELECT id FROM video WHERE title LIKE '%"""+dir+"""%'"""
		# cursor.execute(sql)
		# results = cursor.fetchall()
		# for row in results:
		# 	id_video = row[0]
		text=''
		with open (dir+'text/final.txt','w+') as outfile:
			for file in glob.glob(dir+"/text/*.txt"):
				with open(file) as infile:
					sentence = infile.read().lower()
					# sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence)
					# words = [w for w in sentence.split() if w not in sw]
					# for word in words:
					# 	if d.check(word):
					# 		print(1)
					# 	else:
					# 		print(word)
					# 		words.remove(word)
					words = string_handle(sentence)
					sum1 = sum1+len(words)
					text = text + ' '+' '.join(words)
					# outfile.write(text)
			# text = outfile.read()
			print (text)
			folder_path = os.path.dirname(dir)
			path,folder_name = os.path.split(folder_path)
			sql = """UPDATE video_ocr SET keywords=\"%s\" WHERE title LIKE \"%%%s%%\"""" % (text,folder_name)
			#print(sql)
			print(sum1)
			try:
				#cursor.execute(sql)
				db.commit()
			except Exception as e:
				logging.error(traceback.format_exc())
				db.rollback()


def search_keyword(keyword):
	sql="""SELECT title FROM video WHERE keywords LIKE '%%%s%%'""" % keyword
	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		logging.error(traceback.format_exc())
		db.rollback()
	results = cursor.fetchall()
	for row in results:
		title = row[0]
		print(title)


def main():
	parser = argparse.ArgumentParser("OCR Search")
	parser.add_argument("--keyword", help="Enter a keyword to search")
	args = parser.parse_args()
	search_keyword(args.keyword)
	#insert_video()
	#insert_keyword()
	


if __name__ == '__main__':
    main()


