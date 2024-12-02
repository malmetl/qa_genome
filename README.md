# qa_genome
Тесты для VGARus

В разделе "Build" добавьте шаг "Execute shell" (или "Execute Windows batch command" для Windows).
````
git config --global http.sslVerify false

git clone https://github.com/malmetl/qa_genome.git

cd qa_genome

pip install -r requirements.txt

pytest --alluredir=allure-results

allure generate allure-results -o allure-report --clean
````
.


