## To setup the project
1/ Clone the project

2/ Setup your CLIENT_ID and CLIENT_SECRET

3/ Add 'http://127.0.0.1:5000/auth/callback' in 'Redirect URIs' in your spotify application

4/ Run in your terminal:

      1/ `docker-compose -f docker-compose-test.yml stop`
      
      2/ `docker-compose -f docker-compose-test.yml build`
      
      3/ `docker-compose -f docker-compose-test.yml up -d`
      
      These commands must create 2 containers (back and postgres).

## Explanation
In `bootstrap.py` we created a singleton `postgresql_artists_repository` which will be used in our project.
When we initiate this singleton, we will create 3 tables (if they  don't already exist).
the 3 tables are:

    - Artists:
    
    - New_releases
    
    - new_releases_artist
