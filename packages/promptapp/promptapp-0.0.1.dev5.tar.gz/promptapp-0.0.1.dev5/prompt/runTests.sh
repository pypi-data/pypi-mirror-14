cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)/../"
coverage run --source=prompt/classes --branch -m unittest discover -s prompt/tests -p "*.py"
coverage html -d prompt/htmlcov
