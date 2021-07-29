# Shapefile(input) Geojson(ouput) api

### Dependencies

* This project require postgresql database with postgis and hstore extensions enabled
* It used geodjango and django_rest_framework_gis

### Installing

* Clone this repository
```
git clone <repo-url>
```
* Create a postgresql database and enable postgis and hstore extension
* create .env file and place your database connection parameters there same with django secret key


### Executing program

* How to run the program
* create a virtual env and install requirements
```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```
* migrate the model to the database
```
python manage.py migrate
```
* runserver in dev
```
python manage.py runserver
```
* For rest api endpoint visit http://localhost:8000/api
* For django admin site create super user
```
python manage.py createsuperuser 
```
And visit http://localhost:8000/admin


## Help

When having issue installing GDAL in the requirements.txt try installing gdal and lidgdal-dev then use
```
pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
```
Other error create a issue so that i can have a look.
## Authors

Contributors names and contact info

ex. Benard Odhiambo 
ex. [@Henriod](https://twitter.com/Henriod93)


## License

Your can use this project anywhere you might need am not reliable for any issue caused by it

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)