## Programming Languages in Wikipedia
import requests, json, re
from pprint import pprint
from bs4 import BeautifulSoup

# The following function takes as input a full URL.
# It returns a BeautifulSoup object representing that web page's contents
# If the page does not exist, it returns None
def getPage(url):
   req = requests.get(url)
   if (req.status_code != 200):
      return None
   return BeautifulSoup(req.content, 'html.parser')

## You will need to add this to the relative links you may encounter
baseUrl = "https://en.wikipedia.org"

## This page contains a list of all programming languages that have Wikipedia pages
listPage = getPage(baseUrl + "/wiki/List_of_programming_languages")

################################################################
## Exercise 1
letterSections = [div for div in listPage.find_all('div', {'class': 'div-col'})]

## Test the above by making sure that:
#-- print(len(letterSections)) ## should be 26
## And that letterSections[0] contains all the languages that start with A
#-- print(letterSections[0])

################################################################
## Exercise 2
def getLanguagesFromSection(section):
   return [
      {
         'name': item.a.string,
         'link': item.a.attrs['href']
      }
      for item in section.find_all("li")
      if item.a is not None
   ]

## Use the following to test your function for the languages that start with A
theALanguages = getLanguagesFromSection(letterSections[0])
#-- print(len(theALanguages))         ## should be 55 (58)
## This for-loop should print things like: {'name': 'Autocoder', 'link': '/wiki/Autocoder'}
#-- for lang in theALanguages:
#--     print(lang)

################################################################
## Exercise 3
allLanguages = [
   lang
   for sec in letterSections
   for lang in getLanguagesFromSection(sec)
   
]

## If you have done this correctly, then
#-- print(len(allLanguages))  ## Should be 698 (717)
## You can use this as an example as you test the remaining exercises
clang = [lang for lang in allLanguages
         if lang['name'] == 'C'][0]
#-- print(clang)

################################################################
## Exercise 4
def getSidebar(lang):
   langContents = getPage(baseUrl + lang['link'])
   if langContents is None:
      return None
   return langContents.find(lambda x: x.name == 'tbody' and 
      (x.find('a', {'title': 'Software developer'}) != None or 
       x.find('a', {'title': 'Software design'}) != None))

## If you have done this correctly, then getSidebar(clang) should
## return the sidebar of the C language's page
cSidebar = getSidebar(clang)
#-- print(cSidebar)

################################################################
## Exercise 5. You do not have to write any code.
## You are supposed to read the following three functions, and
## add comments above them and possibly inline, to explain what
## the functions do.

#  Returns the text of a list of languages
def getAnchorTexts(contents):
   return [
      anchor.get_text().lower()
      for anchor in contents.find_all("a", { 'href': re.compile("/wiki/(?!#cite)") })
   ]

#  Returns the links of a list of languages
def getAnchorLinks(contents):
   return [
      anchor.attrs['href']
      for anchor in contents.find_all("a", { 'href': re.compile("/wiki/(?!Category:|Wikipedia:|#cite)") })
   ]

#  Expands the entry for a language
def enrichLangEntry(lang):
   lang["paradigms"] = []
   lang["typeDiscipline"] = []
   lang["influenced"] = []
   lang["influencedBy"] = []
   sidebar = getSidebar(lang)
   print('\n', lang['name'])
   if sidebar is None:
      return None
   for rowHeading in sidebar.find_all("th"):
      rowHeadingText = rowHeading.get_text().lower()
      print(rowHeadingText)

      rowContents = rowHeading.next_sibling.next_sibling
      nextRow = rowHeading.parent.next_sibling.next_sibling

      if rowHeadingText == "paradigm":
         lang["paradigms"] = getAnchorTexts(rowContents)
      elif rowHeadingText == "typing discipline":
         lang["typeDiscipline"] = getAnchorTexts(rowContents)
      elif rowHeadingText == "influenced":
         lang["influenced"] = getAnchorLinks(nextRow)
      elif rowHeadingText == "influenced by":
         lang["influencedBy"] = getAnchorLinks(nextRow)

## This line will take a while to execute, as it reads all pages for all languages
#i = 0
#for lang in allLanguages[50:100]:
#   enrichLangEntry(lang)
#   i += 1
#   print(i)
enrichLangEntry(clang)

## If you have done these correctly, the following line should print for you
## the appropriate information for the C language
pprint(clang)

#################################################################
### Exercise 6
#allLangDict = {}
### Add your steps here
#
### If you've done this correctly, the following should give you back the C language:
#allLangDict['/wiki/C_(programming_language)']
#
#################################################################
### Exercise 7
#missingLanguages = {}
#for lang in allLanguages:
#   pass
#   ## Add your work here
#
### If you've done this correctly, the following should return 177 languages
#len(missingLanguages)
#
#################################################################
### Exercise 8
#for lang1 in allLanguages:
#   for lang2 in lang1["influenced"]:
#      pass
#      ## Add your work here
#      ## It should include a print statement showing the links to the languages
#      ## that are not properly setup to point to each other.
#   ## You may need a second for loop
#
#################################################################
### Exercise 9
#
#allParadigms = {}
#for lang in allLanguages:
#   pass
#   ## Add your work here
#
#
#### After you are done, the following should print the results nicely:
#for paradigm in allParadigms:
#   print(paradigm, ":", len(allParadigms[paradigm]))
#   for lang in allParadigms[paradigm]:
#      print("   " + lang["name"])
### And the following will print simply the counts, for those paradigms with over 5 languages:
#for paradigm in allParadigms:
#   length = len(allParadigms[paradigm])
#   if length >= 5:
#      print(paradigm, ":", length)
#
#################################################################
### Exercise 10
#typeDisciplines = {}
#for lang in allLanguages:
#   pass
#   ## Add your work here
#
#
#### After you are done, the following should print the results nicely:
#for discipline in typeDisciplines:
#   print(discipline, ":", len(typeDisciplines[discipline]))
#   for lang in typeDisciplines[discipline]:
#      print("   " + lang["name"])
### And the following will print simply the counts, for those disciplines with over 2 languages:
#for discipline in typeDisciplines:
#   length = len(typeDisciplines[discipline])
#   if length >= 2:
#      print(discipline, ":", length)
#