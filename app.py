from flask import Flask, render_template, request, Response
import requests
from datetime import datetime
import datetime

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stock_calc')
def stock_calc():
    return render_template('stock_calc.html')


@app.route('/fin_info')
def fin_info():
    return render_template('fin_info.html')


@app.route('/fin_info_calc', methods=['POST'])
def fin_info_calc():
    if request.method == 'POST':
        output_name = {}
        symbol = request.form['symbol']

        # get name
        r_name = requests.get("https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + symbol +
                              "&apikey=" + api_key)

        # check if symbol is present/correct
        if r_name.status_code == 200:
            nm = r_name.json()
            full_name = nm['bestMatches']
            if full_name:
                for full in full_name:
                    if '1.0000' in full['9. matchScore']:
                        output_name = full['2. name']
            else:
                output_name = "Check if Symbol Entered is Correct"

            # get symbol
            r_value = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + symbol +
                        "&apikey=" + api_key)
            if r_value.status_code == 200:
                d = r_value.json()
                if d['Global Quote']:
                    output = d['Global Quote']
                else:
                    output = "No Data Found for this Symbol"
            else:
                response = Response(r_value.status_code)
                return render_template('fin_info.html', response=response)
        else:
            response = Response(r_name.status_code)
            return render_template('fin_info.html', response=response)

        # set the system date
        now = datetime.datetime.now()
        output_dt = now.strftime("%c") + " " + "PST"
        #tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
        #output_dt = now.strftime("%c") + " " + tz_string

        return render_template('fin_info.html', output=output, output_name=output_name, output_dt=output_dt)


@app.route('/calculate_profit', methods=['POST'])
def cal_profit():
    if request.method == 'POST':
        # transferring form details to variables

        allot = float(request.form['allot'])
        final_share = float(request.form['final_share'])
        init_share = float(request.form['initial_share'])
        sell_com = float(request.form['sell_com'])
        buy_com = float(request.form['buy_com'])
        capital = float(request.form['capital'])

        proceeds = float(allot * final_share)
        total_purchase = float(allot * init_share)
        capital_cont = proceeds - (total_purchase + buy_com + sell_com)
        tax_capital = float((capital/100) * capital_cont)
        cost = float(total_purchase + sell_com + buy_com + tax_capital)
        net_profit = float(proceeds - cost)
        return_inv = float((net_profit / cost) * 100)
        break_even = float((buy_com + sell_com + total_purchase) / allot)
        result = {'proceeds': proceeds, 'cost': cost, 'net_profit': net_profit, 'return_inv': return_inv,
                  'init_share': init_share, 'sell_com': sell_com, 'buy_com': buy_com, 'tax_capital': tax_capital,
                  'capital': capital, 'break_even': break_even, 'allot': allot, 'capital_cont': capital_cont,
                  'total_purchase': total_purchase}
        for k in result:
            result[k] = round(result[k], 2)
        return render_template('stock_calc.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
