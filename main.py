import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8"
}
input_text = input("Could you kindly specify the type of job you are interested in? \n -->")
query = {"text": f"{input_text}",
         "area": "1"

         }

# row_data = requests.get('https://httpbin.org/get', headers=headers)
row_data = requests.get('https://hh.ru/search/vacancy', headers=headers , params=query)

print(row_data.text)
#print(row_data.headers)
#print(row_data.content)
