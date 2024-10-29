from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio
import time
import platform
from file import writeLine

from datetime import datetime, timedelta, timezone
load_dotenv()

# when = "NOV-2"
# where = "IN", "NP"
async def run_check(where, when, driver):
    step = ""

    # Set a wait time (can be adjusted)
    wait = WebDriverWait(driver, 30) 

    driver.get("https://prod.idp.collegeboard.org/signin")
    driver.find_element(by=By.ID, value="okta-signin-username").send_keys(
        os.getenv("collage_username")
    )
    driver.find_element(by=By.ID, value="okta-signin-password").send_keys(
        os.getenv("password")
    )
    step = "Signing In"

    driver.find_element(by=By.ID, value="okta-signin-password").send_keys(
        Keys.ENTER
    )

    wait.until(EC.url_contains("https://www.collegeboard.org/"))

    # Navigating to the dashboard
    step = "Navigating to the dashboard"
    driver.get("https://mysat.collegeboard.org/dashboard")

    # Clicking the "Register" button
    step = "Clicking the 'Register' button"
    
    wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR, 'a[href="https://satsuite.collegeboard.org/score-report-help#tms"]'
            )
        )
    )

    # wait.until(EC.presence_of_element_located((By.ID, "qc-id-header-register-button")))
    await asyncio.sleep(1)
    driver.find_element(By.ID, "qc-id-header-register-button").click()
    step = "Clicked"
    wait.until(EC.url_contains("personalInformation"))

    # Clicking the "Get Started" button
    step = "Clicking the 'Get Started' button"
    # wait.until(
    #     EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, 'a[href="https://privacy.collegeboard.org"]')
    #     )
    # )
    # print("++")
    wait.until(
        EC.element_to_be_clickable((By.ID, "qc-id-getstarted-button-getstarted"))
    ).click()

    # Clicking the "Confirm Graduation Date" and "Confirm Grade" buttons
    step = "Clicking the 'Confirm Graduation Date' and 'Confirm Grade' buttons"
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-personalinfo-button-graddateconfirm"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-personalinfo-button-gradeconfirm"))).click()

    # Clicking the "Continue" button for photo upload
    step = "Clicking the 'Continue' button for photo upload"
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-photoupload-confirmphoto-button-continue"))).click()

    # Clicking the "Continue" button in the student questionnaire
    step = "Clicking the 'Continue' button in the student questionnaire"
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-studentquestionnaire-button-continue"))).click()

    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "_2y5NMLSQe7uzCzmxl4K6Jn"))
    )
    driver.find_element(By.ID, "qc-id-studentquestionnaire-button-continue").click()

    visibility_names = [
        "qs-gpa",
        "qs-courseworkMath",
        "qs-courseworkEnglish",
        "qs-courseworkScience",
        "qs-courseworkSocialStudies",
        "qs-courseworkLanguages",
        "qs-highschoolActivities",
        "qs-educationLevel",
    ]

    # Repeated clicks for the questionnaire continue button
    step = "Repeated clicks for the questionnaire continue button"
    for _ in range(8):
        wait.until(
            EC.visibility_of_element_located((By.ID, visibility_names[_]))
        )
        driver.find_element(By.ID, "qc-id-studentquestionnaire-button-continue").click()

    # Clicking the "Get Started" button for selecting date and center
    step = "Clicking the 'Get Started' button for selecting date and center"
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-selectdatecenter-button-getstarted"))).click()

    # Accepting terms and conditions
    step = "Accepting terms and conditions"
    wait.until(EC.presence_of_element_located((By.ID, "qc-id-termsconditions-scrollbox-termsconditions"))).click()
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    wait.until(EC.element_to_be_clickable((By.ID, "terms-acceptance-checkbox"))).click()

    # Clicking the continue button after accepting terms
    step = "Clicking the continue button after accepting terms"
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-termsconditions-button-continue"))).click()

    # Proceeding to select the test location
    step = "Proceeding to select the test location"
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-selectdatecenter-testlocation-button-next"))).click()

    # Selecting the test date
    step = "Selecting the test date"
    wait.until(EC.element_to_be_clickable((By.ID, f"qc-id-selectdatecenter-testdate-button-{when}"))).click()

    # Clicking continue after selecting the test date
    step = "Clicking continue after selecting the test date"
    wait.until(EC.element_to_be_clickable((By.ID, "testdate-continue-button"))).click()

    # Select Where
    step = "Selecting the test center location"
    if where != 'NP':
        select_element = driver.find_element(by=By.ID, value="qc-id-selectdatecenter-testcenter-international-list-country")
        select = Select(select_element)
        select.select_by_value(where)

    # Searching for test centers
    step = "Searching for test centers"
    wait.until(EC.element_to_be_clickable((By.ID, "qc-id-selectdatecenter-testcenter-international-button-search"))).click()

    # Toggling to show available test centers only
    wait.until(EC.presence_of_element_located((By.ID, "qc-id-selectdatecenter-testcenter-toggle-showavailableonly"))).click()
    await asyncio.sleep(2)

    step = "Looking at centers"

    raw_result = driver.find_element(
        by=By.TAG_NAME, value="table"
    )

    result = str(raw_result.text).replace("\n", ",")
    result_arr = result.split(",")

    schools = ""
    for index, line in enumerate(result_arr):
        if line == "Seat is Available":
            schools += f"{(result_arr[index - 1])}, "
    driver.quit()
    return schools


async def run_try(where, when):
    
    kathmandu_offset = timedelta(hours=5, minutes=45)
    kathmandu_tz = timezone(kathmandu_offset)
    kathmandu_time = datetime.now(kathmandu_tz)

    logTime = kathmandu_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{logTime}] Check")
    
    
    writeLine(f"[{logTime}] Check")
    
    options = Options()
    options.add_argument("--no-sandbox")
    if platform.system() != 'Windows':
        options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("detach", True)

    
    tries = 5
    for attempt in range(tries):
        if attempt != 0:
            print(f"Rechecking: {attempt}")
            writeLine(f"Rechecking: {attempt}")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        try:
            res = await run_check(where, when, driver)
            print(f"[{logTime}] {res}")
            writeLine(f"[{logTime}] {res}")
            return res
        except:
            driver.quit()
            if attempt == tries - 1:
                return f"Failed, Check timestamp: {logTime}"