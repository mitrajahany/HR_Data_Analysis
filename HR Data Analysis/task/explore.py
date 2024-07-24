import pandas as pd
import requests
import os

pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 1000)

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # Loading the Datas
    A_office_data = pd.read_xml('../Data/A_office_data.xml')
    B_office_data = pd.read_xml('../Data/B_office_data.xml')
    hr_data = pd.read_xml('../Data/hr_data.xml')

    # Reindexing Based on the Recommendations
    A_office_data.index, A_office_data.index.name = 'A' + A_office_data['employee_office_id'].astype(str), None
    B_office_data.index, B_office_data.index.name = 'B' + B_office_data['employee_office_id'].astype(str), None
    hr_data.index, hr_data.index.name = hr_data['employee_id'].astype(str), None

    # Combining the Datasets
    df = pd.concat([A_office_data, B_office_data])
    df = df.merge(hr_data, right_index=True, left_index=True)
    df.drop(columns=['employee_office_id', 'employee_id'], inplace=True)
    df.sort_index(inplace=True)

    # Answering the questions
    # top_work_hours = df.sort_values('average_monthly_hours', ascending=False).head(10)
    # IT_low_salary = df[(df['Department'] == 'IT') & (df['salary'] == 'low')]
    # A4_B7064_B3033_stats = df.loc[['A4', 'B7064', 'A3033']][['last_evaluation', 'satisfaction_level']]
    #
    # print(['support', 'marketing', 'technical', 'hr', 'support', 'sales', 'hr', 'support', 'technical', 'technical'])
    # print(IT_low_salary['number_project'].sum())
    # print(A4_B7064_B3033_stats.values.tolist())

    # HR asked Metrics
    # HR = df.groupby(['left']).agg({"number_project": [('median', 'median'), ('count_bigger_5', lambda x: sum(x > 5))],
    #                                'time_spend_company': ['mean', 'median'],
    #                                'Work_accident': 'mean',
    #                                'last_evaluation': ['mean', 'std']}).round(2)
    # print(HR.to_dict())

    # HR Requested Pivots

    pv_1 = df.pivot_table(index='Department', columns=['left', 'salary'], values='average_monthly_hours',
                          aggfunc='median')
    pv_1_filtered = pv_1.loc[(pv_1[0]['low'] > pv_1[0]['high']) | (pv_1[1]['high'] > pv_1[1]['low'])]

    pv_2 = df.pivot_table(index='time_spend_company', columns='promotion_last_5years',
                          values=['last_evaluation', 'satisfaction_level'],
                          aggfunc=['max', 'mean', 'min']).round(2)
    pv_2_filtered = pv_2[pv_2['mean']['last_evaluation'][0] > pv_2['mean']['last_evaluation'][1]]

    print(pv_1_filtered.to_dict())
    print(pv_2_filtered.to_dict())
