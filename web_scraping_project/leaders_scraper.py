import requests
root_url = " https://country-leaders.onrender.com/"
status_url = "status"
req = requests.get(f"{root_url}/{status_url}")
if req.status_code == 200:
    print(f"its ok:{req.text}")
else:
    print("responcse.status_code")

countries_url = "countries"
req = requests.get(f"{root_url}/{countries_url}")
countries = req.json()
print(countries)

# Query the enpoint, set the cookies variable and display it (2 lines)
cookie_url = "cookie"
cookie = requests.get(f"{root_url}/{cookie_url}").cookies
print(cookie)


# display the countries variable (1 line)
countries_url = f"{root_url}/countries"
countries = requests.get(countries_url, cookies=cookie).json()
print(countries)

# display the leaders variable (1 line)
leaders_url = f"{root_url}/leaders"
leaders = requests.get(leaders_url, cookies=cookie).json()
print(leaders)

def get_leaders():
    # 1,define the urls
    leaders_url = f"{root_url}/leaders"
    countries_url = f"{root_url}/countries"
    cookie_url = f"{root_url}/cookie"

    # 2, Get the cookies
    cookies = requests.get(cookie_url).cookies.get_dict()

    # 3 Get the countries
    countries = requests.get(countries_url, cookies=cookies).json()

    # 4 Dictionary to hold leaders per country
    leaders_per_country = {}
    for country in countries:
        leaders_response = requests.get(leaders_url, cookies=cookies, params={'country': country}).json()
        leaders_per_country[country] = leaders_response
    # 5 return the dictionary
    return leaders_per_country

leaders_per_country = get_leaders()
print(leaders_per_country)

first_leader = next(iter(leaders_per_country.values()))[0]
wiki_url = first_leader.get("wikipedia_url")
wiki_req = requests.get(wiki_url)
print(wiki_req.text)

from bs4 import BeautifulSoup
soup = BeautifulSoup(wiki_req.text, 'html.parser')
print(soup.prettify())

paragraphs = soup.find_all('p')
print(paragraphs)

first_paragraph = None
for paragraph in paragraphs:
    text = paragraph.get_text().strip()
    if text:  # Check if the paragraph is not empty
        first_paragraph = text
        break
print(first_paragraph)

def get_first_paragraph(wikipedia_url):
    print(wikipedia_url)        
    wiki_req = requests.get(wikipedia_url)   
    soup = BeautifulSoup(wiki_req.text, 'html.parser')
    paragraphs = soup.find_all('p')    
    first_paragraph = None
    for paragraph in paragraphs:
        first_paragraph = paragraph.get_text(strip=True)  
    return first_paragraph

first_paragraph = get_first_paragraph(wiki_url)
print(first_paragraph)

import re
#remove emultiple spaces and newlines
#ensures that all occurrences of multiple spaces, tabs, or newlines in the string are replaced with just one space.
first_paragraph = re.sub(r'\s+', ' ', first_paragraph)
#ensure space between lowercase and upper case
#ensures that when a lowercase letter is directly followed by an uppercase letter, a space is inserted between them.
first_paragraph = re.sub(r'([a-z])([A-Z])', r'\1 \2', first_paragraph)
print(first_paragraph)

def get_first_paragraph(wikipedia_url):
    print(wikipedia_url)        
    wiki_req = requests.get(wikipedia_url)   
    soup = BeautifulSoup(wiki_req.text, 'html.parser')
    paragraphs = soup.find_all('p')    
    first_paragraph = None
    for paragraph in paragraphs:
        first_paragraph = paragraph.get_text(strip=True)  
    return first_paragraph
first_paragraph = get_first_paragraph(wiki_url)
print(first_paragraph)


