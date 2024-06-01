import pandas as pd
import json


def excel_to_json(file_path):
    df = pd.read_excel(file_path)
    data = []
    headers = df.columns.tolist()

    for index, row in df.iterrows():
        entry = {}
        for header in headers:
            cellData = row[header]
            if "," in str(cellData):
                sub_data = {}
                pairs = [pair.strip() for pair in str(cellData).split(',')]
                for pair in pairs:
                    sub_key, sub_value = pair.split(':')
                    if sub_value:
                        sub_data[sub_key.strip()] = sub_value.strip()
                    else :
                        sub_data[sub_key.strip()] = None
                entry[header] = sub_data
            else:
                entry[header] = row[header]
        data.append(entry)

    return json.dumps(data, indent=4)


if __name__ == '__main__':
    excel_file_path = 'D:/Playwright-Pytest-Base-Framework/AkshayExcelToJSON.xlsx'
    json_data = excel_to_json(excel_file_path)

    with open('output.json', 'w') as json_file:
        json_file.write(json_data)