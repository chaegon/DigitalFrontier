
import pandas as pd

class CodeName():
    def __init__(self):
        self.df_code_name = pd.read_csv('../data/code-name.csv')

    def getDataCodeName(self, sKeyword):
        sKeyword = sKeyword.strip()
        print('>> 검색어 ['+sKeyword+']')
        # print(df_code_name.columns)

        list_search = []
        for idx, row in self.df_code_name[['code', 'name']].iterrows():
            for content in row:
                if sKeyword in content:
                    # print(idx)
                    list_search.append(self.df_code_name.loc[idx])
                    break

        df_search = pd.DataFrame(list_search, columns=self.df_code_name.columns).reset_index()
        print(df_search[['type','code','name']])

        return df_search


if __name__ == '__main__':
    codeName = CodeName()
    while True:
        sInput = input('검색어를 입력하세요: ')
        codeName.getDataCodeName(sInput)
        print('--------------------------------------\n')