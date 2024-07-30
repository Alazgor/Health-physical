from __future__ import with_statement
from alembic import context
from sqlalchemy import create_engine, pool
from logging.config import fileConfig

# Это путь до вашего базового приложения Flask
import os
import sys
sys.path.append(os.path.abspath(os.getcwd()))  # Примерный путь, может отличаться в зависимости от проекта

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from alembic import op
import sqlalchemy as sa


# Загружаем конфигурацию Flask приложения
config = context.config
fileConfig(config.config_file_name)

# Получаем экземпляр вашего приложения Flask
db = SQLAlchemy(current_app)

# Добавьте путь к моделям, если они не доступны напрямую из приложения Flask
# sys.path.append(os.path.join(os.getcwd(), 'app/models'))

target_metadata = db.metadata

def run_migrations_online():
    engine = db.get_engine()

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Этот блок кода добавляет столбец 'password' и обновляет существующие
def upgrade():
    # Создаем столбец 'password' в таблице 'user' с заданным значением по умолчанию
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password', nullable=False) # временно разрешаем NULL

    # Обновляем другие столбцы в таблице 'user', если это необходимо
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.String(length=150),
               type_=sa.String(length=120),
               nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=150),
               type_=sa.String(length=50),
               nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.String(length=150),
               type_=sa.String(length=50),
               nullable=False)
        batch_op.alter_column('birth_date',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.drop_column('role')  # Удаление столбца 'role', если это предусмотрено
        batch_op.drop_column('password_hash')  # Удаление столбца 'password_hash', если это предусмотрено

    # Обновляем таблицу 'workout', если это необходимо
    with op.batch_alter_table('workout', schema=None) as batch_op:
        batch_op.alter_column('duration',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)
        batch_op.alter_column('calories',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)


def downgrade():
    # Откат изменений, если необходимо
    with op.batch_alter_table('workout', schema=None) as batch_op:
        batch_op.alter_column('calories',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.alter_column('duration',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=True))
        batch_op.alter_column('birth_date',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.String(length=50),
               type_=sa.String(length=150),
               nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=50),
               type_=sa.String(length=150),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=sa.String(length=150),
               nullable=True)
        batch_op.drop_column('password')  # Удаление столбца 'password', если это предусмотрено

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
