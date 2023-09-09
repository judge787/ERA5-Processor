import time
import os
import zipfile
import sys
# import pyautogui 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException

city = "Charlottetown" #enter the city 
province = "PE" #enter the province in abbreviation
location = f"{city}, {province}" 

#enter all the coordinates
northCoordinate = 46.38 
southCoordinate = 46.12
westCoordinate = -63.60
eastCoordinate = -63.19

downloadButtonStartingNumber = 168 #the number of the first download button on the page, you can find it in the xpath

group = 3 #change the group number to the group number you are working on (different gorups have different years and different logins)

# choice 1 = request ERA5 data 
# choice 2 = request ERA5 land data
# choice 3 = download data er5

password = 'Era5processor1!' #only change the password if you manually make new accounts for each group and they all have the same password
#if statements to change the email address, years, and program choice depending on the group number
if group == 1:
    emailAddress = 'era5proc01@gmail.com'
    startYear = 1980
    endYear = 1999
    choice = 1

if group == 2:
    emailAddress = 'era5proc02@gmail.com'
    startYear = 2007
    endYear = 2020
    choice = 1

if group == 3:
    emailAddress = 'era5proc03@gmail.com'
    startYear = 1980
    endYear = 1985
    choice = 2

if group == 4:
    emailAddress = 'era5proc04@gmail.com'
    startYear = 1986
    endYear = 1990
    choice = 2

if group == 5:
    emailAddress = 'era5proc05@gmail.com'
    startYear = 1991
    endYear = 1994
    choice = 2

if group == 6:
    emailAddress = 'era5proc06@gmail.com'
    startYear = 1995
    endYear = 1999
    choice = 2

if group == 7:
    emailAddress = 'era5proc07@gmail.com'
    startYear = 2007
    endYear = 2011
    choice = 2

if group == 8:
    emailAddress = 'era5proc08@gmail.com'
    startYear = 2012
    endYear = 2016
    choice = 2

if group == 9:
    emailAddress = 'era5proc09@gmail.com'
    startYear = 2017
    endYear = 2020
    choice = 2


#paths for the different urls
urlEra5 = 'https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form'
urlEra5Land = 'https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=form'
urlRequests = 'https://cds.climate.copernicus.eu/cdsapp#!/yourrequests'

#paths for sub region selection
northPath = '//*[@id="area"]/div/div[1]/div/div[1]/input'
southPath = '//*[@id="area"]/div/div[1]/div/div[3]/input'
westPath = '//*[@id="area"]/div/div[1]/div/div[2]/div[1]/input'
eastPath = '//*[@id="area"]/div/div[1]/div/div[2]/div[2]/input'

#paths for specific buttons and fields
loginPath = '//*[@id="cds_menu_login"]/li/a'
netcdfPath = '//*[@id="format"]/div[2]/label[2]/input'
areaPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[7]/exclusive-frame-widget/div/fieldset/div/div/exclusive-frame-widget-content/div/div/div[2]/input'
loginSubmitPath = '//button[@data-drupal-selector="edit-submit"]'
radiationAndHeatPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[2]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[5]/div[1]/h4/a/span/i'

#paths for time selection
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september','october', 'november', 'december']
monthsName = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct', 'Nov', 'Dec']

#a list for the path to every month
monthsPaths = ['//*[@id="month"]/div[2]/label[1]/input', '//*[@id="month"]/div[2]/label[2]/input', '//*[@id="month"]/div[2]/label[3]/input', '//*[@id="month"]/div[2]/label[4]/input', '//*[@id="month"]/div[2]/label[5]/input', '//*[@id="month"]/div[2]/label[6]/input', '//*[@id="month"]/div[2]/label[7]/input', '//*[@id="month"]/div[2]/label[8]/input', '//*[@id="month"]/div[2]/label[9]/input', '//*[@id="month"]/div[2]/label[10]/input', '//*[@id="month"]/div[2]/label[11]/input', '//*[@id="month"]/div[2]/label[12]/input']

years = list(range(startYear, endYear + 1))
# yearPath = '//*[@id="year"]/div[2]/label[41]/input'

offsetYearPathNumber = startYear - 1939 

offsetYearPathNumber = 41
difference = startYear - 1980
offsetYearPathNumber = offsetYearPathNumber + difference
yearsPath = []
amountOfYears = endYear - startYear + 1
for i in range(amountOfYears):
    yearsPath.append(f'//*[@id="year"]/div[2]/label[{offsetYearPathNumber + i}]/input')


daysSelectAllPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[5]/string-list-widget/div/fieldset/string-list-widget-content/div[2]/select-clear-all/div/div/a[1]'
timeSelectAllPath = '//*[@id="time"]/div[2]/select-clear-all/div/div/a[1]'
monthsClearAll = '//*[@id="month"]/div[2]/select-clear-all/div/div/a[2]'
daysClearAll = '//*[@id="day"]/div[2]/select-clear-all/div/div/a[2]'
monthsSelectAllPath = '//*[@id="month"]/div[2]/select-clear-all/div/div/a[1]'
requestPath = '//*[@id="cds-download-form"]/div[3]/fieldset/input[3]'
yearsClearAll = '//*[@id="year"]/div[2]/select-clear-all/div/div/a[2]'
selectDeleteAllRequestsPath = '//*[@id="yr-delete-th"]'
deletePath = '//*[@id="refresh-delete-row"]/div[2]/button'
confirmDeletePath = '//*[@id="confirm_delete"]/div/div/div[3]/button[2]'

index =-1

#code for requestting ERA5Land data
hideLakePath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[2]/div[1]/h4/a'
hideSnowPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[3]/div[1]/h4/a'
hideSoilwaterPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[4]/div[1]/h4/a'
hideEvaporationPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[6]/div[1]/h4/a'
subregionExtractionPath = '//*[@id="exclusive-frame-area_group"]/div[2]/input'

timeSelectAllPathERA5Land = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[5]/string-list-widget/div/fieldset/string-list-widget-content/div[2]/select-clear-all/div/div/a[1]'
daysSelectAllPathERA5Land = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[4]/string-list-widget/div/fieldset/string-list-widget-content/div[2]/select-clear-all/div/div/a[1]'
yearsClearAllERA5Land = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[2]/string-choice-widget/div/fieldset/div/div/string-choice-widget-content/div[3]/div/a'
monthsClearAllERA5Land = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[3]/string-choice-widget/div/fieldset/div/div/string-choice-widget-content/div[3]/div/a'
yearsClearAllERA5Land = '//*[@id="year"]/div[3]/div/a'


dewPointTemparture2mPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[1]/div[2]/div/div/div[1]/label[1]/input'
temparture2mPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[1]/div[2]/div/div/div[1]/label[2]/input'
soilTemperatureLevel1Path = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[1]/div[2]/div/div/div[1]/label[4]/input'
soilTemperatureLevel2Path = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[1]/div[2]/div/div/div[1]/label[5]/input'
soilTemperatureLevel3Path = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[1]/div[2]/div/div/div[1]/label[6]/input'
surfaceSolarRadiationDownwardsPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[5]/div[2]/div/div/div[1]/label[6]/input'
surfaceThermalRadiationDownwardsPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[5]/div[2]/div/div/div[1]/label[7]/input'
uwindPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[7]/div[2]/div/div/div[1]/label[1]/input'
vWindPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[7]/div[2]/div/div/div[1]/label[2]/input'
surfacePressurePath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[7]/div[2]/div/div/div[1]/label[3]/input'
totalPrecipitationPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[7]/div[2]/div/div/div[1]/label[4]/input'
highvegetationPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[8]/div[2]/div/div/div[1]/label[1]/input'
lowvegetationPath = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[1]/string-list-array-widget/div/fieldset/div/div/div/string-list-array-widget-content/div[2]/uib-accordion/div/div[8]/div[2]/div/div/div[1]/label[2]/input'
selectAllWindPath = '//*[@id="accordiongroup-360-3405-panel"]/div/div/div[2]/a[1]'
year1980Path = '/html/body/div[1]/div/div/section/div[2]/div/div/div/resource-details/div[1]/div[1]/div[2]/div[2]/div/form-builder/form/div[1]/div[2]/string-choice-widget/div/fieldset/div/div/string-choice-widget-content/div[2]/label[31]/input'

browser = webdriver.Chrome()# Create Chrome driver

#functions that are used throught the program 
def click(variable, path): #function that clicks on a button
    name = variable
    try:
        variable = WebDriverWait(browser, 10).until( 
            EC.presence_of_element_located((By.XPATH, path)) 
        )
        variable.click()
    except:
        print_in_red(name + " not found")

def click_yellowText(variable, path): #function that clicks on a button and pritns out a yellow message
    name = variable
    try:
        variable = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        variable.click()
    except:
        print_in_yellow(name + " not found")

