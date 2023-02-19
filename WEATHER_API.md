# Weather plugins(loosely named for now)

## WeatherFlow (Tempest)

### API

#### Access
Personal Access Token. Sign in to the Tempest Web App at tempestwx.com, then go to Settings -> Data Authorizations -> Create Token, then copy & paste that token into your app. #TODO: into settings.toml file details.
TEMPEST_API_TOKEN="KeyFromAbove"

Also requires your zipcode and country in the ISO 3166 [format](https://www.iso.org/obp/ui/#search).  For example 14722,US

#### Documentation
https://weatherflow.github.io/Tempest/api/



## Open Weather Map

### API


#### Access
Create a key at https://home.openweathermap.org/api_keys and add the following key in the settings.toml file:
OWM_API_TOKEN="keyFromAbovePage"

#### Parameters
units=metric|imperial|(default=Kelvin)

#### Documentation
https://openweathermap.org/current



