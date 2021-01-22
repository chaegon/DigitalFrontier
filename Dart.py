import requests
import pandas as pd
import io
import zipfile
import xml.etree.ElementTree as et
import json


# 기업 고유번호 크롤링
def get_corpcode(crtfc_key):
    """ OpenDART 기업 고유번호 받아오기 return 값: 주식코드를 가진 업체의 DataFrame """
    params = {'crtfc_key':crtfc_key}
    items = ["corp_code","corp_name","stock_code","modify_date"]
    item_names = ["고유번호","회사명","종목코드","수정일"]
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    res = requests.get(url,params=params)
    zfile = zipfile.ZipFile(io.BytesIO(res.content))
    fin = zfile.open(zfile.namelist()[0])
    root = et.fromstring(fin.read().decode('utf-8'))
    data = []
    for child in root:
        if len(child.find('stock_code').text.strip()) > 1:
            data.append([])
            for item in items:
                data[-1].append(child.find(item).text)
    df = pd.DataFrame(data, columns=item_names)
    return df


def convertFnltt(url, items, item_names, params):
    res = requests.get(url, params)
    json_dict = json.loads(res.text)
    data = []
    if json_dict['status'] == "000":
        for line in json_dict['list']:
            data.append([])
            for itm in items:
                if itm in line.keys():
                    data[-1].append(line[itm])
                else:
                    data[-1].append('')
    df = pd.DataFrame(data, columns=item_names)
    return df


# 단일회사 주요계정
def get_fnlttSinglAcnt(crtfc_key, corp_code, bsns_year, reprt_code):
    items = ["rcept_no", "bsns_year", "stock_code", "reprt_code", "account_nm", "fs_div", "fs_nm",
             "sj_div", "sj_nm", "thstrm_nm", "thstrm_dt", "thstrm_amount", "thstrm_add_amount",
             "frmtrm_nm", "frmtrm_dt", "frmtrm_amount","frmtrm_add_amount", "bfefrmtrm_nm",
             "bfefrmtrm_dt", "bfefrmtrm_amount","ord"]
    item_names = ["접수번호", "사업연도", "종목코드", "보고서코드", "계정명", "개별연결구분",
                  "개별연결명", "재무제표구분", "재무제표명", "당기명", "당기일자","당기금액",
                  "당기누적금액", "전기명", "전기일자", "전기금액","전기누적금액", "전전기명",
                  "전전기일자", "전전기금액", "계정과목정렬순서"]
    params = {'crtfc_key':crtfc_key, 'corp_code':corp_code, 'bsns_year':bsns_year,'reprt_code':reprt_code}
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
    return convertFnltt(url,items,item_names,params)


# 단일회사 전체 재무제표
def get_fnlttSinglAcntAll(crtfc_key, corp_code, bsns_year, reprt_code, fs_div = "CFS"):
    items = ["rcept_no","reprt_code","bsns_year","corp_code","sj_div","sj_nm", "account_id",
             "account_nm","account_detail","thstrm_nm", "thstrm_amount","thstrm_add_amount",
             "frmtrm_nm","frmtrm_amount", "frmtrm_q_nm","frmtrm_q_amount","frmtrm_add_amount",
             "bfefrmtrm_nm", "bfefrmtrm_amount","ord"]
    item_names = ["접수번호","보고서코드","사업연도","고유번호","재무제표구분", "재무제표명","계정ID","계정명",
                  "계정상세","당기명","당기금액", "당기누적금액","전기명","전기금액","전기명(분/반기)",
                  "전기금액(분/반기)","전기누적금액","전전기명","전전기금액", "계정과목정렬순서"]
    params = {'crtfc_key':crtfc_key, 'corp_code':corp_code, 'bsns_year':bsns_year, 'reprt_code':reprt_code, 'fs_div':fs_div}
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    return convertFnltt(url,items,item_names,params)

# 다중회사 주요계정
def get_fnlttMultiAcnt(crtfc_key, corp_code, bsns_year, reprt_code):
    items = ["rcept_no", "bsns_year", "stock_code", "reprt_code", "account_nm", "fs_div", "fs_nm",
             "sj_div", "sj_nm", "thstrm_nm", "thstrm_dt", "thstrm_amount","thstrm_add_amount",
             "frmtrm_nm", "frmtrm_dt", "frmtrm_amount","frmtrm_add_amount", "bfefrmtrm_nm",
             "bfefrmtrm_dt", "bfefrmtrm_amount","ord"]
    item_names = ["접수번호", "사업연도", "종목코드", "보고서코드", "계정명", "개별연결구분","개별연결명", "재무제표구분",
                  "재무제표명", "당기명", "당기일자","당기금액", "당기누적금액", "전기명", "전기일자", "전기금액",
                  "전기누적금액", "전전기명", "전전기일자", "전전기금액", "계정과목정렬순서"]
    corps_str = ",".join(corp_code)
    params = {'crtfc_key':crtfc_key, 'corp_code':corps_str, 'bsns_year':bsns_year,'reprt_code':reprt_code}
    url = "https://opendart.fss.or.kr/api/fnlttMultiAcnt.json"
    return convertFnltt(url,items,item_names,params)



data = pd.DataFrame()
data = get_corpcode('8ea589a8db853913cba6782223a6624bd9263e31')

print(data.head(5))