def sanitize_text(text): 
    # Replace any numbers in square brackets like [1], [2] with empty string
    text = re.sub(r'\[\d+\]', '', text)
    
    # Replace HTML entities with a space (e.g., '&amp;' becomes ' ')
    text = re.sub(r'&[a-z]+;', ' ', text)
    
    # Remove the URL in the markdown-style link: [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\s*\(.*?\)', r'\1', text)
    
    # Remove all characters that are not letters, digits, spaces, periods, commas, or single quotes
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\']+', '', text)
    
    # Remove trailing punctuation like periods, commas, exclamation marks, etc.
    text = re.sub(r'[.,;!?]+$', '', text)
    
    # Replace multiple spaces with a single space and strip leading/trailing spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Function to fetch and return the first valid paragraph from a Wikipedia page
#try-except block to handle potential errors like network issues or invalid URLs when fetching the Wikipedia page
def get_first_paragraph(wikipedia_url):
    try:
        # Fetch the Wikipedia page content
        wiki_req = requests.get(wikipedia_url)
        
        # Check if the request was successful
        if wiki_req.status_code == 200:
            # Parse the page content using BeautifulSoup
            soup = BeautifulSoup(wiki_req.text, 'html.parser')
            paragraphs = soup.find_all('p')
            
            # Iterate through paragraphs and return the first valid one after sanitizing
            for p in paragraphs:
                text = p.get_text().strip()
                if text:  # Only process non-empty paragraphs
                    return sanitize_text(text)
            return "No valid paragraphs found."
        
        else:
            return f"Failed to retrieve page. Status code: {wiki_req.status_code}"
    
    except requests.RequestException as e:
        return f"An error occurred: {str(e)}"

def get_leaders():
     # 1,define the urls
    root_url = "https://country-leaders.onrender.com" 
    status_url = "status"
    req = requests.get(f"{root_url}/{status_url}")
    if req.status_code == 200:    
        print(req.text) 
    else:
        print(f"Error to access website: {req.status_code}")        
    # 2, Get the cookies
    cookie_url = "cookie"    
    cookie = requests.get(f"{root_url}/{cookie_url}").cookies
     # 2, Get the countries
    countries_url = "countries"
    r = requests.get(f"{root_url}/{countries_url}", cookies=cookie)
    countries = r.json()    
    # 4 Dictionary to hold leaders per country
    leaders_url = 'leaders'
    leaders_per_country = {}
    for country in countries:        
            leader_r = requests.get(f"{root_url}/{leaders_url}", cookies=cookie, params={"country":country})        
            if leader_r.status_code == 200:
                leaders = leader_r.json()            
            leaders_per_country[country] = leaders
            for leader in leaders:
                print(f"Leader of {country}: {leader.get('first_name')} {leader.get('last_name')}, Wikipedia URL: {leader.get('wikipedia_url')}")
         
    return leaders_per_country

leaders_data = get_leaders()

def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    status_url = "status"
    
    # Check if the website is accessible
    req = requests.get(f"{root_url}/{status_url}")
    if req.status_code != 200:
        print(f"Error accessing the website: {req.status_code}")
        return {}
    
    print(req.text)
    
    # Fetch the countries and cookie
    countries_url = "countries"
    cookie_url = "cookie"
    cookie = requests.get(f"{root_url}/{cookie_url}").cookies
    countries_response = requests.get(f"{root_url}/{countries_url}", cookies=cookie)
    
    if countries_response.status_code != 200:
        print(f"Error fetching countries: {countries_response.status_code}")
        return {}
    
    countries = countries_response.json()
    
    leaders_url = 'leaders'
    leaders_per_country = {}
    
    for country in countries:
        # Get leaders for each country
        leader_r = requests.get(f"{root_url}/{leaders_url}", cookies=cookie, params={"country": country})
        
        if leader_r.status_code == 200:
            leaders = leader_r.json()
            country_leaders = {}
            
            for leader in leaders:
                full_name = f"{leader.get('first_name')} {leader.get('last_name')}"
                wikipedia_url = leader.get('wikipedia_url')
                
                if wikipedia_url:
                    first_paragraph = get_first_paragraph(wikipedia_url)
                    country_leaders[full_name] = first_paragraph
                    print(f"Leader of {country}: {full_name}, First Paragraph: {first_paragraph}")
            
            leaders_per_country[country] = country_leaders
    
    return leaders_per_country


