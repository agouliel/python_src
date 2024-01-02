import csv
from db import Session
from models import Product, Manufacturer
from sqlalchemy import delete

def main():
    #Model.metadata.drop_all(engine)  # warning: this deletes all data!
    #Model.metadata.create_all(engine)

    with Session() as session, session.begin(), open('products.csv') as f:
        #session.delete(Product) # this doesn't work (instance is required)
        session.execute(delete(Product))
        session.execute(delete(Manufacturer))

        reader = csv.DictReader(f)
        all_manufacturers = {}

        for row in reader:
            row['year'] = int(row['year'])

            manufacturer = row.pop('manufacturer')
            p = Product(**row)

            if manufacturer not in all_manufacturers:
                m = Manufacturer(name=manufacturer)
                session.add(m)
                all_manufacturers[manufacturer] = m
            all_manufacturers[manufacturer].products.append(p)


if __name__ == '__main__':
    main()
