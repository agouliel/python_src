# Useful links
[https://medium.com/@rameshkannanyt0078/managing-database-connections-in-fastapi-best-practices-6f8404364936]   
[https://fastapi.tiangolo.com/tutorial/body]   
[https://stackoverflow.com/questions/77696337/a-formdata-field-called-local-kw-is-added-automatically-as-a-mandatory-argument]   
[https://fastapi.tiangolo.com/tutorial/query-params/]   
[https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database]   
[https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html]

# Test using:
`curl -X POST http://127.0.0.1:8000/update -H "Content-Type: application/json" -d '{"ticket_id":"1","bets":"8"}'`   
`curl http://127.0.0.1:8000/select_with_body -H "Content-Type: application/json" -d '{"ticket_id":"1"}'`   
`curl http://127.0.0.1:8000/select_with_path_param/1`   
`curl http://127.0.0.1:8000/select_with_stream`
