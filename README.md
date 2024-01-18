# Visitor Location Map

An example web app that shows the location of users on a map. The web app is built with React and Google Maps and the underlying REST API is built in Pyton with FastAPI.

* [Web App](web-app)
* [REST API](api)

## Disclaimer/Scope/Discussion

* The UI is very minimal
* We only show the 1000 most recently registered ips/locations
* The IP may not uniquely identify a user (i.e. the same user may visit from different IPs) so a marker on the map can represent many users behind the same IP. Also, as a single user connects from different locations and with different ISPs this will typically yield multiple markers and sometimes the location of the markers is not accurate.
* I have not tested how the app scales to thousands of locations
