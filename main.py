from src.head_hunter import JSONSaver, HeadHunterAPI
from src.superjob import SuperJobAPI, JSONSaverSJ
from src.utils import sort_by_salary_min, sort_by_salary_max

print(
    "Greetings, Sir! I am Jarvis, your trusted job search assistant for today. Let's work together to find you the perfect job opportunity!")
job = input("Sir, Could you kindly specify the type of job you are interested in? \n-->")
platform = input("Sir, currently I have access to two job search platforms: HeadHunter and SuperJob.\n"
                 "Which platform would you like me to search on? \n1-HeadHunter\n2-SuperJob\n(Type only number)-->")
if platform == '1':
    page = input(
        "Sir, how many pages would you like me to display job vacancies? Vacancies per page 100.\n(Type only number up to 10)-->")
    max_min = input("Sir, would you like me to display job vacancies in order of increasing salaries or decreasing "
                    "salaries? Please let me know your preference.\n1-->Increasing\n2-->Decreasing\n(Type only number)-->")

    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(job, page)
    json_saver = JSONSaver(job)
    json_saver.add_vacancies(hh_vacancies)
    data = json_saver.select()
    if max_min == '1':
        data = sort_by_salary_max(data)
    else:
        data = sort_by_salary_min(data)
    a = 0
    for row in data:
        a += 1
        print(a)
        print(row, end=f"\n{'=' * 150}\n")
else:

    page_sj = input(
        "Sir, how many pages would you like me to display job vacancies? Vacancies per page 100.\n(Type only number up to 5)-->")
    max_min = input("Sir, would you like me to display job vacancies in order of increasing salaries or decreasing "
                    "salaries? Please let me know your preference.\n1-->Increasing\n2-->Decreasing\n(Type only number)-->")

    sj_api = SuperJobAPI()
    sj_vacancies = sj_api.get_vacancies(job, page_sj)

    json_saver_sj = JSONSaverSJ(job)
    json_saver_sj.add_vacancies(sj_vacancies)
    data_sj = json_saver_sj.select()
    if max_min == '1':
        data_sj = sort_by_salary_max(data_sj)
    else:
        data_sj = sort_by_salary_min(data_sj)
    a = 0
    for row in data_sj:
        a += 1
        print(a)
        print(row, end=f"\n{'=' * 150}\n")
