import os
os.environ["KAGGLE_CONFIG_DIR"] = ".kaggle"
from kaggle.api.kaggle_api_extended import KaggleApi
from os.path import exists

api = KaggleApi()
api.authenticate()


if not exists("datasets"):
    os.mkdir("datasets")
os.chdir("datasets")
api.dataset_download_file("gpreda/covid-world-vaccination-progress","country_vaccinations.csv")
api.dataset_download_file("imdevskp/corona-virus-report","country_wise_latest.csv")
api.dataset_download_file("tanuprabhu/population-by-country-2020","population_by_country_2020.csv")
