## Programming Languages in Wikipedia
import requests, json, re
from pprint import pprint
from bs4 import BeautifulSoup
import os.path

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
print("Exercise 3 Test:", clang['name'] == 'C')

################################################################
## Exercise 4
def getSidebar(lang):
   langContents = getPage(baseUrl + lang['link'])
   if langContents is None:
      return None
   return langContents.find('table', {'class': 'infobox'})

## If you have done this correctly, then getSidebar(clang) should
## return the sidebar of the C language's page
cSidebar = getSidebar(clang)
#-- print(cSidebar) #--

################################################################
## Exercise 5. You do not have to write any code.
## You are supposed to read the following three functions, and
## add comments above them and possibly inline, to explain what
## the functions do.

#  Returns a list of the text from an element
def getAnchorTexts(contents):
   return [
      anchor.get_text().lower()
      for anchor in contents.find_all("a", { 'href': re.compile("/wiki/(?!#cite)") })
   ]

#  Returns a list of the links from an element
def getAnchorLinks(contents):
   return [
      anchor.attrs['href']
      for anchor in contents.find_all("a", { 'href': re.compile("/wiki/(?!Category:|Wikipedia:|#cite)") })
   ]

#  Updates the language with more detail
def enrichLangEntry(lang):
   lang["paradigms"] = []
   lang["typeDiscipline"] = []
   lang["influenced"] = []
   lang["influencedBy"] = []
   sidebar = getSidebar(lang)
   if sidebar is None:
      return None
   for rowHeading in sidebar.find_all("th"):
      rowHeadingText = rowHeading.get_text().lower()
      rowContents = rowHeading.next_sibling     #.next_sibling  -- Had to remove these two parts
      nextRow = rowHeading.parent.next_sibling  #.next_sibling
      if rowHeadingText == "paradigm":
         lang["paradigms"] = getAnchorTexts(rowContents)
      elif rowHeadingText == "typing discipline":
         lang["typeDiscipline"] = getAnchorTexts(rowContents)
      elif rowHeadingText == "influenced":
         lang["influenced"] = getAnchorLinks(nextRow)
      elif rowHeadingText == "influenced by":
         lang["influencedBy"] = getAnchorLinks(nextRow)


if os.path.exists('data.txt'):
   #  Load data if it exists
   f = open('data.txt', 'r')
   allLanguages = eval(f.read())
   f.close()
   clang = [lang for lang in allLanguages
         if lang['name'] == 'C'][0]
else:
   ## This line will take a while to execute, as it reads all pages for all languages
   i = 0
   for lang in allLanguages:
      enrichLangEntry(lang)
      i += 1
      print("Enriching Languages ", round(100 * (i / len(allLanguages)), 1), "%", sep = "")

## If you have done these correctly, the following line should print for you
## the appropriate information for the C language
#-- pprint(clang)
print("Exercise 5 Test: ", 'paradigms' in list(clang.keys()))

#################################################################
## Exercise 6
allLangDict = {}
## Add your steps here
for lang in allLanguages:
   allLangDict[lang['link']] = lang

## If you've done this correctly, the following should give you back the C language:
all_c = allLangDict['/wiki/C_(programming_language)']
print("Exercise 6 Test:", clang == all_c)

#################################################################
## Exercise 7
missingLanguages = []
for lang in allLanguages:
   if 'influenced' in lang.keys():
      for l in lang['influenced']:
         if not l in allLangDict.keys() and not l in missingLanguages:
            missingLanguages.append(l)
   if 'influencedBy' in lang.keys():
      for l in lang['influencedBy']:
         if not l in allLangDict.keys() and not l in missingLanguages:
            missingLanguages.append(l)

## If you've done this correctly, the following should return 177 (194) languages
print("Exercise 7 Test", len(missingLanguages) == 194)
#-- pprint(missingLanguages)

#################################################################
## Exercise 8
inconsistencies = []
for lang1 in allLanguages:
   for lang2 in lang1["influenced"]:
      if lang2 in allLangDict.keys() and not lang1['link'] in allLangDict[lang2]['influencedBy']:
         tup = (lang2, "should be influenced by", lang1['link'])
         if not tup in inconsistencies:
            inconsistencies.append(tup)
   for lang2 in lang1["influencedBy"]:
      if lang2 in allLangDict.keys() and not lang1['link'] in allLangDict[lang2]['influenced']:
         tup = (lang2, "should be influence", lang1['link'])
         if not tup in inconsistencies:
            inconsistencies.append(tup)

#  508 inconsistencies at the time of writing
print("Exercise 7 Test", len(inconsistencies) == 508)

#################################################################
### Exercise 9
#
allParadigms = {}
for lang in allLanguages:
   for paradigm in lang['paradigms']:
      if paradigm in allParadigms.keys():
         allParadigms[paradigm].append(lang)
      else:
         allParadigms[paradigm] = [lang]

print("\nParadigms")
### After you are done, the following should print the results nicely:
#-- for paradigm in allParadigms:
#--    print(paradigm, ":", len(allParadigms[paradigm]))
#--    for lang in allParadigms[paradigm]:
#--       print("   " + lang["name"])
## And the following will print simply the counts, for those paradigms with over 5 languages:
for paradigm in allParadigms:
   length = len(allParadigms[paradigm])
   if length >= 5:
      print(paradigm, ":", length)

#################################################################
## Exercise 10
typeDisciplines = {}
for lang in allLanguages:
   for typeDis in lang['typeDiscipline']:
      if typeDis in typeDisciplines.keys():
         typeDisciplines[typeDis].append(lang)
      else:
         typeDisciplines[typeDis] = [lang]

print("\nType Disciplines")
### After you are done, the following should print the results nicely:
#-- for discipline in typeDisciplines:
#--    print(discipline, ":", len(typeDisciplines[discipline]))
#--    for lang in typeDisciplines[discipline]:
#--       print("   " + lang["name"])
## And the following will print simply the counts, for those disciplines with over 2 languages:
for discipline in typeDisciplines:
   length = len(typeDisciplines[discipline])
   if length >= 2:
      print(discipline, ":", length)
