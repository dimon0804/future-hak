import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from django.utils import timezone
import pytz
from dashboard.models import Post
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException


def parse_news():
    new_posts = []
    
    def setup_chrome():
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        return chrome_options
    # Парсинг первого источника: rscf.ru
    def parse_rscf():
        url = "https://rscf.ru/news/"
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='news-item')

        try:
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')
            except:
                pass

        for card in cards:
            try:
                title = card.find('a', class_='news-title').text.strip()
                if Post.objects.filter(title=title).exists():
                    continue

                content = card.find('div', class_='news-desc').text.strip()
                raw_date = card.find('div', class_='news-date').text.strip()
                category_ru = card.find('a', class_='news-category').text.split()[0].strip().lower()
                
                img_tag = card.find('img')
                image_url = 'https://rscf.ru' + img_tag['src'] if img_tag and img_tag.get('src') else ''

                try:
                    date_obj = datetime.strptime(raw_date, '%d %B, %Y')
                except:
                    month_mapping = {
                        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
                        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
                        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
                    }
                    day, month_ru, year = raw_date.replace(',', '').split()
                    month = month_mapping.get(month_ru.lower(), 1)
                    date_obj = datetime(int(year), month, int(day))

                date_obj = timezone.make_aware(date_obj, timezone=pytz.UTC)

                post = Post(
                    title=title,
                    author_id=1,
                    category=_map_category(category_ru),
                    status='published',
                    content=content,
                    created_at=date_obj,
                    image=image_url,
                    tags='РНФ'
                )
                post.save()
                new_posts.append(post)

            except Exception as e:
                print(f"Ошибка в rscf: {str(e)}")
                continue

    # Парсинг второго источника: наука.рф
    def parse_elibrary():
        try:
            # Инициализация драйвера
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=setup_chrome())
            
            # Загрузка страницы
            driver.get("https://elibrary.ru/news_library.asp")
            
            try:
                # Ожидание загрузки контента
                WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "td[colspan='3'][valign='top']"))
                )
            except TimeoutException:
                print("Ошибка: элементы не найдены после 25 секунд ожидания")
                return

            # Парсинг контента
            soup = BeautifulSoup(driver.page_source, 'lxml')
            news_items = soup.select('td[colspan="3"][valign="top"]:has(font[color="#f16b51"])')
            
            for item in news_items[:3]:  # Ограничение для теста
                try:
                    # Извлечение данных
                    date_tag = item.find('font', color="#f16b51")
                    raw_date = date_tag.get_text(strip=True) if date_tag else ''
                    date_obj = datetime.strptime(raw_date, '%d.%m.%Y')
                    date_obj = timezone.make_aware(date_obj, timezone=pytz.UTC)

                    title_tag = item.find('a', href=True)
                    title = title_tag.get_text(strip=True) if title_tag else ''
                    
                    if not title or Post.objects.filter(title=title).exists():
                        continue

                    # Формирование URL
                    article_url = urljoin('https://elibrary.ru/', title_tag['href'])

                    # Извлечение контента
                    content_div = item.find('div', style=lambda s: 'margin:5px 0 0 30px' in str(s))
                    content = content_div.get_text('\n', strip=True) if content_div else ''

                    # Создание и сохранение поста
                    post = Post(
                        title=title,
                        author_id=1,
                        category='academia',
                        status='published',
                        content=content,
                        created_at=date_obj,
                        # url=article_url,
                        tags='eLibrary'
                    )
                    post.save()
                    new_posts.append(post)

                except Exception as e:
                    print(f"Ошибка обработки элемента: {str(e)}")
                    continue

        except WebDriverException as e:
            print(f"Критическая ошибка WebDriver: {str(e)}")
        except Exception as e:
            print(f"Общая ошибка: {str(e)}")
        finally:
            if 'driver' in locals():
                driver.quit()

    def parse_science_news():
        url = "https://www.sciencenews.org/all-stories"
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('li[class*="post-item-river__wrapper"]')
        new_posts = []

        for article in articles:
            try:
                # Extract title and URL
                title_tag = article.select_one('h3[class*="post-item-river__title"] a')
                if not title_tag:
                    continue
                    
                title = title_tag.get_text(strip=True)
                if Post.objects.filter(title=title).exists():
                    continue

                article_url = title_tag['href']

                # Extract category
                category_tag = article.select_one('a[class*="post-item-river__eyebrow"]')
                category = category_tag.get_text(strip=True) if category_tag else "General"

                # Extract date
                date_tag = article.select_one('time')
                date_str = date_tag['datetime'] if date_tag else ''
                try:
                    date_obj = datetime.fromisoformat(date_str)
                    date_obj = timezone.make_aware(date_obj)
                except:
                    date_obj = timezone.now()

                # Extract summary
                summary_tag = article.select_one('p[class*="post-item-river__excerpt"]')
                summary = summary_tag.get_text(strip=True) if summary_tag else ''

                # Extract image
                img_tag = article.select_one('img')
                image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''

                # Create post
                post = Post(
                    title=title,
                    author_id=1,  # Укажите нужный ID автора
                    category=_map_category(category),
                    status='published',
                    content=summary,
                    created_at=date_obj,
                    image=image_url,
                    tags='Science News',
                    # url=article_url
                )
                post.save()
                new_posts.append(post)

            except Exception as e:
                print(f"Ошибка обработки статьи: {str(e)}")
                continue

    # Вызываем оба парсера
    parse_rscf()
    parse_elibrary()
    parse_science_news()
    
    return new_posts

def _map_category(ru_category: str) -> str:
    category_mapping = {
        'химия': 'chemistry',
        'физика': 'physics',
        'биология': 'biology',
        'космос': 'space',
        'технологии': 'technology',
        'Health & Medicine': 'health',
        'Здоровье и медицина': 'health',
        'Life': 'biology',
        'Space': 'space',
        'Physics': 'physics',
    }
    return category_mapping.get(ru_category, 'technology')