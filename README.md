*Blueslide Scan*
============

### A Google dorks searching tool to discover SQL injection ###


# **Usage** #

The tool will perform a Google search and after that will test GET parameters looking for error/time-based/blind-based SQL injection points.

## Looking for PHP files belonging to the .com domain with "id" parameter in the URL  (retrieving 3 Google result pages) ##
`python blueslide.py --site .com --ext php --inurl ?id= 3`

## Looking for .com URLs with "price" parameter and the word "product" in the title (retrieving 2 Google result pages). ##
`python blueslide.py --site .com --intitle products --inurl ?price= 2`


It is recommended not to perform high number or searches in a short time to avoid Google's reCaptcha mechanism.


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
