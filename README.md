<!-- PROJECT TITLE -->
<br />
<div align="center">
    <h3 align="center">My Diet</h3>
    <p align="center">
        An intake organizing and recording tool to help you eat healthy
        <br />
    </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#authentication">Authentication</a></li>
        <li><a href="#index-page">Index Page</a></li>
        <li><a href="#intake-calculate">Intake Calculator</a></li>
        <li><a href="#profile">User Profile</a></li>
      </ul>
    </li>
    <li><a href="#file-structure">File Structure</a></li>
    <li>
      <a href="#distinctiveness-complexity">Distinctiveness and Complexity</a>
      <ul>
        <li><a href="#distinctiveness">Distinctiveness</a></li>
        <li><a href="#complexity">Complexity</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Many friends of mine want to eat healthy. But they simply do not know where to start. I want to make an intake-related application - the one beginners would enjoy. This app is it.

* It is **easy to understand**. Foods are divided into 5 simple groups in most of this application.
* It gives time to **reflect**. Users would gain or improve self-acknowledgement when inputing the amount they eat.
* It has no social network or other features. Users may **not be distracted** while enjoying their very own personal experience.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![VSCode][VSCode.com]][VSCode-url]
* [![Django][Django.com]][Django-url]
* [![SQLite][SQLite.com]][SQLite-url]
* [![HTML5][HTML5.com]][HTML5-url]
* [![JavaScript][JavaScript.com]][JavaScript-url]
* [![Python][Python.com]][Python-url]
* [![Chart][Chart.js]][Chart-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Below is a list of items you will need to use the web application. Click on the links to see installation guides.
* IDE: [Visual Studio Code](https://code.visualstudio.com/download), [IntelliJ IDEA](https://www.jetbrains.com/idea/), [PyCharm](https://www.jetbrains.com/pycharm/), or others
* [Python](https://medium.com/co-learning-lounge/how-to-download-install-python-on-windows-2021-44a707994013)
* [Django](https://docs.djangoproject.com/en/4.1/intro/install/)
* [SQLite](https://www.sqlite.org/download.html)
* [Git](https://git-scm.com/downloads)

### Installation

1. Clone the repository
    ```sh
    git clone https://github.com/me50/huang9185/blob/web50/projects/2020/x/capstone.git
    ```
2. Open your terminal and make sure you are on the folder that contains manage.py
    ```sh
    python manage.py runserver
    ```
3. Open your browser and input link to run the application
    ```sh
    127.0.0.1:8000/diet
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

[![app-index-screenshot][index]](#usage)

### Authentication {#authentication}

* If new to the site, navigate to register page.
    [![index-register-screenshot][index-register]](#authentication)
    * Register yourself with all fields filled.
    [![register-screenshot][register]](#authentication)
* If already have an account, navigate to login page.
    [![index-login-screenshot][index-login]](#authentication)
    * Fill all the fields.
    [![login-screenshot][login]](#authentication)
    * If forgot password, click the link below to change password.
    [![login-password-screenshot][login-password]](#authentication)
    * Fill the form and click verify button.
    [![user-verify-screenshot][user-verify]](#authentication)
    * Type in new password and confirm.
    [![confirm-password-screenshot][confirm-password]](#authentication)
    * Go back to login page and log in.

### Intake Calculator {#intake-calculate}

* To calculate your intake by groups or subgroups, log in and navigate to intake calculator.
    [![index-calculate-screenshot][index-calculate]](#intake-calculate)
    * There are five main groups and more than 100 subgroups.
    [![calculate-groups-screenshot][calculate-groups]](#intake-calculate)
    * Click on any of the two choices, the page below will show up.
    [![calculate-screenshot][calculate]](#intake-calculate)
    * Choose the food name in the first column, fill in the amount in the second. Click on the add and delete buttons on the right side to add or delete rows. Notice the delete button is diabled for the very first row. All fields must be filled to submit the form, or the prompt will stop you from submittion.
    * Click on the verify button to verify, the OK button to confirm, and the submit button to submit. After clicking the OK button, your input cannot be adjusted.
    [![calculate-submit-screenshot][calculate-submit]](#intake-calculate)
    * The result including a table, a sample pie chart to compare with, another pie chart of your own intake will show up.
    [![calculate-result-screenshot][calculate-result]](#intake-calculate)
    * Click on the record data button to record the values by groups or subgroups in your profile, and you will be taken to the index page.
    [![result-record-screenshot][result-record]](#intake-calculate)

### User Profile {#profile}

* Click on your username to go into your profile.
    [![index-profile-screenshot][index-profile]](#profile)
    * Click on the previous and next icons in left-bottom corner of the page to check more of your records. Notice the previous or next button would not show up if on the first or last page of records.
    [![profile-screenshot][profile]](#profile)
    * To search for records by time, type in numbers in the input field, click on the arrow to classify if it's for day, month, or year. Prompt will show up for invalid input. Finally, click on search button to search.
    [![profile-search-screenshot][profile-search]](#profile)
    * To compare the records in one page, click the compare data button in the bottom-left corner of profile page
    [![profile-compare-screenshot][profile-compare]](#profile)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- FILE STRUCTURE -->
## File Structure {#file-structure}

Below is a list of files and folders created by me. Click on them to see details.

<details>
  <summary>File Navigation</summary>
  <ul>
    <details>
      <summary><a href="#diet">diet</a></summary>
      <ul>
        <details>
          <summary><a href="#static">static/diet</a></summary>
          <ul>
            <li><a href="#food-json">food.json</a></li>
            <li><a href="#carousel-images">fruit-fade-3.jpg</a></li>
            <li><a href="#carousel-images">vegies.jpg</a></li>
            <li><a href="#carousel-images">protein.jpg</a></li>
            <li><a href="#carousel-images">grain-1.jpg</a></li>
            <li><a href="#intake-js">intake.js</a></li>
            <li><a href="#password-js">password.js</a></li>
            <li><a href="#profile-js">profile.js</a></li>
            <li><a href="#styles-css">styles.css</a></li>
          </ul>
        </details>
        <details>
          <summary><a href="#templates">templates/diet</a></summary>
          <ul>
            <li><a href="#index-html">index.html</a></li>
            <li><a href="#intake-html">intake.html</a></li>
            <li><a href="#layout-html">layout.html</a></li>
            <li><a href="#login-html">login.html</a></li>
            <li><a href="#password-html">password.html</a></li>
            <li><a href="#profile-html">profile.html</a></li>
            <li><a href="#register-html">register.html</a></li>
          </ul>
        </details>
        <li><a href="#models">models</a></li>
        <li><a href="#urls">urls</a></li>
        <li><a href="#views">views</a></li>
      </ul>
    </details>
    <li><a href="#images">images</a></li>
  </ul>
</details>

### diet {#diet}

The folder that contains all files of diet application

#### static/diet {#static}

The folder that contains all static files for diet

###### [food.json](/diet/static/diet/food.json) {#food-json}
A json file as data source downloaded from [foodb.ca](https://foodb.ca/downloads). It contains all foods' information including names, scientific names, groups, subgroups, descriptions, etc.

###### [carousel images](/diet/static/diet) {#carousel-images}
JPG images used for the carousel of index page

###### [intake.js](/diet/static/diet/intake.js) {#intake-js}
The JavaScript file attached to intake.html

```sh
document.querySelector('#submit-form').onclick = () => result_view(
            document.querySelector('#intake-form').dataset.type
        );

function result_view(type)
```
This function reveals result-view and hides form-view. It also passes the type parameter to intake_calculate function by calling it.

```sh
function intake_calculate(type)
```
It sends user intake to intake_calculator view using POST method by fetching. It then takes the response/result, and fills in the result table and pie charts.

```sh
document.querySelector('#verify-form').onclick = () => validate_form();

function validate_form()
```
The function verifies user intake input. If valid, enable the submit button.

```sh
document.querySelector(".add-row").onclick = () => add_row(document.querySelector(".add-row").parentElement.parentElement);

function add_row(current_row)
```
The function clones current row and inserts to the bottom of form. It makes sure only one set of add and delete button group is visible all the time. If only one row left, the delete button would be disabled.

```sh
document.querySelector('.delete-row').onclick = () => delete_row(document.querySelector(".delete-row").parentElement.parentElement);

function delete_row(current_row)
```
The function deletes current row. If current row is the final row, it renews the listeners attached to the last second row and changes the row's button group's visibility.

###### [password.js](/diet/static/diet/password.js) {#password-js}
The JavaScript file attached to password.html

```sh
function load_verify()
```
The function loads when 'DOMContenLoaded' by default. It hides the actual password view and shows the user identity verification view.

```sh
document.querySelector('#verify').addEventListener('click', () => verify_id());

function verify_id()
```
The function sends user input of username and email to password view using POST method by fetching. If the response/result does not contain error, it passes user id to load_password function.

```sh
function load_password(user_id)
```
It hides the verification view and reveals the actual password view, and attaches a listener to the submit button. The listener checks for equality of two password inputs, and fetches new password and user id to the view with PUT method.

###### [profile.js](/diet/static/diet/profile.js) {#profile-js}
The JavaScript file attached to profile.html

```sh
document.querySelector('#chartBtn').onclick = () => load_chart();

function load_chart()
```
The functions retrieves # of rows and intake amount by five food groups, or, in other words, vertically. It then takes the data and creates five datasets and draws a line chart with five lines corresponding to different groups.

```sh
document.querySelector('select').onchange = () => search_record(
            document.querySelector('select').value
        );

function search_record(val1)
```
When the select value of the search bar is onchange, the function takes val1, which is one of day, month, or year of user choice, and verifies user input. If valid, give the search form an action with type (val1), searchInput, and page number.

###### [styls.css](/diet/static/diet/styles.css) {#styles-css}
The css file that provides style specifications in the range of the app

#### templates/diet {#templates}

The folder that contains all HTML templates for diet

###### [index.html](/diet/templates/diet/index.html) {#index-html}
Contains one carousel view that has four slides with a heading and a paragraph of quotes for each

###### [intake.html](/diet/templates/diet/intake.html) {#intake-html}
Contains a form view of rows, a verify button, and a submit button, and a result view of one table and two canvases

###### [layout.html](/diet/templates/diet/layout.html) {#layout-html}
Contains a navigation bar and a body-class div for body and a block for scripts

###### [login.html](/diet/templates/diet/login.html) {#login-html}
Contains a heading, a message if passed, a login form, and two redirecting links to registration, and password changing respectively

###### [password.html](/diet/templates/diet/password.html) {#password-html}
Contains a verify view of username and email input fields, and a password view of two password input fields, and buttons to "submit forms"

###### [profile.html](/diet/templates/diet/profile.html) {#profile-html}
If the user has records, a search bar, a table of records, a pagination button group, a button to show chart, and a canvas for chart are shown; otherwise, show a message

###### [register.html](/diet/templates/diet/register.html) {#register-html}
Contains a heading, a message if exists, a form to register, and a link to redirect to login page

#### [models](/diet/models.py) {#models}
There are five classes created. The data of Food, Foodgroup, and Subgroup comes from Food.json file under static/diet folder. For all the classes below, default primary keys of id would not be mentioned.

<mark>User class</mark>
The standard user class as a child of django user model

<mark>Food class</mark>
The class used in first columns of all rows in Intake Calculator form. Contains five fields:

* *name*: a text field of food names that cannot be null
* *scientific_name*: a text field that can be null
* *descrption*: a text field 
* *group_id*: an integer field that contains the primary keys of Foodgroup objects
* *subgroup_id*: an integer field that contains the primary keys of Subgroup objects. If a Food object has its subgroup_id as 200, it does not belong to any subgroup.

<mark>Foodgroup class</mark>
The class of main food groups. Contains one field:

* *group_name*: an unique text field

<mark>Subgroup class</mark>
The class of minor food groups. Contains one field:

* *name*: an unique text field

<mark>Record class</mark>
The class of user intake records. It is used for user profile, searching and comparing. Contains seven fields:

* *user_id*: an integer field of user ids
* *time*: a date-time field that is aute-added when object is created
* *vf_amt*: an integer field of vegetable and fruit intake amount
* *protein_amt*: an integer field of protein intake amount
* *grain_amt*: an integer field of grain intake amount
* *liquid_amt*: an integer field of liquid intake amount
* *other_amt*: an integer field of other intake amount

#### [urls](/diet.urls.py) {#urls}
There are nine routes in total:

```sh
path('', views.index, name='index')
```
The route above is used as default when users open up the app url, log or register them in, and after record some intaks.

```sh
path('login', views.login_view, name='login'),
path('logout', views.logout_view, name='logout'),
path('register', views.register, name='register'),
path('password', views.password, name='change_password')
```
The four paths above are used for the authentication system while the last one serves for both normal route and API route purposes.

```sh
path('intake/<str:calc_type>', views.intake, name='intake'),
path('intake/calc/<str:calc_type>', views.intake_calculator, name='calc')
```
This first path directs users to the intake page, the second as an API route is used when calculating intake results.

```sh
path('profile', views.profile, name='profile'),
path('profile/search', views.profile, name='search')
```
The first path is used when users record data or go into their profile, the second one is for them to search records according to specific days, months, or years.

#### [views](/diet/views.py) {#views}

| Function Name | Request Method | Parameters | Return Value | Decorators | Description |
| --- | --- | --- | --- | --- | --- |
| index | GET | request | render index page | none | none |
| profile | GET | request | profile page with records if exist | @login_required | none |
|  | POST |  | index page with message | | record user intake amount |
| record_serialize | none | records (page_obj), num (default=15) | serialized record objects | none | none |
| intake_calculator | POST | request, calc_type (group or subgroup) | json chart_list, liquid_amt, group_names, subgroup_names | @csrf_exempt, @login_required | none |
| intake | GET | request, calc_type | render intake page | @login_required | none |
| password | GET | request | render change-password page | @csrf_exempt | none |
| | POST | | return json user id | | verify user identity when changing password |
| | PUT | | return json message | | save new password |
| register | POST | request | register page if input invalid, index page otherwise | none | none |
| | GET | | render register page | | |
| login_view | POST | request | render index page if input valid, login page otherwise | none | none
| | GET | | render login page | | |
| logout_view | GET | request | render index page | @login_required | none |

### images {#images}

The folder that contains all images for README.md

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- DISTINCTIVENESS AND COMPLEXITY -->
## Distinctiveness and Complexity {#distinctiveness-complexity}

### Distinctiveness
1. I use chart.js in this application and provide a much more elegant <mark>visual presentation</mark> of data. The combination separates this project from all the old ones.
2. The usage of <mark>bootstrap carousel classes</mark> adds a new touch on the visuals and technicals.
3. The function of <mark>adding and deleting row</mark> in the same page without reloading is an entirely new feature that did not appear in any of the projects in the past.
4. The <mark>search bar</mark> in profile page puts button, select, and input tags in one group. The listener attached to the select tag would act differently depends on user choices. 
5. It is an interesting trial using <mark>normal route and API route on one view function</mark>, after considering how similar the definitions and methods are.

### Complexity
The project overall is very complex while using new features and new external classes like chart.js.

<ins>Some new features:</ins>
* Password Changing
* External Database Usage: three models out of five have their data being transfered from foods.ca using Python methods related to files 
  ```sh
  for line in open('food.json', 'r', encoding='utf-8'):
    line = json.loads(line)
  ```
* Row Addition and Deletion
* Chart.js
* Carousel

<ins># of models:</ins> 5
<ins># of js functions:</ins> 10
<ins># of html pages:</ins> 7
<ins># of urls:</ins> 9
<ins># of views:</ins> 9

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Elyn Huang - [@github](https://github.com/huang9185) - helyn20012@outlook.com

Project Link: [https://github.com/me50/huang9185/blob/web50/projects/2020/x/capstone](https://github.com/me50/huang9185/blob/web50/projects/2020/x/capstone)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[index]: images/index.jpg
[index-register]: images/index-register.jpg
[register]: images/register.jpg
[index-login]: images/index-login.jpg
[login]: images/login.jpg
[login-password]: images/login-password.jpg
[user-verify]: images/user-verify.jpg
[confirm-password]: images/confirm-password.jpg
[index-calculate]: images/index-calculate.jpg
[calculate-groups]: images/calculate-groups.jpg
[calculate]: images/calculate.jpg
[calculate-submit]: images/calculate-submit.jpg
[calculate-result]: images/calculate-result.jpg
[result-record]: images/result-record.jpg
[index-profile]: images/index-profile.jpg
[profile]: images/profile.jpg
[profile-search]: images/profile-search.jpg
[profile-compare]: images/profile-compare.jpg
[VSCode.com]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[VSCode-url]: https://code.visualstudio.com/docs
[Django.com]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://docs.djangoproject.com/en/4.1/
[SQLite.com]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/index.html
[HTML5.com]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[HTML5-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
[JavaScript.com]: https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[Python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Chart.js]: https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white
[Chart-url]: https://www.chartjs.org/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com