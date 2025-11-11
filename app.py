from flask import Flask

# 1. Crea la aplicación
app = Flask(__name__)

# 2. Define la ruta principal (la "home")
@app.route('/')
def index():
    return "Hola. Mi servidor Flask está funcionando."

# 3. Código para arrancar el servidor (solo si ejecutamos este archivo)
if __name__ == '__main__':
    app.run(debug=True)