from bs4 import BeautifulSoup
from typing import Dict, Any


def get_tournament_info_bs4(html_source: str) -> Dict[str, Any]:
    """
    Извлекает название турнира и дату, находя третий элемент в списке.

    Args:
        html_source: HTML-код страницы в виде строки.

    Returns:
        Словарь с данными о турнире.
    """
    info = {}
    soup = BeautifulSoup(html_source, 'html.parser')

    # Извлечение названия турнира
    try:
        # Находим все элементы-пути
        breadcrumb_items = soup.select('li[itemprop="itemListElement"]')

        # Выбираем третий элемент (индекс 2)
        if len(breadcrumb_items) >= 3:
            third_element = breadcrumb_items[2]

            # Находим span внутри третьего элемента, который содержит название
            tournament_name_element = third_element.select_one('span[itemprop="name"]')

            if tournament_name_element:
                full_name = tournament_name_element.get_text(strip=True)
                if ' - ' in full_name:
                    base_name = full_name.split(' - ')[0]
                else:
                    base_name = full_name
                info['tournament_name'] = base_name
            else:
                info['tournament_name'] = None
        else:
            info['tournament_name'] = None
            print("На странице нет третьего элемента-хлебной крошки.")
    except Exception as e:
        info['tournament_name'] = None
        print(f"Ошибка при поиске названия турнира: {e}")

    # Извлечение только даты
    try:
        date_element = soup.select_one('div.duelParticipant__startTime > div')
        if date_element:
            full_date = date_element.get_text(strip=True).split(' ')[0]
            info['tournament_date'] = full_date
        else:
            info['tournament_date'] = None
    except Exception as e:
        info['tournament_date'] = None
        print(f"Ошибка при поиске даты турнира: {e}")

    return info