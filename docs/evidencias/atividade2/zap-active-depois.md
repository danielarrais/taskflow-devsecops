# ZAP Scanning Report

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 0 |
| Low | 1 |
| Informational | 4 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP warnings logged - see the zap.log file for details | 68    |
| Info | Informational |  | Percentage of network failures | 1 % |
| Info | Informational | http://127.0.0.1:5001 | Percentage of responses with status code 2xx | 43 % |
| Info | Informational | http://127.0.0.1:5001 | Percentage of responses with status code 3xx | 7 % |
| Info | Exceeded Low | http://127.0.0.1:5001 | Percentage of responses with status code 4xx | 49 % |
| Info | Informational | http://127.0.0.1:5001 | Percentage of endpoints with content type text/html | 100 % |
| Info | Informational | http://127.0.0.1:5001 | Percentage of endpoints with method GET | 93 % |
| Info | Informational | http://127.0.0.1:5001 | Percentage of endpoints with method POST | 6 % |
| Info | Informational | http://127.0.0.1:5001 | Count of total endpoints | 31    |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Private IP Disclosure | Low | 2 |
| Authentication Request Identified | Informational | 1 |
| Non-Storable Content | Informational | Systemic |
| User Agent Fuzzer | Informational | Systemic |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 2 |




## Alert Detail



### [ Private IP Disclosure ](https://www.zaproxy.org/docs/alerts/2/)



##### Low (Medium)

### Description

A private IP (such as 10.x.x.x, 172.x.x.x, 192.168.x.x) or an Amazon EC2 private hostname (for example, ip-10-0-56-78) has been found in the HTTP response body. This information might be helpful for further attacks targeting internal systems.

* URL: http://127.0.0.1:5001/tasks
  * Node Name: `http://127.0.0.1:5001/tasks`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `172.23.0.1:37303`
  * Other Info: `172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
`
* URL: http://127.0.0.1:5001/tasks%3Fq=ZAP
  * Node Name: `http://127.0.0.1:5001/tasks (q)`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `172.23.0.1:37303`
  * Other Info: `172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:37303
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
172.23.0.1:42111
`


Instances: 2

### Solution

Remove the private IP address from the HTTP response body. For comments, use JSP/ASP/PHP comment instead of HTML/JavaScript comment which can be seen by client browsers.

### Reference


* [ https://datatracker.ietf.org/doc/html/rfc1918 ](https://datatracker.ietf.org/doc/html/rfc1918)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ Authentication Request Identified ](https://www.zaproxy.org/docs/alerts/10111/)



##### Informational (High)

### Description

The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.

* URL: http://127.0.0.1:5001/login
  * Node Name: `http://127.0.0.1:5001/login ()(csrf_token,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=username
userValue=ZAP
passwordParam=password
referer=http://127.0.0.1:5001/login
csrfToken=csrf_token`


Instances: 1

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/)



#### Source ID: 3

### [ Non-Storable Content ](https://www.zaproxy.org/docs/alerts/10049/)



##### Informational (Medium)

### Description

The response contents are not storable by caching components such as proxy servers. If the response does not contain sensitive, personal or user-specific information, it may benefit from being stored and cached, to improve performance.

* URL: http://127.0.0.1:5001/WEB-INF/web.xml
  * Node Name: `http://127.0.0.1:5001/WEB-INF/web.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: http://127.0.0.1:5001/Windows/system.ini
  * Node Name: `http://127.0.0.1:5001/Windows/system.ini`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: http://127.0.0.1:5001/bin/sleep
  * Node Name: `http://127.0.0.1:5001/bin/sleep`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: http://127.0.0.1:5001/scRipt
  * Node Name: `http://127.0.0.1:5001/scRipt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: http://127.0.0.1:5001/tasks
  * Node Name: `http://127.0.0.1:5001/tasks`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``

Instances: Systemic


### Solution

The content may be marked as storable by ensuring that the following conditions are satisfied:
The request method must be understood by the cache and defined as being cacheable ("GET", "HEAD", and "POST" are currently defined as cacheable)
The response status code must be understood by the cache (one of the 1XX, 2XX, 3XX, 4XX, or 5XX response classes are generally understood)
The "no-store" cache directive must not appear in the request or response header fields
For caching by "shared" caches such as "proxy" caches, the "private" response directive must not appear in the response
For caching by "shared" caches such as "proxy" caches, the "Authorization" header field must not appear in the request, unless the response explicitly allows it (using one of the "must-revalidate", "public", or "s-maxage" Cache-Control response directives)
In addition to the conditions above, at least one of the following conditions must also be satisfied by the response:
It must contain an "Expires" header field
It must contain a "max-age" response directive
For "shared" caches such as "proxy" caches, it must contain a "s-maxage" response directive
It must contain a "Cache Control Extension" that allows it to be cached
It must have a status code that is defined as cacheable by default (200, 203, 204, 206, 300, 301, 404, 405, 410, 414, 501).

### Reference


* [ https://datatracker.ietf.org/doc/html/rfc7234 ](https://datatracker.ietf.org/doc/html/rfc7234)
* [ https://datatracker.ietf.org/doc/html/rfc7231 ](https://datatracker.ietf.org/doc/html/rfc7231)
* [ https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html ](https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html)


#### CWE Id: [ 524 ](https://cwe.mitre.org/data/definitions/524.html)


#### WASC Id: 13

#### Source ID: 3

### [ User Agent Fuzzer ](https://www.zaproxy.org/docs/alerts/10104/)



##### Informational (Medium)

### Description

Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.

* URL: http://127.0.0.1:5001
  * Node Name: `http://127.0.0.1:5001`
  * Method: `GET`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)`
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:5001
  * Node Name: `http://127.0.0.1:5001`
  * Method: `GET`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)`
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:5001/
  * Node Name: `http://127.0.0.1:5001/`
  * Method: `GET`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)`
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:5001/
  * Node Name: `http://127.0.0.1:5001/`
  * Method: `GET`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)`
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:5001/tasks/new
  * Node Name: `http://127.0.0.1:5001/tasks/new ()(csrf_token,description,title)`
  * Method: `POST`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)`
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution



### Reference


* [ https://owasp.org/www-project-web-security-testing-guide/ ](https://owasp.org/www-project-web-security-testing-guide/)



#### Source ID: 1

### [ User Controllable HTML Element Attribute (Potential XSS) ](https://www.zaproxy.org/docs/alerts/10031/)



##### Informational (Low)

### Description

This check looks at user-supplied input in query string parameters and POST data to identify where certain HTML attribute values might be controlled. This provides hot-spot detection for XSS (cross-site scripting) that will require further review by a security analyst to determine exploitability.

* URL: http://127.0.0.1:5001/tasks%3Fq=ZAP
  * Node Name: `http://127.0.0.1:5001/tasks (q)`
  * Method: `GET`
  * Parameter: `q`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:5001/tasks?q=ZAP

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
q=ZAP

The user-controlled value was:
zap`
* URL: http://127.0.0.1:5001/login
  * Node Name: `http://127.0.0.1:5001/login ()(csrf_token,password,username)`
  * Method: `POST`
  * Parameter: `csrf_token`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:5001/login

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
csrf_token=mcFaIcLBx50gLt3FWaCIsPmbnsC96G88oRFnMDLgIfk

The user-controlled value was:
mcfaiclbx50glt3fwacispmbnsc96g88orfnmdlgifk`


Instances: 2

### Solution

Validate all input and sanitize output it before writing to any HTML attributes.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)


#### CWE Id: [ 20 ](https://cwe.mitre.org/data/definitions/20.html)


#### WASC Id: 20

#### Source ID: 3


