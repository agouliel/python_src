# Create and populate the database
`sqlite3 test.db`   
`create table users(id integer, username text, password text, token text, token_expiration text);`   
`insert into users(id, username, password) values(1, 'alex', 'test');`   
`create table vessels(id integer, name);`   
`insert into vessels values(1, 'estia');`

# Run the app
`flask --app attendance run`

# Test using curl
`curl -X POST --user "alex:test" http://127.0.0.1:5000/api/tokens`   
`curl -H "Authorization: Bearer <token>" http://127.0.0.1:5000/api/vessels`
