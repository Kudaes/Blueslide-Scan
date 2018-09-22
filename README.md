*Blueslide Scan*
============

### A Google dorks searching tool to discover SQL injection ###


# **Usage** #

The tool performs a Google search based on the dorks supplied and after that tests GET parameters looking for SQL injection points.

## Looking for PHP files belonging to my.domain with "id" parameter in the URL  (retrieving 3 Google result pages) ##
`python blueslide.py --site my.domain --ext php --inurl ?id= 3`

## Looking for my.domain URLs with "price" parameter and the word "product" in the title (retrieving 2 Google result pages). ##
`python blueslide.py --site my.domain --intitle product --inurl ?price= 2`


It is recommended not to perform a high number of searches in a short time in order to avoid Google's Captcha mechanism.


# **Requirements** #
* Python2.
* requests.
* re.
* multiprocessing.
* google module.


# **Legal Disclaimer** #
This project is made for educational and ethical testing purposes only. Usage of Blueslide Scan for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.


# **License** #
The project is licensed under MIT License.


# **Author** #
*Kurosh Dabbagh Escalante*
* Linkedin: [https://www.linkedin.com/in/kuroshda/](https://www.linkedin.com/in/kuroshda/)
