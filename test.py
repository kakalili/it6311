from poc_ocr import PoCOCR
import re
import nltk
from nltk.corpus import stopwords
import enchant

nltk.download('stopwords')
d = enchant.Dict("en_US")
poc_ocr = PoCOCR("config/settings.py")
sw = set(stopwords.words('english'))
OUTPUT_DIR_TESSERACT = "/home/frank/youtube_data"
OUTPUT_DIR_OCRSPACE= "/home/frank/youtube_data_ocr"
#with open("youtube.txt") as fp:
#	for line in fp:
#		print(line)
import os, fnmatch, glob
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def video_index():
	print(1)
	for file in glob.glob("*.mp4"):
		print(file)
		poc_ocr.run(file, OUTPUT_DIR_TESSERACT, 0.1, 'tesseract', 'eng')


def combine_all_text():
	sum1=0
	for dir in glob.glob(OUTPUT_DIR_TESSERACT+"/*/"):
		print(dir)
		with open (dir+'text/final.txt','w') as outfile:
			for file in glob.glob(dir+"/text/*.txt"):
				with open(file) as infile:
					sentence = infile.read().lower()
					words = [w for w in sentence.split() if w not in sw]
					for word in words:
						if d.check(word):
							print(1)
						else:
							words.remove(word)
					print(words)	
					sum1 = sum1 +len(words)

					#outfile.write(infile.read())
	print(sum1)
										

def main():
	video_index()
	combine_all_text()

	


if __name__ == '__main__':
    main()
