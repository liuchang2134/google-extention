from django.shortcuts import render


def scrape_experience(linkedin_url):
    context = {}
    context['hello'] = "Hello World"
    context['name'] = ""
    context['about'] = ""
    context['experience'] = []
    import time

    from bs4 import BeautifulSoup
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium import webdriver

    driver = webdriver.Chrome("../chromedriver")

    email = "cr7rex1@gmail.com"
    password = "990528Qs"
    driver.get("https://www.linkedin.com/login")

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    email_elem = driver.find_element_by_id("username")
    email_elem.send_keys(email)

    password_elem = driver.find_element_by_id("password")
    password_elem.send_keys(password)
    password_elem.submit()

    def is_signed_in():
        try:
            driver.find_element_by_id("global-nav-search")
            return True
        except:
            pass
        return False

    if is_signed_in():
        driver.get(linkedin_url)
    else:
        print("you are not logged in!")
        x = input("please verify the capcha then press any key to continue...")
        driver.get(linkedin_url)

    root = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "pv-top-card",
            )
        )
    )
    name = root.find_element_by_class_name('text-heading-xlarge').text.strip()
    context['name'] = name
    try:
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        sections = soup.find_all("h2", {"class": "pvs-header__title text-heading-large"})
        links = soup.find_all("a", {
            'class': 'optional-action-target-wrapper artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--muted inline-flex justify-center full-width align-items-center artdeco-button--fluid'})
        titles = soup.find_all("span", {"class": "mr1 t-bold"})
        for i in sections:
            if 'About' in i.find("span", {"class": "visually-hidden"}).get_text().strip():
                about = soup.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
                context['about'] = about
            elif "Experience" in i.find("span", {"class": "visually-hidden"}).get_text().strip():
                if links is not None:
                    for j in links:
                        if 'experience' in j.get_attribute_list('href')[0]:
                            driver.get(j.get_attribute_list('href')[0])
                            time.sleep(2)
                            soup_experience = BeautifulSoup(driver.page_source, 'html.parser')
                            title = soup_experience.find_all('span', {'class': 'mr1 t-bold'})
                            company = soup_experience.find_all('span', {'class': 't-14 t-normal'})
                            time = soup_experience.find_all('span', {'class': 't-14 t-normal t-black--light'})
                            for k, l, m in zip(title, company, time):
                                context['experience'].append(
                                    k.find("span", {"class": "visually-hidden"}).get_text().strip() +
                                    l.find("span", {"class": "visually-hidden"}).get_text().strip() +
                                    m.find("span", {"class": "visually-hidden"}).get_text().strip())

                else:
                    for j in titles:
                        print(j.find("span", {"class": "visually-hidden"}).get_text().strip())

            elif "Skills" in i.find("span", {"class": "visually-hidden"}).get_text().strip():
                print('Skills')
                if links is not None:
                    for j in links:
                        if 'skills' in j.get_attribute_list('href')[0]:
                            skills_page = j.get_attribute_list('href')[0]
                            driver.get(skills_page)
                            time.sleep(2)
                            soup_skills = BeautifulSoup(driver.page_source, 'html.parser')
                            skill = soup_skills.find('section', {'class': 'artdeco-card ember-view pb3'}).find_all(
                                'span', {'class': 'mr1 t-bold'})
                            for k in skill:
                                print(k.find("span", {"class": "visually-hidden"}).get_text().strip())

                else:
                    for j in titles:
                        print(j.find("span", {"class": "visually-hidden"}).get_text().strip())
            time.sleep(4)
    except:
        print("Error")
    driver.quit()
    return context
