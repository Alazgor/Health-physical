# from health import db
# from health.models import User
# from datetime import datetime
# from health import db
# from health.models import User
# from datetime import datetime
# from dotenv import load_dotenv
# import os  # Добавьте этот импорт
#
# # Load environment variables from an .env file
# load_dotenv()
#
# # Создать приложение и контекст приложения
# app = create_app()
# with app.app_context():
#     # Создать нового администратора
#     admin_user = User(
#         first_name="Admin",
#         last_name="User",
#         email="adminmail@example.com",
#         birth_date=datetime(2000, 1, 1),
#         role="admin"
#     )
#     admin_user.set_password("Malabar1984")  # Замените на ваш пароль
#
#     # save user in database
#     db.session.add(admin_user)
#     db.session.commit()
