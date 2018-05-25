# 用selenium + pyquery爬取京东商品信息
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

# 创建webdriver对象
browser = webdriver.Chrome()
# 创建WebDriverWait对象，等待10秒抛出异常
wait = WebDriverWait(browser,10)

# 初始化
keyword = input('请输入要获取的商品:')
max_page = int(input("请输入要爬取的页数:"))
url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % keyword

# 打开网页
print('请稍后..')
browser.get(url)



# 获取商品
def get_goods(page):
    # 获取网页源代码
    html= browser.page_source

    # 构造pyquery对象
    doc = pq(html)

    # 获取到多个元素则返回一个生成器
    # 获取对象集：pyquery对象(css选择器).items()
    items = doc('#J_goodsList .gl-warp .gl-item').items()

    for num,item in enumerate(items):
        # 组织参数
        good = {
            '商品名称':item('.gl-i-wrap .p-name').text(),
            '售价':item('.gl-i-wrap .p-price').text()
        }
        print('商品%d:'%num ,good)
        save(page,good)


# 翻页
def chaneg_page(page):
    print('正在爬取第',page,'页...')
    try:
        if page > 1:
            # 获取确定按钮
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage span.p-skip > a')))
            # 用js点击下一页按钮
            js1 ="document.querySelector('.pn-next').click()"
            browser.execute_script(js1)

            # time.sleep(3)

        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage .p-num a.curr'), str(page)))
        print('页码校验成功!')

        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#J_goodsList .gl-i-wrap .p-name')))
        print('页面元素加载成功!')

        # 爬取商品信息 传入page是因为里面调用了save(page,good)函数
        get_goods(page)

    except TimeoutException:
        chaneg_page(page)


# 保存商品信息
def save(page,good):
    file_path = './京东商品信息/'+'京东%s信息第%d页.txt' %(keyword, page)
    # 要用a追加 用w会覆盖
    with open(file_path,'a') as f:
        f.write(str(good)+'\n')


if __name__ == '__main__':
    for i in range(1,max_page+1):
        chaneg_page(i)

