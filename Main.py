from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080") 

DRIVER_PATH = "C:\\Users\\Shane\\proj\\chromedriver"
BASE_URL = 'https://www.daft.ie'
ALL_KK = '/kilkenny/residential-property-for-rent/?searchSource=rental'
KK_CITY = '/kilkenny/residential-property-for-rent/kilkenny/?searchSource=rental'
LOC_QUERY = ''


driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

def outPutResult(posts,LOC_QUERY):
    print(f'{len(posts)} results containing "{LOC_QUERY}"')
    f = open("results.txt","w+")
    for i,  post in enumerate(posts):
        amount = post.find('strong', class_ = 'PropertyInformationCommonStyles__costAmountCopy')
        if amount is None: amount = '?'
        else: amount = post.find('strong', class_ = 'PropertyInformationCommonStyles__costAmountCopy').text
        
        beds = post.find('div', class_ = 'QuickPropertyDetails__iconCopy')
        if beds is None: beds = '?'
        else: beds = post.find('div', class_ = 'QuickPropertyDetails__iconCopy').text

        bath = post.find('div', class_ = 'QuickPropertyDetails__iconCopy--WithBorder')
        if bath is None: bath = '?'
        else: bath = post.find('div', class_ = 'QuickPropertyDetails__iconCopy--WithBorder').text
        
        location = post.find('a', class_ = 'PropertyInformationCommonStyles__addressCopy--link')
        if location is None: location = '?'
        else: location = post.find('a', class_ = 'PropertyInformationCommonStyles__addressCopy--link').text

        link = post.find('div', class_ = 'PropertyImage__mainImageContainerStandard')
        if link is None: link = '?'
        else: link = post.find('a').get('href')

        typeOfList = post.find('div', class_= 'QuickPropertyDetails__propertyType').text
        if 'House to Rent' in typeOfList:
            typeOfList = 'House' 
        if 'Apartment to Rent' in typeOfList:
            typeOfList = 'Apartment'
        if 'Studio apartment to Rent' in typeOfList:
            typeOfList = 'Studio' 
        text = amount+', '+beds +' Beds, '+ bath + ' Bathrooms, Located ' + location + ' --- '+typeOfList + ' --- '+BASE_URL + link
        print(f'{i}:   {text}')
        f.write('{}\n'.format(f'{i}:   {text}'))
    
    
def stepThroughPages(posts, pageLink):
    driver.get(BASE_URL + pageLink)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    next = soup.find('li', class_ = 'next_page')
    posts.extend(soup.find_all('div', class_ = 'PropertyCardContainer__container'))
    if next is None: return posts
    page = next.find('a')
    return stepThroughPages(posts, page.get('href'))

def runOutPut (LOC_QUERY):
    LOC_QUERY = input("Enter your query: ")
    
    totalPosts = stepThroughPages([],KK_CITY)
    #totalPosts = stepThroughPages([], ALL_KK)
    totalPosts = [post for post in totalPosts if LOC_QUERY in  post.find('a', class_ = 'PropertyInformationCommonStyles__addressCopy--link').get_text().lower()]
    outPutResult(totalPosts,LOC_QUERY)



runOutPut(LOC_QUERY)

driver.quit()
