from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import traceback
from selenium.webdriver.support.ui import Select
import time

def fetch_exchange_rate(date, currency_code):
    # 初始化库
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    print('日期为', formatted_date)

    try:
        driver.get("https://www.boc.cn/sourcedb/whpj/")
        # 等待日期输入框加载
        wait.until(EC.visibility_of_element_located((By.NAME, "erectDate"))) 
        date_input = driver.find_element(By.NAME, "erectDate") #初始
        date_input.clear()
        date_input.send_keys(formatted_date)

        nothing_input = driver.find_element(By.NAME, "nothing")#结束
        nothing_input.clear()
        nothing_input.send_keys(formatted_date)

        # 定位下拉框，并选择对应的货币
        select_element = wait.until(EC.presence_of_element_located((By.NAME, "pjname")))
        select = Select(select_element)

        # 货币代码到货币名称的映射
        currency_map = {
            'USD': '美元', 
            'EUR': '欧元',
            'GBP': '英镑',
            'HKD': '港币',
            'CHF': '瑞士法郎',
            'DEM': '德国马克', 
            'FRF': '法国法郎', 
            'SGD': '新加坡元',
            'SEK': '瑞典克朗',
            'DKK': '丹麦克朗',
            'NOK': '挪威克朗',
            'JPY': '日元',
            'CAD': '加拿大元',
            'AUD': '澳大利亚元',
            'MOP': '澳门元',
            'PHP': '菲律宾比索',
            'THB': '泰国铢',
            'NZD': '新西兰元',
            'KRW': '韩元',
            'RUB': '卢布',
            'MYR': '林吉特',
            'TWD': '新台币',
            'ESP': '西班牙比塞塔',  
            'ITL': '意大利里拉',
            'NLG': '荷兰盾',  
            'BEF': '比利时法郎',
            'FIM': '芬兰马克',  
            'INR': '印度卢比',
            'IDR': '印尼卢比',
            'BRL': '巴西里亚尔',
            'AED': '阿联酋迪拉姆',
            'ZAR': '南非兰特',
            'SAR': '沙特里亚尔',
            'TRY': '土耳其里拉',
        }
        # 规范化名称
        currency_name = currency_map.get(currency_code.upper())
        print(currency_name)
        if currency_name is None:
            print(f"未找到货币代号{currency_code}对应的名称。")
            return

        # 选择货币
        select.select_by_visible_text(currency_name)

        # 搜索
        driver.execute_script("executeSearch();")
        #确保加载完成
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "list_navigator")))
        
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/table/tbody/tr[2]")))
        rates_table = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/table")
        rows = rates_table.find_elements(By.TAG_NAME, "tr")

        for row in rows[1:]:  # 跳过表头
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                currency_name = cols[0].text.strip()
                print('scraping currency is ' ,currency_name)
                result = cols[3].text.strip()  # 现汇卖出价在第四列
                with open("result.txt", "w") as file:
                    file.write(result)
                print(result)
                break
    except Exception as e:
        print(f"发生错误：{e}")
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("方法: python3 yourcode.py date currency_code")
    else:
        date = sys.argv[1]
        currency_code = sys.argv[2]

        fetch_exchange_rate(date, currency_code)
