from data.data import tours
from data.base import Session
from data.models import Tour


def write_data_to_db():
    with Session() as session:
        for index, tour in tours.items():
            tour_db = Tour(id=index, **tour)
            session.add(tour_db)

        session.commit()

    print("Дані перенесено")
