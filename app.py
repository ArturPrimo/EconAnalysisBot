import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import vertexai
from vertexai.generative_models import GenerativeModel
import credentials
import database

xpath_finance_tab = '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/nav/div[1]/ul/li[4]/a'
xpath_finance_title = '//*[@id="leftColumn"]/div[7]'
xpath_finance_stats = '//*[@id="rsdiv"]/div'

xpath_demo_tab = '//*[@id="pairSublinksLevel2"]/li[2]/a'
xpath_demo_title = '//*[@id="leftColumn"]/div[7]'
xpath_demo_stats = '//*[@id="rrtable"]'

xpath_balancep_tab = '//*[@id="pairSublinksLevel2"]/li[3]/a'
xpath_balancep_title = '//*[@id="leftColumn"]/div[7]'
xpath_balancep_stats = '//*[@id="rrtable"]'

xpath_cashflow_tab = '//*[@id="pairSublinksLevel2"]/li[4]/a'
xpath_cashflow_title = '//*[@id="leftColumn"]/div[7]'
xpath_cashflow_stats = '//*[@id="rrtable"]'

xpath_indicator_tab = '//*[@id="pairSublinksLevel2"]/li[5]/a'
xpath_indicator_title = '//*[@id="leftColumn"]/div[7]'
xpath_indicator_stats = '//*[@id="rrTable"]'

xpath_dividend_tab = '//*[@id="pairSublinksLevel2"]/li[6]/a'
xpath_dividend_title = '//*[@id="leftColumn"]/div[7]'
xpath_dividend_stats = '//*[@id="dividendsHistoryData18604"]'

xpath_balance_tab = '//*[@id="pairSublinksLevel2"]/li[7]/a'
xpath_balance_title = '//*[@id="leftColumn"]/div[7]'
xpath_balance_stats = '//*[@id="earningsHistory18604"]'

xpaths2 = [
    {'name': 'Finanças', 'title': xpath_finance_title, 'stats': xpath_finance_stats},
    {'name': 'Balanços', 'title': xpath_balance_title, 'stats': xpath_balance_stats}
]

xpaths = [
    {'name': 'Finanças', 'title': xpath_finance_title, 'stats': xpath_finance_stats},
    {'name': 'Demonstrações', 'title': xpath_demo_title, 'stats': xpath_demo_stats},
    {'name': 'Balanço Patrimonial', 'title': xpath_balancep_title, 'stats': xpath_balancep_stats},
    {'name': 'Fluxo de Caixa', 'title': xpath_cashflow_title, 'stats': xpath_cashflow_stats},
    {'name': 'Indicadores', 'title': xpath_indicator_title, 'stats': xpath_indicator_stats},
    {'name': 'Dividendos', 'title': xpath_dividend_title, 'stats': xpath_dividend_stats},
    {'name': 'Balanços', 'title': xpath_balance_title, 'stats': xpath_balance_stats}
]



def click_element_by_xpath(driver, xpath, max_attempts=3):
    attempts = 0
    while (attempts < max_attempts):
        try:
            #tab = driver.find_element(By.XPATH, xpath)
            #tab.click()
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.mouseclick()
            break
        except:
            attempts += 1
            time.sleep(5)

def click_element_by_link(driver, link_text, max_attempts=3):
    attempt = 0
    while attempt < max_attempts:
        try:
            print(f"Trying to Click on {link_text} By Link")
            link = driver.find_element(By.LINK_TEXT, link_text)
            # Click the link
            link.click()
            print("Element found and clicked.")
            break
        except:
            close_button_xpath = '//*[@id="PromoteSignUpPopUp"]/div[2]/i'
            attempt += 1
            print(f"Attempt {attempt}: Element not found on the page.")
            driver.execute_script("window.scrollBy(0, 300);")
            click_element_by_xpath(driver, close_button_xpath)
            if attempt == max_attempts:
                print("Maximum attempts reached. Quitting.")
                break
            time.sleep(2)  # Wait for 2 seconds before the next attempt


def get_information(driver, name, xpath_title, xpath_stats):
    click_element_by_link(driver, name)
    print("extracting...")
    title = driver.find_element(By.XPATH, xpath_title)
    stats = driver.find_elements(By.XPATH, xpath_stats)
    texts = [element.text for element in stats]
    concatenated_string = "\n".join(texts)
    return title.text, concatenated_string
    

def main(url):
    data = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    for item in xpaths:
        print(item['name'])
        data.append(get_information(driver, item['name'], item['title'], item['stats']))
    print(data)
    driver.quit()
    return data

def initialize_model_1_5():
    project_id = os.environ["PROJECT_ID"]
    vertexai.init(project=project_id, location="us-central1")
    return GenerativeModel(model_name="gemini-1.5-flash-001")

def call_llm_1_5(prompt: str):
    """Useful to call an LLM model"""
    model = initialize_model_1_5()
    response = model.generate_content(prompt)
    answer = response.candidates[0].content.parts[0]._raw_part.text
    return answer


# Convert the dictionary into a pandas DataFrame
df = pd.DataFrame(database.companies)

st.title('Company Analysis Dashboard')

# Dropdown menu for company selection
company = st.selectbox('Select a company:', df['company'])

# Filter the DataFrame based on the selected company
company_data = df[df['company'] == company]


if st.button("Execute Analysis with Gemini 1.5 LLM"):
    with st.spinner("Analyzing..."):
        if not company_data.empty:
            result = main(company_data['url'].values[0])
            st.write(f"**Company:** {company_data['company'].values[0]}")
            st.write(f"**URL:** {company_data['url'].values[0]}")
            prompt = f"""Voce e um analista de investimentos. O seu trabalho e decidir se e uma boa hora para investir na empresa.
            Faca a analise de acordo com os dados abaixo:
            {result}
            """
            answer = call_llm_1_5(prompt)
            st.write(answer)

        else:
            st.write("No data available for the selected company.")
