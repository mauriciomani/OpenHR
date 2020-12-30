pip install -t . pandas
pip install -t . pytrends
pip install -t . fsspec
pip install -t . s3fs

rm -r *.dist-info __pycache__

zip -r name_of_zip_file.zip .
