# Selenium

## Installation

Selenium Python 绑定提供一个简单的 API 来访问 Selenium WebDriver。

安装 Selenium Python 绑定：

```
pip install selenium
```

Selenium 需要一个 driver 来访问特定 OS 特定的浏览器的 Driver。

## Getting Started

```py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
```

selenium.webdriver 模块提供所有 WebDriver 实现，当前支持 Firefox，Chrome，IE 和 Remote。

Keys 类提供 keyboard 按键，By 类用于定位 document 中的元素。

driver = webdriver.Firefox() 创建了一个 WebDriver 实例，作为所有操作的入口。

driver.get 方法导航到给定的 URL，即在浏览器中打开给定的 URL。WebDriver 将会等待直到页面完全载入（即 onload 事件发射）。但是如果页面中在 onload 之后使用了 AJAX，WebDriver 不能得知页面何时加载完。

WebDriver 使用 find_element 提供了大量方法来查找元素。例如，input text 元素可以使用 find_element 和 By.NAME 通过它的名字来查找。

sending keys 类似使用 keyboard 输入 keys。特殊的键（控制键）可以通过 selenium.webdriver.common.keys 中的 Keys 来发送。

elem.clear() 清空文本框中预置的文本。

页面提交之后，就可以通过 driver.page_source 得到结果（如果有的话）。

driver.close() 关闭浏览器窗口。还可以调用 quit 方法而不是 close 方法。quit 方法会退出浏览器，而 close 只关闭一个 tab 页。

Selenium 操作的两个主要对象：WebDriver 实例和文档元素。WebDriver 通过 url 得到文档，然后从文档中找到元素，在元素上调用方法来操作它。

## Navigating

使用 WebDriver 第一件事就是导航到一个链接。通常方法是调用 get 方法：

driver.get("http://www.google.com")

### 和页面交互

只得到页面没有太多用处，通常我们想和页面中的元素交互。首先，需要定位到元素：

```html
<input type="text" name="passwd" id="passwd-id" />
```

```py
element = driver.find_element(By.ID, "passwd-id")
element = driver.find_element(By.NAME, "passwd")
element = driver.find_element(By.XPATH, "//input[@id='passwd-id']")
element = driver.find_element(By.CSS_SELECTOR, "input#passwd-id")
```

还可以通过链接的文本来查找一个 link，但是文本必须严格匹配。若使用 XPATH 且有多个元素匹配 query，只会返回第一个元素。

如果找不到元素，抛出 NoSuchElementException。

WebDriver 有一个 Object-based API，使用相同的接口表示所有类型的元素。这意味着尽管 API 有很多方法，但是不是所有方法对所有类型的元素都有意义。WebDriver 会尽量做正确的事，如果在一个元素上调用的方法没有意义，会抛出异常。

得到元素后，就可以与它交互。例如，得到一个文本框，可以想其中输入字符：

element.send_keys("some text")

特殊的控制键可以通过 Keys 类来发送：

element.send_keys(" and some", Keys.ARROW_DOWN)

可以对任何元素调用 send_keys，这可以测试快捷键，例如 Gmail。这样输入不会清空文本框现有内容，只会在后面追加字符。可以调用 element.clear() 来显式清楚文本框的内容。

### Filling in forms

除了输入文本框，还可以操作其他类型的 form 空间，例如 drop down list。

```py
element = driver.find_element(By.XPATH, "//select[@name='name']")
all_options = element.find_elements(By.TAG_NAME, "option")
for option in all_options:
    print("Value is: %s" % option.get_attribute("value"))
    option.click()
```

这会先查找第一个 SELECT 元素，然后循环它的每个 OPTION，打印它们的 values，然后依次选择。

这不是处理 SELECT 元素最有效的方法。WebDriver 提供一个 Select 类，它包含处理 OPTION 很多高效的方法：

```py
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.NAME, 'name'))
select.select_by_index(index)
select.select_by_visible_text("text")
select.select_by_value(value)
select.deselect_all()
all_selected_options = select.all_selected_options
options = select.options
```

填完表单后，可以提交它。一个方法是，直到 submit 按钮并点击它：

```py
driver.find_element(By.ID, "submit").click()
```

此外，WebDriver 还在每个元素上提供了 submit 方法。如果在 form 内的一个元素上调用这个方法，WebDriver 将会遍历 DOM 直到它找到外围的 form 元素，然后再它上面调用 submit。如果元素不在 form 中，则会抛出 NoSuchElementException。

```py
element.submit()
```

### Drag and drop

可以拖放元素，移动特定距离，或放在另一个元素上。

