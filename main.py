from src.classes_for_hh_and_spjob import HeadHunterAPI
from src.head_hunter import JSONSaver
from src.utils import sort_by_salary_min, sort_by_salary_max

# keyword = input("Could you kindly specify the type of job you are interested in? \n -->")
keyword = "Python"
hh_api = HeadHunterAPI()
hh_vacancies = hh_api.get_vacancies(keyword)

json_saver = JSONSaver(keyword)
json_saver.add_vacancies(hh_vacancies)
data = json_saver.select()
#data = sort_by_salary_min(data)
data = sort_by_salary_max(data)
for row in data:
    print(row, end=f"\n{'=' * 150}\n")
# json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
# json_saver.delete_vacancy(vacancy)
