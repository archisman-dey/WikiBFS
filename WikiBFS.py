"""
Finds minimum number of clicks needed to go
from one wikipedia article to another by performing
a BFS on the links
"""

import wikipedia as wiki
import sys

class Page (object):
	"""Class for a wikipedia page"""
	Title = None
	Links = []
	parent = None #determines which page this page comes from
	errorFree = True

	def __init__ (self, title, parent = None):
		self.Title = title
		self.parent = parent
	
	def makepage(self):
		"""Initialises the page list"""
		try : 
		
			page = wiki.page(title = self.Title)
			self.Links = page.links
		
		except wiki.exceptions.DisambiguationError:
			self.errorFree = False
			print("Encountered DisambiguationError for " + self.Title)

	def searchLinks (self, key):
		return (key in self.Links)


def findShortestPath (startPage, endPage):
	"""returns a page object for endPage with parents defined"""
	visited = {} #dictionary to store visited pages
	searchable = [startPage]  #used as a queue of links

	for page in searchable :
		page.makepage()

		if (page.errorFree == False) :
			continue
		if page.Title in visited :
			continue

		print("Searching " + page.Title)

		if page.searchLinks(endPage) :
			print("Found!")
			return page
		else :
			visited[page] = True

			for eachLink in page.Links :
				if eachLink in visited:
					continue

				next_page = Page(title = eachLink, parent = page)
				searchable.append(next_page)


def makeResult (page, endPage):
	"""returns a list of the articles needed to go from startpage to endpage"""
	result = [endPage]
	
	while (page != None):
		result.append(page.Title)
		page = page.parent

	result.reverse()
	return result

def printResult (array):
	for i in array[0:-1]:
		sys.stdout.write(i + " -> ")	#this is used to print without newline
	print(array[-1])

start = Page(input("Starting Page : ")) 
end = input("Page to look for : ")

try :
	end = wiki.page(title = end).title
except wiki.exceptions.DisambiguationError :
	print("DisambiguationError : " + end)
	sys.exit(0)

clicks = makeResult(findShortestPath(start, end), end)

printResult(clicks)
print(str(len(clicks)-1) + " clicks needed!")