def inputCoordinates(direction, path, value): #function that inputs values into a text box
    name = direction
    try:
        direction = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, path))
        )
        direction.clear()
        direction.send_keys(value)

    except:
        print("\033[91m" + name + " input not found\033[0m")
#functions that are used to print out messages in different colors
def print_in_red(message):
    print("\033[91m" + message + "\033[0m")

def print_in_yellow(message):
    print("\033[93m" + message + "\033[0m")

def print_in_blue(message):
     print("\033[94m" + message + "\033[0m")

def print_in_green(message):
    print('\033[92m' + message + '\033[0m')

def login():#function used to login users  
    global browser, loginPath, loginSubmitPath, emailAddress, password

    click('login', loginPath)

    try: #finds the email and password input fields and inputs the values
        email = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="name"]'))
        )
        email.send_keys(emailAddress)

        passwordInput = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="pass"]'))
        )
        passwordInput.send_keys(password)

    except: #if the email or password input fields are not found, print out a message
        print("Email or password input fields not found")

    click('loginSubmit', loginSubmitPath)

def setUpERA5LandRequest(): #function that sets up the ERA5-Land request
    click('hideLake', hideLakePath)
    click('hideSnow', hideSnowPath)
    click('hideSoilwater', hideSoilwaterPath)
    click('hideEvaporation', hideEvaporationPath)

    click('2m dewpoint Temperature', dewPointTemparture2mPath)
    click('2m Temperature', temparture2mPath)
    click('Soil Temperature Level 1', soilTemperatureLevel1Path)
    click('Soil Temperature Level 2', soilTemperatureLevel2Path)
    click('Soil Temperature Level 3', soilTemperatureLevel3Path)
    click('Surface Solar Radiation Downwards', surfaceSolarRadiationDownwardsPath)
    click('Surface Thermal Radiation Downwards', surfaceThermalRadiationDownwardsPath)
    click('U wind', uwindPath)
    click('V wind', vWindPath)
    click('Surface Pressure', surfacePressurePath)
    click('Total Precipitation', totalPrecipitationPath)
    click('High vegetation', highvegetationPath)
    click('Low vegetation', lowvegetationPath)

    click(years[0], yearsPath[0])
    click(months[0], monthsPaths[0])

    click('daysSelectAll ERA5 Land', daysSelectAllPathERA5Land)
    click('timeSelectAll ERA5 Land', timeSelectAllPathERA5Land)
    click('subregion-extraction', subregionExtractionPath)

    inputCoordinates('north', northPath, northCoordinate)
    inputCoordinates('south', southPath, southCoordinate)
    inputCoordinates('west', westPath, westCoordinate)
    inputCoordinates('east', eastPath, eastCoordinate)

    click('netcdf', netcdfPath)

def requestPage(): #function that goes to the request page
    browser.get(urlRequests)
    login()
    print_in_blue(f"\nChoice: {choice}\nGroup: {group}\nStart year: {startYear}\nEnd year: {endYear}\n{location}") #prints out the users choices
    print_in_yellow("\nEnter y when you have deleted all previous requests")
    confirmLand = input()
    if confirmLand.lower() == 'y':
        return
    
def requestPageDownload(): #function that goes to the request page to download data
    browser.get(urlRequests)
    login()
    print_in_yellow("\nEnter y when you have changed downloadStartingNumber and restarted the program")
    confirmLand = input()
    if confirmLand.lower() == 'y':
        return
    

def get_years_path_land(start_year, end_year): #function that gets the path for the years
    offset_year_path_number = start_year - 1939
    offset_year_path_number = 31
    difference = start_year - 1980
    offset_year_path_number = offset_year_path_number + difference
    years_path = []
    amount_of_years = end_year - start_year + 1

    for i in range(amount_of_years):
        years_path.append(f'//*[@id="year"]/div[2]/label[{offset_year_path_number + i}]/input')
    
    return years_path