```py
element = driver.find_element(By.NAME, "source")
target = driver.find_element(By.NAME, "target")

from selenium.webdriver import ActionChains
action_chains = ActionChains(driver)
action_chains.drag_and_drop(element, target).perform()
```

### 在 windows 和 frames 之间移动

现代 web 应用可能会有多个 frame 或多个 window。

WebDriver 通过 switch_to.window 方法在命名的 names 之间移动。

driver.switch_to.window("windowName")

现在对 driver 的所有调用都被解释为针对这个新的 window。

```html
<a href="somewhere.html" target="windowName">Click here to open a new window</a>
```

或者，可以传递一个 window handle 到 switch_to.window() 方法。这样，可以依次迭代每个打开的 widnow：

```py
for handle in driver.windows_handers:
    driver.switch_to.window(handle)
```

还可以再 frames 之间切换：

```py
driver.switch_to.frame("frameName")
```

可以通过点号分隔的路径访问 subframes，也可以通过 index：

```py
driver.switch_to.frame("frameName.0.child")
```

这将会进入 frameName 的第一个 subframe 的名为 child 的 subframe。

所有 frame 都表现的就好像它们是 top frame，所有 driver 操作都针对这个 frame。

一旦完成对 frame 的操作，就可以回到 parent frame：

```py
driver.switch_to.default_content()
```

### popup dialogs

selenium webdriver 内置支持处理弹出式对话框。一旦你触发了一个打开 popup 的操作，可以访问这个 alert：

```py
alert = driver.switch_to.alert
```

这回返回当前打开的 alert object。使用这个 object，你可以 accept，dismiss，读取的它的内容，甚至在 prompt 中输入。这个接口对 alert，confirms，prompts 的工作是一样的。

### 导航：history 和 location

通常导航 url 使用 driver.get 方法。WebDriver 还有很多小的，task-focused 接口，而 navigation 是一个很有用的 task。要导航到一个页面，使用 get 方法：

```py
driver.get("http://www.example.com")
```

要在浏览器历史中向前、向后移动：

```py
driver.forward()
driver.back()
```

注意这个功能完全依赖底层 driver，有可能出现意料之外的行为。

### Cookies

要访问 cookies，首先需要在 cookie 所在的 domain：

```py
# Go to the correct domain
driver.get("http://www.example.com")

# Now set the cookie. This one's valid for the entire domain
cookie = {'name' : 'foo', 'value' : 'bar'}
driver.add_cookie(cookie)

# And now output all the available cookies for the current URL
driver.get_cookies()
```

## Locating Elements

Selenium 的两个主要操作对象：driver 实例和页面元素。有各种策略在页面上定位元素。

- find_element
- find_elements

```py
from selenium.webdriver.common.by import By

driver.find_element(By.XPATH, '//button[text()="Some text"]')
driver.find_elements(By.XPATH, '//button')
```

By 策略：

- ID = "id"
- NAME = "name"
- XPATH = "xpath"
- LINK_TEXT = "link text"
- PARTIAL_LINK_TEXT = "partial link text"
- TAG_NAME = "tag name"
- CLASS_NAME = "class name"
- CSS_SELECTOR = "css selector"

```py
find_element(By.ID, "id")
find_element(By.NAME, "name")
find_element(By.XPATH, "xpath")
find_element(By.LINK_TEXT, "link text")
find_element(By.PARTIAL_LINK_TEXT, "partial link text")
find_element(By.TAG_NAME, "tag name")
find_element(By.CLASS_NAME, "class name")
find_element(By.CSS_SELECTOR, "css selector")
```

找不到元素抛出异常 NoSuchElementException。

## Waits

如今绝大多数 web apps 都使用 ajax 技术。页面内的元素可能在页面加载完成后才通过异步的 ajax 加载完成。这会导致定位元素变得困难。这个问题可以通过 waits 解决。

有两种 waits：显式的和隐式的。显式 wait 使 WebDriver 在进一步操作之前等等特定条件。隐式 wait 使 WebDriver 轮询 DOM 特定时间，以尝试定位元素。

### 显式 waits

```py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()
```

这段代码中，Selenium 会等待最多 10s 来查找匹配特定条件的元素的出现。如果在 10s 内指定元素没有出现，抛出 TimeoutException。默认地，WebDriverWait 每 500 毫秒调用 ExpectedCondition，直到它返回成功。ExpectedCondition 成功时返回 true，失败返回 null。

### Expected Conditions

可以显式编写自己的 Expected Conditions，也可以使用常用的 conditions：

- title_is
- title_contains
- presence_of_element_located
- visibility_of_element_located
- visibility_of
- presence_of_all_elements_located
- text_to_be_present_in_element
- text_to_be_present_in_element_value
- frame_to_be_available_and_switch_to_it
- invisibility_of_element_located
- element_to_be_clickable
- staleness_of
- element_to_be_selected
- element_located_to_be_selected
- element_selection_state_to_be
- element_located_selection_state_to_be
- alert_is_present

