import csv
import json
import dotenv
import os


dotenv.load_dotenv('.env')
df_path=os.getenv('DF_PATH')



def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []


    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)


        for row in csvReader:

            jsonArray.append(row)


    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


csvFilePath = fr'{df_path}'
jsonFilePath = r'user_info.json'
csv_to_json(csvFilePath, jsonFilePath)