def get_first_paragraph(wikipedia_url):
    print(wikipedia_url)
    r = requests.get(wikipedia_url)
    
    # Parse HTML content
    soup = BeautifulSoup(r.text, 'html.parser')
    paragraphs = soup.find_all('p')
    
    #get the 1st paragraph
    first_paragraph = None
    for paragraph in paragraphs:
        text = paragraph.get_text(separator=" ",strip=True)# this fix the words problem
        if text:  #check non-empty paragraphs
            first_paragraph = text
            break
        # clean up the text
    if first_paragraph: 
        first_paragraph = re.sub(r'\(\[\s?.*?\s?\]\s?\/.*?;?\)|\[\s?[a-zA-Z0-9]\s?\]', '', first_paragraph) #  remove like [1], [a]
    
    return first_paragraph
leaders_data = get_leaders()

def get_first_paragraph(wikipedia_url, session):
    wiki_req = session.get(wikipedia_url)
    soup = BeautifulSoup(wiki_req.text, 'html.parser')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        if p.text.strip():
            return sanitize_text(p.text.strip())
    return ""
leaders_url = leaders_per_country['be'][0]['wikipedia_url']
print("leaders wikepedia url:", leaders_url)
first_paragraph = get_first_paragraph(leaders_url, requests.session())
print("first paragraph from the wekepedia is:", first_paragraph)

# <25 lines
from requests import Session
import time

def session_loop_request(session, url, cookies=None, params=None, retry=False):    
    response = session.get(url, cookies=cookies, params=params)
    if response.status_code == 403 and not retry:       #this fix the cookie expired problem  
        print("Cookie expired. Refreshing cookie and retrying...")
        new_cookie = refresh_cookie(session)
        return session_loop_request(session, url, cookies=new_cookie, params=params, retry=True)
    response.raise_for_status()
    if "json" in response.headers.get("Content-Type", ""):
        return response.json()
    return response.text

def refresh_cookie(session): #this fix the cookie expired problem    
    root_url = "https://country-leaders.onrender.com"
    cookie_url = f"{root_url}/cookie"
    return session.get(cookie_url).cookies

def get_leaders():
    root_url = "https://country-leaders.onrender.com"    
    with Session() as session:        
        status_url = f"{root_url}/status"
        status_response = session.get(status_url)
        if status_response.status_code == 200:
            print(status_response.text)
        else:
            print(f"Error accessing the website: {status_response.status_code}")        
        cookie = refresh_cookie(session)
        countries_url = f"{root_url}/countries"
        countries = session_loop_request(session, countries_url, cookies=cookie)        
        leaders_per_country = {}
        leaders_url = f"{root_url}/leaders"
        for country in countries:
            country_leaders = {}
            leaders_data = session_loop_request(session, leaders_url, cookies=cookie, params={"country": country})            
            for leader in leaders_data:
                full_name = f"{leader.get('first_name')} {leader.get('last_name')}"
                wikipedia_url = leader.get('wikipedia_url')
                if wikipedia_url:                    
                    first_paragraph = get_first_paragraph(session, wikipedia_url)
                    country_leaders[full_name] = first_paragraph
                    print(f"Leader of {country}: {full_name}, First Paragraph: {first_paragraph}")            
            leaders_per_country[country] = country_leaders
            time.sleep(0.5)  # delay between countries to avoid overload
            
    return leaders_per_country

def get_first_paragraph(session, wikipedia_url):    
    print(wikipedia_url)
    response = session.get(wikipedia_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    first_paragraph = None
    for paragraph in paragraphs:
        text = paragraph.get_text(separator=" ",strip=True)# this fix the words problem
        if text:
            first_paragraph = text
            break 
    if first_paragraph: 
        first_paragraph = re.sub(r'\(\[\s?.*?\s?\]\s?\/.*?;?\)|\[\s?[a-zA-Z0-9]\s?\]', '', first_paragraph) #this fix refefences[1],[a]   
       
    return first_paragraph

leaders_data = get_leaders()

