from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    '''Функция открывает файл и добавляет в него данные.'''
    # with open('vsearch.log', 'a', encoding="utf-8") as log:
    #     print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    import mysql.connector
    dbconfig = {'host': '127.0.0.1','user': 'root', 'password': '12345', 'database': 'vsearchlogDB', }
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log (phrase, letters, ip, browser_string, results) values (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res,))
    conn.commit()
    cursor.close()
    conn.close()
    # _SQL = """select * from log"""
    # cursor.execute(_SQL)
    # for row in cursor.fetchall():
    #     print(row)



@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    '''Создает страницу с результатом и выводит его'''
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    '''Создает главную страни для ввода'''
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
def view_the_log() -> 'html':
    '''Вывод в браузере данных в лог файле'''
    with open('vsearch.log') as log:
        contents = []
        for line in log:
            contents.append([])
            for i in line.split('|'):
                contents[-1].append(escape(i))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title = 'View Log',
                           the_row_titles = titles,
                           the_data = contents)


if __name__ == '__main__':
    app.run(debug=True)
