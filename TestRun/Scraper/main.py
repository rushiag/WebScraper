from bs4 import BeautifulSoup
import os
import functions
import requests


#main function 
#make HTTP request    --> requests
#use bs4			  --> beautifulsoup
#store cleaned data   --> functions
#read data 			  --> functions (optional)
#remove data		  --> functions (optional)

def main_scraper(url,directory):
	functions.create_directory(directory)
	source_code = requests.get(url)
	source_text = source_code.text
	soup = BeautifulSoup(source_text,"html.parser")
	articles = soup.find_all("article",{'class':'blog-post'})
	for article in articles:
		print("url: " + article.a.get("href"))
		print("title: "+ article.a.get("title"))
		print()
		article_formatted = "url: " + article.a.get("href") + "\n\n" +"title: "+ article.a.get("title") + "\n\n"
		if functions.does_file_exist(directory+"/articles.txt") is False:
			functions.create_new_file(directory+"/articles.txt")
	
		functions.write_to_file(directory+"/articles.txt", article_formatted)
		get_details(article.a.get("href"))





def get_details(url):
	source_code = requests.get(url)
	source_text = source_code.text
	soup = BeautifulSoup(source_text,"html.parser")
	divEntry = soup.find("div",{'class':'entry'}) #<div class="entry"><p></p> <p></p> .... </div>
	soup = BeautifulSoup(str(divEntry),'html.parser')
	paragraphs = soup.find_all("p")
	print("")
	print("Paragraphs: ")
	functions.write_to_file("DailyCoffeeNews/articles.txt","Paragraphs: \n")
	for p in paragraphs:
		if p.string is not None:
			if "coffee" in p.string: 
				print(p.string)
				functions.write_to_file("DailyCoffeeNews/articles.txt",p.string)
	print("-----------------------")
	print("-----------------------")
	print("-----------------------")
	print("-----------------------")
	functions.write_to_file("DailyCoffeeNews/articles.txt","--------------\n\n")









main_scraper("https://dailycoffeenews.com","DailyCoffeeNews")


















