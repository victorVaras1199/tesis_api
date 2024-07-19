from flask import Flask, request, jsonify

app = Flask(__name__)

books = [
	{
		"id": 1,
		"title": "1984",
		"author": "George Orwell"
	},
	{
		"id": 2,
		"title": "Cien años de soledad",
		"author": "Gabriel García Márquez"
	}
]

# Ruta para obtener todos los libros
@app.route('/books', methods=['GET'])
def obtener_libros():
	return jsonify(books)

if __name__ == '__main__':
	app.run(debug=True)
