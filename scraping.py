import time

import chromedriver_binary  # noqa
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from tqdm import tqdm

from table import facultyID2name, termID2year

HOME_URL = "http://syllabus01.academic.hokudai.ac.jp/Syllabi/Public/Syllabus/SylSearch.aspx"
RESULT_URL = "http://syllabus01.academic.hokudai.ac.jp/Syllabi/Public/Syllabus/SylList.aspx"


class ScheduleScraping:
    def __init__(self, termID, facultyID):
        self.termID = termID
        self.facultyID = facultyID
        self.errors = []

    def toResultPage(self):
        # 00 -> 全学教育
        self.driver.get(HOME_URL)
        time.sleep(1)

        # 期間 学士課程 学部 授業科目・担当教員別
        idList = [
            "ctl00_phContents_ucSylSearchuc_ddl_year",
            "ctl00_phContents_ucSylSearchuc_ddl_org",
            "ctl00_phContents_ucSylSearchuc_ddl_fac",
            "ctl00_phContents_ucSylSearchuc_ddl_open",
        ]
        valueList = [
            termID2year[self.termID][0],
            "02",
            self.facultyID,
            termID2year[self.termID][1],
        ]

        for selectID, value in zip(idList, valueList):
            dropdown = self.driver.find_element_by_id(selectID)
            select = Select(dropdown)
            select.select_by_value(value)
            time.sleep(1)

        btn = self.driver.find_element_by_id("ctl00_phContents_ucSylSearchuc_ctl109_btnSearch")
        btn.click()  # submit
        time.sleep(1)

        # 表示件数を全てにする
        dropdown = self.driver.find_element_by_id("ctl00_phContents_ucSylList_DDLLine_ddl")
        select = Select(dropdown)
        select.select_by_index(0)
        time.sleep(1)

    def getItems(self):

        assert self.driver.current_url == RESULT_URL

        trs = self.driver.find_elements_by_xpath(
            '//*[@id="ctl00_phContents_ucSylList_gv"]/tbody/tr'
        )
        trs = trs[1:]  # トップの余分な情報を捨てる

        for tr in tqdm(trs):
            item = dict()
            tds = tr.find_elements_by_tag_name("td")

            item["courseTitle"] = tds[2].text
            item["teacher"] = tds[3].text
            item["year"] = termID2year[self.termID][0]
            item["semester"] = termID2year[self.termID][1] + "学期"
            item["faculty"] = facultyID2name[self.facultyID]
            dayOfWeek = tds[4].text.split("\n")
            item["scheduleByJap"] = dayOfWeek[0]
            item["scheduleByEn"] = dayOfWeek[1]
            item["yearOfEligible"] = tds[5].text

            yield item

    def _close(self):
        # ブラウザーを終了
        self.driver.quit()

    def _open(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)  # seconds

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._close()
