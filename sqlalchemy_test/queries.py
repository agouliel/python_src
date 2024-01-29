from db import Session
from models import Product
from sqlalchemy import select

session = Session()

q1 = select(Product.name_and_cpu())
results1 = session.execute(q1)
for row in results1:
    print(row)

q2 = select(Product)
results2 = session.execute(q2)
for row in results2:
    print(row[0].id_and_name())
