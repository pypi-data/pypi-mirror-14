from flask import Flask
from flask_graphql import GraphQL

from .blog.schema import blog_schema


def create_app():
    app = Flask(__name__)
    GraphQL(app, schema=blog_schema)
    return app


def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