# #code for choice 1
if choice == 1:
    print_in_blue(f"\nChoice: {choice}\nGroup: {group}\nStart year: {startYear}\nEnd year: {endYear}\n{location}")
    browser.get(urlRequests)
    login()
    print_in_yellow("\nEnter y when you have deleted all previous requests")
    confirm = input()
    if confirm == 'y' or 'Y':
        browser.get(urlEra5) # Navigate to the URL
        print_in_blue(f"\nProceeding to the Request Page...\n")
        click('radiationAndHeat', radiationAndHeatPath) 
        click(years[0], yearsPath[0])
        click(months[0], monthsPaths[0])
        click('daysSelectAll', daysSelectAllPath)
        click('timeSelectAll', timeSelectAllPath)
        click('area', areaPath)

        inputCoordinates('north', northPath, northCoordinate)
        inputCoordinates('south', southPath, southCoordinate)
        inputCoordinates('west', westPath, westCoordinate)
        inputCoordinates('east', eastPath, eastCoordinate)

        click('netcdf', netcdfPath)

        print_in_yellow("\nUnder radiation and heat, check the follwing:\n\n-Surface solar radiation downwards\n-Surface thermal radiation downwards\n-Total sky direct solar radiation at surface are selected ")
        print("\nPlease enter y when you have selected the three above options.")
        confirmation = input()
        if confirmation == 'y' or 'Y':
            click('request', requestPath)
            click_yellowText('ERROR: delete january duplicate', deletePath)
            click_yellowText('ERROR: confirm delete january duplicate', confirmDeletePath)
        
            for i in range(startYear, endYear + 1): #for loop that goes through the years
                index += 1
                for j in range(0, 12): 
                    browser.get(urlEra5) # Navigate to the URL to request ERA5 data
                    
                    if j == 0: #if the month is january, click the clear all button and then click the right year for years
                        click('clearAllYears', yearsClearAll)
                        click(years[index], yearsPath[index])
                    
                    click('clearAllMonths', monthsClearAll)
                    click(months[j], monthsPaths[j])

                    if j == 2  or j == 4 or j == 6 or j == 9 or j ==11:
                        try:
                            click('selectAllDays', daysSelectAllPath)
                        except:
                            print(f"Days select all not found for {months[j]} {years[index]}")

                    try:
                        request = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.XPATH, requestPath))
                        )
                        request.click()
                        print_in_green(f"Requested ERA5 for {months[j]} {years[index]}")
                    except:
                        print_in_red(f"Request not found for {months[j]} {years[index]}")

        print_in_yellow("\nCheck the requests if all requests are correct (there could be a dupllicate january request for the first starting year)")
        time.sleep(60)
        sys.exit(0)

#offset year path number for era5land
offsetYearPathNumber = startYear - 1939 
offsetYearPathNumber = 31
difference = startYear - 1980
offsetYearPathNumber = offsetYearPathNumber + difference
yearsPath = []
amountOfYears = endYear - startYear + 1

for i in range(amountOfYears):
    yearsPath.append(f'//*[@id="year"]/div[2]/label[{offsetYearPathNumber + i}]/input')

if choice == 2:
    print_in_blue(f"\nChoice: {choice}\nGroup: {group}\nStart year: {startYear}\nEnd year: {endYear}\n{location}")
    browser.get(urlRequests)
    login()
    print_in_yellow("\nEnter y when you have deleted all previous requests")
    confirmLand = input()
    if confirmLand == 'y' or 'Y':
        print_in_blue(f"Proceeding to the Request Page...\n")
        browser.get(urlEra5Land) # Navigate to the URL
        click('hideLake', hideLakePath)
        click('hideSnow', hideSnowPath)
        click('hideSoilwater', hideSoilwaterPath)
        click('hideEvaporation', hideEvaporationPath)

        click('2m dewpoint Temperature', dewPointTemparture2mPath)
        click( '2m Temperature', temparture2mPath)
        click('Soil Temperature Level 1', soilTemperatureLevel1Path)
        click('Soil Temperature Level 2', soilTemperatureLevel2Path)
        click('Soil Temperature Level 3', soilTemperatureLevel3Path)
        click('Surface Solar Radiation Downwards', surfaceSolarRadiationDownwardsPath)
        click('Surface Thermal Radiation Downwards', surfaceThermalRadiationDownwardsPath) 
        click('U wind', uwindPath)
        click('V wind', vWindPath)
        click('Surface Pressure', surfacePressurePath)
        click('Total Precipitation', totalPrecipitationPath)
        click('High vegetation', highvegetationPath)
        click('Low vegetation', lowvegetationPath)

        click(years[0], yearsPath[0])
        click(months[0], monthsPaths[0])

        click('daysSelectAll ERA5 Land', daysSelectAllPathERA5Land)
        click('timeSelectAll ERA5 Land', timeSelectAllPathERA5Land)
        click('subregion-extraction', subregionExtractionPath)

        inputCoordinates('north', northPath, northCoordinate)
        inputCoordinates('south', southPath, southCoordinate)
        inputCoordinates('west', westPath, westCoordinate)
        inputCoordinates('east', eastPath, eastCoordinate)

        click('netcdf', netcdfPath)

        print_in_yellow("review documentation guide and ensure all values are checked ")
        print("\nPlease enter y when you have selected all the options.")

        confirmation = input()
        if confirmation == 'y' or 'Y':
            click('request', requestPath)
            click('selectDeleteAllRequests', selectDeleteAllRequestsPath)
            click('deleteAllDeleteRequests', deletePath)
            click_yellowText('ERROR: confirm delete january duplicates', confirmDeletePath)
        
            for i in range(startYear, endYear + 1):
                index += 1
            
                for j in range(0, 12): 
                
                    browser.get(urlEra5Land)
                    
                    if j == 0: #if the month is january, click the clear all button and then click the right year for years
                        click('clearAllYears', yearsClearAllERA5Land)
                        click(years[index], yearsPath[index])
                    
                    click('clearAllMonths', monthsClearAllERA5Land)
                    click(months[j], monthsPaths[j])

                    if j == 2  or j == 4 or j == 6 or j == 9 or j ==11: #these months the program has to select all days beacuse the last month had less days
                        try:
                            click('selectAllDays', daysSelectAllPathERA5Land)
                        except:
                            print(f"Days select all not found for {months[j]} {years[index]}")
                    
                    try:
                        request = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.XPATH, requestPath))
                        )
                        request.click()
                        print_in_green(f"Requested ERA5Land for {months[j]} {years[index]}")
                    except:
                        print_in_red(f"Request not found for {months[j]} {years[index]}")

        print_in_yellow("\nCheck the requests if all requests are correct (there could be a dupllicate january request for the first starting year)")
        time.sleep(180) #wait 3 minutes before the program closes
        sys.exit(0) #close the program


