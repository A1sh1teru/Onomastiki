from flask import Flask, render_template, request, url_for
import nbformat
from nbconvert import PythonExporter
import io
from contextlib import redirect_stdout

app = Flask(__name__)

@app.route('/')
def layout():
    return render_template('layout.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/', methods=['GET', 'POST'])
def run_notebook():
    if request.method == 'POST':
        notebook_file = request.files['notebook']  # Получаем загруженный .ipynb файл
        csv_files = [request.files['csv_file_1'], request.files['csv_file_2'], request.files['csv_file_3']]  # Получаем загруженные .csv файлы
        notebook_content = notebook_file.read()  # Читаем содержимое загруженного .ipynb файла
        notebook = nbformat.reads(notebook_content, as_version=4)  # Интерпретируем содержимое файла .ipynb как блокнот

        # Дополнительная обработка .csv файлов
        for csv_file in csv_files:
            csv_content = csv_file.read()  # Читаем содержимое каждого загруженного .csv файла
            # Далее выполняется необходимая обработка .csv файлов

        exporter = PythonExporter()
        (python_code, resources) = exporter.from_notebook_node(notebook)  # Преобразуем содержимое блокнота в код Python

        f = io.StringIO()
        with redirect_stdout(f):
            exec(python_code)  # Выполняем полученный код Python

        output = f.getvalue()
        return render_template('layout.html', output=output)  # Вывод передается в шаблон HTML для отображения
    # return render_template('layout.html')
# 

if __name__ == "__main__":
    app.run(debug=True)