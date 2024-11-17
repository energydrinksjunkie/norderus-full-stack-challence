import requests

def fetch_and_parse_grid():
    url = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"
    response = requests.get(url)
    raw_data = response.text.strip()
    
    grid = [
        list(map(int, row.split()))
        for row in raw_data.split('\n')
    ]
    return grid