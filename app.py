import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_data_base.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    """
    Страница со всеми пользователями

    Если метод GET:
    Выводит всех пользователей в формате JSON
    Если метод POST:
    Принимает нового пользователя в формате JSON и записывает в БД
    """
    if request.method == 'GET':
        users_data = User.query.all()
        return jsonify([user.to_dict() for user in users_data]), 200
    elif request.method == 'POST':
        user = json.loads(request.data)
        new_user_obj = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        db.session.add(new_user_obj)
        db.session.commit()
        db.session.close()
        return "Пользователь записан в базу данных "


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user_by_id(user_id):
    """
    Страница пользователя по его id
    Если метод GET: выводит данные по пользователю в формате JSON
    Если метод PUT: обновляет данные пользователя
    Если метод DELETE: удаляет пользователя
    """
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Пользователь не найден", 404

        return jsonify(user.to_dict())

    elif request.method == 'PUT':
        user = db.session.query(User).get(user_id)
        user_data = json.loads(request.data)

        if user is None:
            return "Пользователь не найден", 404

        user.id = user_data['id']
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.phone = user_data['phone']
        user.role = user_data['role']
        user.email = user_data['email']
        user.age = user_data['age']
        db.session.add(user)
        db.session.commit()

        return "Пользователь обновлен"

    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)

        if user is None:
            return "Пользователь не найден", 404

        db.session.delete(user)
        db.session.commit()
        db.session.close()

        return f"Пользователь с id {user_id} удален", 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    """
    Страница со всеми заказами

    Если метод GET:
    Выводит все заказы в формате JSON
    Если метод POST:
    Принимает новый заказ в формате JSON и записывает в БД
    """
    if request.method == 'GET':
        orders_data = Order.query.all()
        return jsonify([order.to_dict() for order in orders_data]), 200
    elif request.method == 'POST':
        order = json.loads(request.data)
        month_start, day_start, year_start = [int(o) for o in order['start_date'].split("/")]
        month_end, day_end, year_end = order['end_date'].split("/")
        new_order_obj = Order(
            id=order['id'],
            description=order['description'],
            start_date=datetime.date(year=year_start, month=month_start, day=day_start),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )
        db.session.add(new_order_obj)
        db.session.commit()
        db.session.close()
        return "Заказ записан в базу данных "


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_order_by_id(order_id):
    """
    Страница заказа по его id
    Если метод GET: выводит данные по заказу в формате JSON
    Если метод PUT: обновляет данные заказа
    Если метод DELETE: удаляет заказ
    """
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Заказ не найден", 404
        return jsonify(order.to_dict())

    elif request.method == 'PUT':
        order = db.session.query(Order).get(order_id)
        order_data = json.loads(request.data)

        if order is None:
            return "Заказ не найден", 404

        month_start, day_start, year_start = [int(o) for o in order_data['start_date'].split("/")]
        month_end, day_end, year_end = order_data['end_date'].split("/")

        order.id = order_data['id']
        order.description = order_data['description']
        order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
        order.end_date = datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']

        db.session.add(order)
        db.session.commit()
        db.session.close()

        return "Заказ обновлен"

    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)

        if order is None:
            return "Пользователь не найден", 404

        db.session.delete(order)
        db.session.commit()
        db.session.close()

        return f"Заказ с id {order_id} удален", 200


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    """
    Страница со всеми предложениями

    Если метод GET:
    Выводит все предложения в формате JSON
    Если метод POST:
    Принимает новое предложение в формате JSON и записывает в БД
    """
    if request.method == 'GET':
        offers_data = Offer.query.all()
        return jsonify([offer.to_dict() for offer in offers_data]), 200
    elif request.method == 'POST':
        offer = json.loads(request.data)
        new_offer_obj = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение записано в базу данных "


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def get_offer_by_id(offer_id):
    """
    Страница пользователя по его id
    Если метод GET: выводит данные по предложению в формате JSON
    Если метод PUT: обновляет данные предложения
    Если метод DELETE: удаляет предложение
    """
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Предложение не найдено", 404
        return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        offer = db.session.query(Offer).get(offer_id)
        offer_data = json.loads(request.data)

        if offer is None:
            return "Предложение не найдено", 404

        offer.id = offer_data['id']
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']

        db.session.add(offer)
        db.session.commit()
        db.session.close()

        return "Предложение обновлено", 200

    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)

        if offer is None:
            return "Предложение не найдено", 404

        db.session.delete(offer)
        db.session.commit()
        db.session.close()

        return "Предложение удалено", 200


if __name__ == '__main__':
    app.run()