if choice == 3: # code for downloading the requests data
    print_in_blue(f"\nChoice: {choice}\nGroup: {group}\nStart year: {startYear}\nEnd year: {endYear}\n{location}")
    requestPageDownload()
    
    print_in_blue(f"\nDownloading ERA5 Data for {startYear} to {endYear}\n")
    
    browser.get(urlRequests) # Navigate to the URL

    index = -1 #used for months
    executions = 0  #redudant variable
    outerIndex = -1 #used for years
    for i in range(startYear, endYear + 1):
        outerIndex += 1 #used for years
    
        for j in range(0, 12): 
            index += 1
            success = 0

            try:
                
                try:
                    time.sleep(4) # Disable implicitly_wait method
                    downloadButton = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, f'//*[@id="cdsapp"]/div/div/table/tbody{[downloadButtonStartingNumber - index]}/tr/td[7]/span/a'))
                    )
                    downloadButton.click()
                    success = 1
                    print(f"downloaded file for {months[j]} {years[outerIndex]}, ")
                    time.sleep(3)
                except:
                    print_in_red(f"Download button not found for {months[j]} {years[outerIndex]}, please try again or manually download the file (choice#{choice})")
                
                downloads_folder = os.path.expanduser('~/Downloads') # Get the path of the default downloads folder
                files = os.listdir(downloads_folder) # Get the list of files in the downloads folder
                files.sort(key=lambda x: os.path.getmtime(os.path.join(downloads_folder, x)), reverse=True)
                latest_file = os.path.join(downloads_folder, files[0]) # Get the path of the latest file

                if choice == 3:  # Get the new file name
                    new_name = f'ERA5_{years[outerIndex]}_{monthsName[j]}.nc'
                    if success == 1 and not latest_file.endswith('.DS_Store') and len(latest_file)>50: #took away the latest file ==/.nc
                        os.rename(latest_file, os.path.join(os.path.dirname(latest_file), new_name)) # Rename the file
                        print_in_blue(f"Renamed {latest_file} to {new_name}")
                    else:
                        print_in_red(f"Error with renaming or downloading {months[j]} {years[outerIndex]}")
                elif choice == 4:
                    new_name = f'ERA5Land_{years[outerIndex]}_{monthsName[j]}.nc'
                    if success == 1 and not latest_file.endswith('.DS_Store') and not latest_file.endswith('.nc') : #took away the latest file ==/.nc
                        os.rename(latest_file, os.path.join(os.path.dirname(latest_file), new_name))
                        print_in_blue(f"Renamed {latest_file} to {new_name}")
                    else:
                        print_in_red(f"Error with renaming or downloading {months[j]} {years[outerIndex]}, latest file: {latest_file}, success: {success}")
                    # print (f"Length of new name:{len(new_name)}, old name length: {len(latest_file)}")  
            except:
                print_in_red(f"Error with {months[j]} {years[outerIndex]}")
    


                
