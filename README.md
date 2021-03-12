# Script for regularly downloading audio from the Infinity call center campaign


# Requirements
+ The script works with the [Infinity call center platform](https://www.infinity.ru/). Working with other software is not expected. U+1F60A
+ Before using the app, you need to create a campaign in Infinity, understand which database table to work with.
+ In the settings of the Infinity platform (Call-center X), all permissions to access the API must be set.


# Installation
+ Clone the repository and go to the application folder:
``` python
git clone https://git.romir.ru/parygin.e/infinity_crone_regularly_uploading.git
cd infinity_crone_regularly_uploading
```
+ Install and activate the Python virtual environment:
``` python
python3 -m venv venv
source venv/bin/activate
```
+ Install all the dependencies are gathered in `requirements.txt`:
``` python
pip3 install -r requirements.txt
```
+ Write your settings in the `.env` file (after removing the `example` from its name).
+ Launch the app.
``` python
python3 infinity_crone_regularly_uploading
```


### Basic settings
+ By default, the script downloads all the records for `yesterday`. If desired, you can change it to `today`. No other options are provided.
``` python
DAY = 'yesterday'
```
+ During execution, the script will create a folder named by date, for example, `2021-12-13`. Audio recordings uploaded in this session will be saved there.


# ToDo
- [ ] Add code descriptions and comments.
- [ ] Setting up the correct logging.


# Information
- [Infinity: Платформа для колл-центра](https://www.infinity.ru/)
- [Infinity: Список методов и событий модуля интеграции (при использовании HTTP)](https://www.inteltelecom.ru/wiki/spisok-metodov-i-sobytiy-modulya-integratsii-pri-ispolzovanii-http/)
