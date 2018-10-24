from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
        return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
