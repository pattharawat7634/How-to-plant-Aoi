import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings (use only for testing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_ocsb_faq():
    url = 'https://www.ocsb.go.th/faq'
    response = requests.get(url, verify=False)  # Disable SSL verification
    soup = BeautifulSoup(response.content, 'html.parser')

    faq_items = soup.find_all('div', class_='accordion-item')
    faqs = []

    for i, item in enumerate(faq_items, 1):
        question = item.find('button', class_='accordion-button').text.strip()
        answer = item.find('div', class_='accordion-body').text.strip()
        faq_dict = {
            'id': i,
            'question': question,
            'answer': answer
        }
        faqs.append(faq_dict)

    return faqs

if __name__ == "__main__":
    try:
        faq_data = scrape_ocsb_faq()
        for faq in faq_data:
            print(f"FAQ Item {faq['id']}:")
            print(f"Question: {faq['question']}")
            print(f"Answer: {faq['answer']}")
            print("-" * 50)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")