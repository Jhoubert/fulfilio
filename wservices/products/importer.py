from database import db_session
from models import Product


def insert_data(df):
    uniques = df.drop_duplicates(subset=['sku'], keep='last')
    total_rows = len(uniques)
    it = 0
    for index, row in uniques.iterrows():
        new_product = Product(
            name=row["name"],
            sku=row["sku"],
            description=row["description"]
        )
        db_session.add(new_product)
        it += 1
        yield {'current': it, 'total': total_rows}
    db_session.commit()
    return {'current': it, 'total': total_rows}
