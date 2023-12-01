# WeatherMap
#### Video Demo:  https://youtu.be/nMFD_s8-dAA
#### Description:
My final project for CS50x is WeatherMap, a web site which allows you to get weather data from marked locations on a map. It uses Openweathermap's free API to get the weather data from markers placed in a map generated using Google Map's API. It includes several more features to allow for a more user friendly usage: A registration and log-in portal and the ability to save places with nickname for quick access.
To create this proejct I needed to research more about APIs, javascript and AJAX. I got this knowledge from two sources, [W3schools](https://www.w3schools.com/graphics/google_maps_basic.asp) and [Stack Overflow](https://stackoverflow.com/questions/29987323/how-do-i-send-data-from-js-to-python-with-flask). I would also like to thank professor David Malan and the whole CS50 staff but most especially the Duck Debugger, who's help made this possible.

#### Layout.html:
Inside my templates folder, I created a layout file which included an adaptation of Bootstrap's Navbar and a footer. The navbar embbeds several hyperlinks in order to navigate through the whole site. Both the footer and the Navbar are influenced in the styles.css file.

#### Styles.css:
The styles.css files contains the CSS tags for the whole site. There is one definition which is used by several items throughout the web site to implement the style of most divs for displaying the weather data.

#### Index.html:
Index.html is the homepage for the site. It extends the layout.html file (as most html files in the project) to create the navbar and the footer. It's design is fairly simple, consisting of several divs (to display the weather data) and one form. At the end, it calls the Google Maps API and the script.js file.

### Script.js:
Located in the static folder, script.js was the hardest part of the whole project. To create it, I had to learn quite a bit of JavaScript. The file starts by fetching the map from the Google Maps API and then inserting it into the index file. Then a click listener is defined, which creates a marker by using a function which is defined later. Then another step is added in order to place the marker from the saved markers. The addMarker function starts by placing the new marker into the map. Then, using AJAX syntax, it sends the location coordinates to the app.py python file for server-side processing. Once it gets the response from Flask, it edits the InnerHTML from the homepage to display the weather data.

### App.py:
App.py is the longest file in the project, which handles all the server-side interactions. It starts by defining a session and calling a database file. Then, it handles the request for the index file. In the marker function, it gets the location data from JavaScript to later insert into the Openweathermap API to get the weather data. To create the Log-in and registration processes, I recylced the code created for Week 9's PSET Finance. In the add function, it gets the marker location from a global variable which is changed by the marker function and the nickname from the form in the add.html file, and inserts it into an SQL database. Finally, the pmarker function returns the saved location data to JavaScript to be placed in the map.

#### Apology.html:
In similar spirit to Finance's aplogy file, apology.html returns an error to the user when some input is not correct.

#### Add.html:
Add.html contains a form to get the desired nickname for the custom user's marker.

#### Login.html:
Login.html contains two text inputs to get the user's log-in data.

#### Register.html:
Like login.html, register.html contains text inputs to get the new user's registration data.

#### Places.html:
Places.html contains a loop which generates a div for each saved place from the user which include the place's name plus a form with a button to get the data from the saved location.

#### Pmarker.html:
Pmarker.html contains nothing inside of it. Its used as a place to send the location coordinates from Python to JavaScript.

#### Weathermap.db:
Weathermap.db is an SQL Database which contains two tables, users and savedplaces. Users contains the login data for each user and Savedplaces references the id for each user and saves their places.



**Weathermap by Inaki Iturriaga, 2023.**
