import urllib.request, urllib.error, urllib.parse, json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
    try:
        return urllib.request.urlopen(url)  # take this url go to the website and bring back data
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


# Return a dictionary with Search Recipes Complex
# https://spoonacular.com/food-api/docs#Search-Recipes-Complex
def searchByIngredient(include="", exclude="", number=2):
    base_url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {}
    params['apiKey'] = '15beae55a2934f559bd57ef947c28e1f'
    if include != "":
        params['includeIngredients'] = include
    if exclude != "":
        params['excludeIngredients'] = exclude
    params['instructionsRequired'] = True
    params['addRecipeInformation'] = True
    params['number'] = number
    apirequest = base_url + '?' + urllib.parse.urlencode(params)
    result = safeGet(apirequest)
    if result is not None:
        recipe_data = json.load(result)
        return recipe_data
    else:
        return "Sorry, couldn't retrieve the movie information."

# example url https://api.spoonacular.com/recipes/findByIngredients?apiKey=15beae55a2934f559bd57ef947c28e1f&ingredients=apples,+flour,+sugar&number=2

print(pretty(searchByIngredient()))



# Define a movie class to get relevant, useful information about a movie
class Recipes():
    def __init__(self, recipe, i):
        self.title = recipe['results'][i]['title']
        self.image = recipe['results'][i]['image']
        self.readyIn = recipe['results'][i]['readyInMinutes']
        self.servings = recipe['results'][i]['servings']
        self.pricePerServings = '$' + str(recipe['results'][i]['pricePerServing'])
        list = []
        for step in recipe['results'][0]['analyzedInstructions'][0]['steps']:
            for ingredient in step['ingredients']:
                list.append(ingredient['name'])

        self.ingredients = list
        self.url = recipe['results'][0]['sourceUrl']

list = []
for i in range(2):
    list.append(Recipes(searchByIngredient(), i))
    print(i)
