from flask import Flask
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.sql import text

from client.database import db
from client.database import MetadataModel


def execute_sql(op, sql):
    """Executes raw SQL in the database"""
    conn = op.get_bind()
    conn.execute(text(sql))


def delete_all_rows(app):
    """Delete all instances without dropping the tables."""
    with app.app_context():
        try:
            for tbl in reversed(MetadataModel.metadata.sorted_tables):
                db.session.execute(tbl.delete())
            db.session.commit()
        except ResourceClosedError:
            pass
