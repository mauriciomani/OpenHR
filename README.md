![Logo](repo_images/logo.png)

# OpenHR
OpenHR is a Python project to make interesting open-source products for people and **human resource functional area** in organizations. Everything you need to know can be found under a free heroku app: https://open-hrm.herokuapp.com/. However there are a lot of things you can work on to improve and add more data products to OpenHR. Remember that you can help not only by coding but improving styles, logo, documenting, translating, etc. Working on a remote distributed project might be very helpful for yourself.

## Improvements
Please visit the Projects section (OpenHR) to check for "to do" tasks or add more "to do". You can also open an "Issue" and link it to current Project. So we can all know what you are currently working on.<br>
If working locally please **clone** the repository, however be aware there might be changes in the main branch, specially in the **webpage.py** file. You can also **fork** the repository. Always create a **new branch** for the apps you working on and kindly make a Pull Request we will be glad to approve. If need a guide on how to make PRs online or offline please visit this [link](documentation/creating_pr.md). No project (app) will be rejected to be part of OpenHR web application, however we insist on working under the following practices:
* Modular code for reusability.
* Comments, please add only necessary comments, unless your project is highly code oriented and you want to help others understand step by step.
* Group you code, according to the logic of the mentioned.
* Use consistent names (try to keep everything on english, however not mandatory).
* Do not repeat. Look for libraries you can use or functions inside OpenHR.
* Avoid deep nesting.
* Avoid uploading csv.
* Keep code as simple as posible.
* Always try to connect with cloud services (if help needed please contact on the communication channels).
* Please add unit, integration and functional testing.
* Avoid by all means to include in code any tokens or passwords (please contact for help).

Remember we are trying to work with **best practices** if any file does not follow best practices please open an Issue or a PR and will be happy to open debate. On more information on the conventions that sould be follow please visit [python best](documentation/python_best.md)

## How to start working
This is the simple guide, clone the code, you can use ssh: `git clone git@github.com:mauriciomani/OpenHR.git` or just download the zip file. It is **highly important that you understand that trends.py file is not useful since you need AWS access**: `aws_access_key_id` and `aws_secret_access_key` (if need access to AWS please contact us), so do not worry if get an error when trying to access `/data` route. Please avoid `git add .`, instead use `git add name_of_file`. Install all the requierements libraries under the **requierements.txt** file, you can use `pip install -r requirements.txt` or check the needed libraries (if using Anaconda you might still need to install Flask). Once done that you are ready to type on the command line: `python webpage.py`. This will allow you to make local tests on you computer, you can also **change debug to True** as long as you **remeber to change it to False again** when commiting.

## OpenHR structure
Currently OpenHR is deployed in a Heroku free app under the **open-hrm** name and automatic deployments have not been enabled. The web page application is built using Python's [Flask](https://flask.palletsprojects.com/en/1.1.x/) library, however, we are aware might be needed to migrate to [Django](https://www.djangoproject.com/). Some of the data pipelines are being managed by AWS, if need access please contact us. We use [Bootstrap](https://getbootstrap.com/) in our **front-end**. The files and folder organization follows the Flask conventions (practically identically to Django). **static** and **templates** folder include images, css files and html files respectively. Under templates file you can find **base.html** that is the main template for all the views, please make sure you are using it with [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) templating language.<br>
Most important file in the Flask app is the **webpage.py**, please make sure **debug is off**. Remember that in this file you can add your static and dynamic html files and all the necessary logic.<br>
Please add all the files that are usefull on the repository but not on the deployed app under the **.slugignore** file (this is like a .gitignore but for Heroku). If you are adding any python dependency (library) kindly add it to the **requierements.txt** file.

### Not so important files
**repo_images** is a folder that contains important images for the project but currently not for the deployed app. The **the-Great-Wave-off-Kanagawa.jpg** is the image that has been used as color palette, please feel free to come up with new color palettes. **LICENCE** and **Procfile**, the former keeps the information of the LICENSE for the current project, the latter is for productionize the application under Heroku. **aws/google_trends**, unless you plan to work under the unemployment rate and google trends application please ignore it; however, might be useful when adding AWS microservices.

## RoadMap
* Relational model for blog logic (integration with cloud services).
* Add english and spanish link.
* Work on unit tests.
* Recommendation system for job postings.
* Web scraping on job posting for discrimmination analysis.
* Improve google trends and unemployment rates forecast.
* Deploy application in any IaaS.

## Useful information to getting started with OpenHR
* [Github guides](https://guides.github.com/activities/hello-world/)
* [Version control with Git](https://www.udacity.com/course/version-control-with-git--ud123)
* [Jose Portilla Django Udemy bootcamp](https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/)
* [Django and Python ultimate web development bootcamp](https://www.udemy.com/course/the-ultimate-beginners-guide-to-django-django-2-python-web-dev-website/)
* [Tech with Tim Flask tutorial](https://www.youtube.com/watch?v=mqhxxeeTbu0)
* [Data Enginner Udacity Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027)
* [Machine Learning Enginner](https://www.udacity.com/course/machine-learning-engineer-nanodegree--nd009t) Useful for coding best practices.
* [For more resources on basic Python and Data Science find OpenHR guide](documentation/learning_resources.md)
* Contact us for help using the communication channel, we will be glad to explain everything needed.

## Communication
mail: mauricioman12@gmail.com