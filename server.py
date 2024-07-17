from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector


app = Flask(__name__)
app.secret_key = "2934872093487"


def get_db_connection():
    connection = mysql.connector.connect(
        user="root", password="aspirine@123", host="localhost", database="gs"
    )
    return connection


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM password")
        password_db = cursor.fetchall()
        user_password = password_db[0][0]
        print(user_password)
        if request.method == "POST":
            password = request.form["password"]
            if user_password == password:
                session["logged_in"] = True
                return redirect(url_for("get_products"))

    return render_template("index.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    if request.method == "POST":
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM password")
        password_db = cursor.fetchall()
        current_db_password = password_db[0][0]
        current_user_password = request.form["password"]
        new_password = str(request.form["newpassword"])
        new_retype = request.form["confirmnewpassword"]

        if new_password == new_retype:
            if current_user_password == current_db_password:
                print(new_password)
                cursor.execute(f"UPDATE password SET password='{new_password}'")
                connection.commit()
                connection.close()
                return render_template("index.html")
            else:
                return "<h2>پسورد تایپ شده با پسورد شما همخوانی ندارد</h2>"
        else:
            return "<h2>پسورد جدید با پسورد دوباره تایپ شده همخوانی ندارد</h2>"
    return render_template("change.html")


@app.route("/getProducts", methods=["GET", "POST"])
def get_products():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "select products.product_id, products.name, products.uom_id, products.price_per_unit, products.total, products.remaining, products.date_of_purchase, products.total_price, uom.uom_name from products inner join uom on products.uom_id=uom.uom_id ORDER BY products.total ASC"
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("getProducts.html", rows=rows)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        connection = get_db_connection()
        name = request.form["name"]
        total_number = request.form["number"]
        price_per_unit = request.form["number1"]
        unit = request.form["unit"]
        date = request.form["date"]
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO products (name, uom_id, price_per_unit, total, remaining, date_of_purchase) VALUES ('{name}', {unit}, {price_per_unit}, {total_number}, {total_number}, '{date}')"
        )
        connection.commit()
        connection.close()

    return render_template("addProduct.html")


@app.route("/products")
def manage_products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "select products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name from products inner join uom on products.uom_id=uom.uom_id"
    )
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template("manage-product.html", rows=rows)


@app.route("/orders")
def manage_orders():
    return render_template("order.html")


if __name__ == "__main__":
    app.run(debug=True)
