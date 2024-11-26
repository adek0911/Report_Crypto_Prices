import requests
from datetime import datetime
# from Email_sender import email_send,email_send_table # FOR TEST ONLY
from Report_crypto.Email_sender import email_send_table
import json

def count_percent(
    price_dict: list,
    fresh_price: tuple,
    today: str = "Dzis",
    alert_change: float = 0,
) -> list:
    prep_list = []
    for i in range(len(price_dict)):
        ans: float = (
            (fresh_price[1] - price_dict[i]) * 100 / fresh_price[1]
        ).__round__(2)
        prep_value=f"{str(ans)}%"
        prep_list.append(f"<td>{prep_value}</td>")
    result=''.join(prep_list)
    return result


def download_prices(crypto_id: str,coingecko_crudencial: dict) -> list:
    result = []
    url_json = requests.get(
        f"{coingecko_crudencial['url']}{crypto_id}/market_chart?vs_currency=usd&days=7&interval=daily&precision=4",headers=coingecko_crudencial['headers'])
    if url_json.status_code == 200:
        url_json = url_json.json()
        for i in url_json["prices"]:
            i[0] = datetime.fromtimestamp(i[0] // 1000).strftime("%d/%m/%Y")
        last_price: float = url_json["prices"].pop()
        url_json["prices"].reverse()
        result.append(last_price)
        result.append(url_json["prices"])
        return result
    else:
        print(f"Błąd połączenia {url_json.status_code} {crypto_id}")
        return 'ERROR'


def report():
    with open("./Report_crypto/credentials.json") as file:
        data_from_file = json.load(file)
        crypto_id = data_from_file['crypto_id']
        coingecko =  data_from_file['coingecko']

    with open("/home/adix0911/Report_crypto/credentials.json") as file:
        data_from_file = json.load(file)
        crypto_id = data_from_file['crypto_id']
        coingecko =  data_from_file['coingecko']

    today = datetime.today().strftime("%d-%m-%Y")
    for i, val in enumerate(crypto_id):
        data_list = download_prices(crypto_id[val],coingecko)
        if data_list =='ERROR':
            break
        else:
            if i == 0:
                prep_data=[str(data_list[1][i][0])[:5].replace("/","-") for i in range(7)]
                prep_data.insert(0,"Name: price")

                mess=f"Last 7 days difference of prices from {prep_data[-1]} to {today}\n"
                prep_for_email=[prep_data]

            percent = count_percent([i[1] for i in data_list[1]], data_list[0])
            col_name_val=f"{val}: {data_list[0][1].__round__(2)}$"

            prep_for_email.append(f"<tr><td>{col_name_val}</td>{percent}</tr>\n")
    if len(prep_for_email)>1:
        # print(f"Report for day: {today}\n",prep_for_email) #FOR TEST ONLY
        email_send_table(subject=f"Report for day: {today}",table_data=prep_for_email,mes=mess)
        pass

def status_of_wallet() -> None:
    """Wallet details"""
    """Summary of wallet"""
    pass
# report()

