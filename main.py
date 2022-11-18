from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#requirements :
#pip install selelnium
#pip install 

class Bot:

    def __init__(self, url):
        self.url = url

    def main(self):
        logins, results = self.storeData()
        for i in range(int(len(logins)/2)):
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            self.driver.get(self.url)
            print("Logowanie do konta: {}...\n".format(logins[i*2]))
            self.acceptCookies()
            self.loginSession(logins[(2*i)], logins[(2*i)+1])
            print("Logowanie zakończone.\n")
            try:
                self.insertData(results)
                self.finalSubmit()
                print("Dane wprowadzone.\n")
            except Exception:
                print("\nBłąd wprowadzania.")

    def acceptCookies(self):
        cookies = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "accept-cookies-checkbox"))
        )
        cookies.click()

    def loginSession(self, login, password):
        loginInput = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "id_login"))
        )
        loginInput.send_keys(login)

        passwordInput = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "id_password"))
        )
        passwordInput.send_keys(password)

        submissionBox = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        submissionBox.click()

    #method that gets data from text files and return it as array
    def storeData(self):
        loginData = []
        resultsData = []
        with open("loginy.txt", "r") as f1:
            for row in f1:
                loginData.append(row.rstrip())

        with open("wyniki.txt", "r") as f2:
            for row in f2:
                resultsData.append(row.rstrip())
        
        return loginData, resultsData

    #method inserting collected results to fields on the page
    def insertData(self, results):

        #set the time for running the session
        try:
            WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//input[starts-with (@name,'openAnswer')]"))
            )
            print("Wprowadzam odpowiedzi...\n")
        except Exception:
            print("Nie znaleziono testu.")   

        answerField =  self.driver.find_elements(By.XPATH, "//input[starts-with (@name,'openAnswer')]")
        for i in range(len(answerField)):
            answerField[i].send_keys(results[i])

    #method submiting the process
    def finalSubmit(self):
        #input("\nSubmit:")
        WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "submitContest"))
        ).click()
        WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "modalOkButton"))
        ).click()




if __name__ == "__main__":
    konkurs = Bot("https://infimat.p.lodz.pl/userContests/sheet/904/solve")
    konkurs.main()