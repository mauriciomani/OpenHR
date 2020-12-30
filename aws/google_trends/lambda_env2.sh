pip install -t . pandas
pip install -t . requests

rm -r *.dist-info __pycache__

zip -r name_of_zip_file.zip .
