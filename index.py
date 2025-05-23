from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

datos_path = os.path.join(os.path.dirname(__file__), 'Datos')
lista = []

def create_route(file):
    def serve_json():
        file_path = os.path.join(datos_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Obtener parámetros GET
        filters = request.args.to_dict()

        # Si hay filtros, aplicar
        if filters:
            if isinstance(data, list):
                # Filtrar solo si es una lista de objetos
                filtered = [
                    item for item in data
                    if all(str(item.get(k, '')).strip().lower() == str(v).strip().lower() for k, v in filters.items())
                ]
                return jsonify(filtered)
            else:
                return jsonify({"error": "El contenido del archivo no es una lista filtrable", "contenido": data})

        return jsonify(data)

    return serve_json

for filename in os.listdir(datos_path):
    if filename.endswith('.json'):
        route_name = f"/{filename.replace('.json', '')}"
        lista.append(route_name)
        app.add_url_rule(route_name, endpoint=route_name, view_func=create_route(filename))

@app.route('/')
def root():
    return jsonify({
        "message": "API Nunsys activa.",
        "rutas_disponibles": lista
    })

if __name__ == '__main__':
    app.run(debug=True)