```py
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
```

自定义 wait conditions：

Custom wait condition can be created using a class with __call__ method which returns False when the condition doesn’t match.

```py
class element_has_css_class(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if self.css_class in element.get_attribute("class"):
        return element
    else:
        return False

# Wait until an element with id='myNewInput' has class 'myCSSClass'
wait = WebDriverWait(driver, 10)
element = wait.until(element_has_css_class((By.ID, 'myNewInput'), "myCSSClass"))
```

## 隐式 Waits

```py
from selenium import webdriver

driver = webdriver.Firefox()
driver.implicitly_wait(10) # seconds
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")
```

## WebDriver API

### WebDriver

- add_cookie()
- add_credential()
- back()
- close()
- create_web_element()
- delete_all_cookies()
- delete_cookie()
- delete_downloadable_files()
- download_file()
- execute()

  发送一个被 command.CommandExecutor 执行的命令。

- execute_async_script()/execute_script()

  在当前 widnow/frame 中执行一段 javascript 代码。

- find_element()/find_elements()
- forward()
- fullscreen_window()
- get()
- get_cookie()
- get_cookies()
- get_credentials()
- get_downloadable_files()
- get_log()
- get_pinned_scripts()
- get_screenshot_as_base64()
- get_screenshot_as_file()
- get_screenshot_as_png()
- get_window_position()
- get_window_rect()
- get_window_size()
- implicitly_wait()
- maximize_window()
- minimize_window()
- pin_script() 存储一些常用的 javascript 代码，稍后通过一个 ID 执行
- print_page()
- quit()
- refresh()
- remove_all_credentials()
- remove_credential()
- remove_virtual_authenticator()
- save_screenshot()
- set_page_load_time()
- set_user_verified()
- set_window_position()
- set_window_rect()
- set_window_size()
- start_client()
- start_session()
- stop_client()
- unpin() 从存储中移除一个 pinned 的 script
- capabilities
- current_url
- current_window_handle
- file_detector
- log_types
- mobile
- name
- orientation
- page_source 当前页面的 source（html）
- switch_to
- timeouts
- title
- window_handles

### WebElement

- clear()
- click()
- find_element()/find_elements()
- get_attribute()
- get_dom_attribute()
- get_property()
- is_displayed()
- is_enabled()
- is_selected()
- screenshot()
- send_keys()
- submit()
- value_of_css_property()
- accessible_name
- id
- location
- parent
- rect
- screenshot_as_base64
- screenshot_as_png
- size
- tag_name
- text

### Action Chains

ActionChains 是一个自动化底层交互的方法，例如鼠标移动，鼠标按钮操作，按键，上下文菜单交互。这用于更复杂的操作，例如 hover over 或拖放。

- click(on_element: WebElement | None = none) => ActionChains

  点击一个元素。on_element 是要被点击的元素，如果为 None，点击当前鼠标所在的位置。
- click_and_hold()
- context_click()
- double_click()
- drag_and_drop()
- drag_and_drop_by_offset()
- key_down()
- key_up()
- move_by_offset()
- move_to_element()
- move_to_element_with_offset()
- pause()
- perform()
- release()
- reset_actions()
- scroll_by_amount()
- scroll_from_origin()
- scroll_to_element()
- send_keys()
- send_keys_to_element()

### Proxy

Proxy 包含 proxy 类型和设置的信息。

为 Driver 设置 proxy：

```py
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=socks5://" + host + ":" + port)
driver = webdriver.Chrome(options);
```
## Alerts

- accept()
- dismiss()
- send_keys()
- text

## Expected conditions

- T
- alert_is_present()
- all_of()
- any_of()
- element_attribute_to_include()
- element_located_selection_state_to_be()
- element_located_to_be_selected()
- element_selection_state_to_be()
- element_to_be_clickable()
- element_to_be_selected()
- frame_t_be_available_and_switch_to_it()
- invisibility_of_element()
- invisibility_of_element_located()
- new_window_is_opened()
- none_of()
- number_of_windows_to_be()
- presence_of_all_elements_located()
- presence_of_element_located()
- staleness_of()
- text_to_be_present_in_element()
- text_to_be_present_in_element_attribute()
- text_to_be_present_in_element_value()
- title_contains()
- title_is()
- url_changes()
- url_contains()
- url_matches()
- url_to_be()
- visibility_of()
- visibility_of_all_elements_located()
- visibility_of_any_elements_lcoated()
- visibility_of_element_located()

