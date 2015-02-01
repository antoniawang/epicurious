import urllib2
import re
from bs4 import BeautifulSoup

#http://www.epicurious.com/tools/searchresults/all?search=ramos%20gin%20fizz&pageNumber=2&pageSize=10&resultOffset=11
search_base_url = "http://www.epicurious.com/tools/searchresults/all?search="
search_term = "Ramos Gin Fizz"
search_suffix = "&pageSize=1000"
starting_url = "http://www.epicurious.com"



def main():
    search_term_proper = search_term.replace(' ','%20').lower()
    search_url = search_base_url + search_term_proper+search_suffix
    contents = urllib2.urlopen(search_url).read()
    soup = BeautifulSoup(contents, "html.parser")
    rows =soup.find_all('a',attrs={"class" : "recipeLnk"})
    #rows += soup.find_all('a',attrs={"class" : "memberRecipeLnk"})
    rows_string = [str(x) for x in rows]
    print "\n".join(rows_string)
    print "\n \n"
    
    tuple_list = []
    for row in rows :
        if search_term.lower() in row.string.lower():
            tuple_list.append( (starting_url+row["href"], row.string))
    #print tuple_list
    
    import os
    count = 1
    try:
        os.unlink('Ramos_Gin_Fizz_Recipes')
    except: pass
    for href, text in tuple_list :
        print text, href
        contents = urllib2.urlopen(href).read()
        soup = BeautifulSoup(contents,"html.parser")
        rows =soup.find_all('ul',attrs={"class" : "ingredientsList"})
        
        ingredients = []
        for ingredient_list in rows:
            ingredients.append("Ramos Gin Fizz Recipe {}".format(count))
            for child in ingredient_list.children :
                if child.string is not None:
                    print child.string
                    ingredients.append(child.string)
                else:
                    ingredient_string = " ".join([str(x) for x in child.span.contents])
                    ingredient_string = re.sub('<a\s[^>]*>', "", ingredient_string)
                    ingredient_string = re.sub('</a>', "", ingredient_string)
                    ingredient_string = re.sub('\s+'," ", ingredient_string)
                    print ingredient_string
                    ingredients.append(ingredient_string)
                    
        count += 1
        ingredients = [x for x in ingredients if x != "\n" and len(x)>0]
        ingredients.append("\n")
        f = open('Ramos_Gin_Fizz_Recipes', 'a')
        print ingredients
        f.write("\n".join(ingredients))
        f.close()       


    







main()        