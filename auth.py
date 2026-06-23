import bcrypt
from database import conn, cursor


def register_user(name,email,password):

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(

            "INSERT INTO users(name,email,password) VALUES(?,?,?)",

            (
                name,
                email,
                hashed_password
            )

        )

        conn.commit()

        return True

    except:

        return False


def login_user(email,password):

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)
    )

    user = cursor.fetchone()

    if user:

        stored_password = user[3]

        if bcrypt.checkpw(

            password.encode('utf-8'),

            stored_password

        ):

            return user

    return None
