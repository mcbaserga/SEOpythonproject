from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

def crawl_and_extract(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tags = [h1.text for h1 in soup.find_all('h1')]
        
        meta_title = soup.find('title').text
        
        meta_description = soup.find('meta', attrs={'name': 'description'})['content']
        
        paragraphs = soup.find_all('p')
        paragraph_text = ' '.join([p.text for p in paragraphs])
        word_count = len(paragraph_text.split())

        return {
            'H1 Tags': h1_tags,
            'Meta Title': meta_title,
            'Meta Description': meta_description,
            'Word Count': word_count,
        }
    except Exception as e:
        return {'error': str(e)}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        data = crawl_and_extract(url) 
        return render_template('index.html', data=data)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)


