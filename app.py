import os
from config import app,db
from sorveteria.sorvetes_routes import sorvetes_blueprint

app.register_blueprint(sorvetes_blueprint)

with app.app_context():
    db.create_all()
    

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )