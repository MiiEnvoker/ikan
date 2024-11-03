from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data ikan hias contoh
fishes = [
    {"id": 1, "name": "Ikan Koi", "description": "Ikan koi dengan warna yang indah", "price": 50000, "stock": 10, "size": "10 cm", "species": "Cyprinus carpio"},
    {"id": 2, "name": "Ikan Guppy", "description": "Ikan kecil dengan ekor berwarna-warni", "price": 15000, "stock": 20, "size": "3 cm", "species": "Poecilia reticulata"},
    {"id": 3, "name": "Ikan Cupang", "description": "Ikan cupang hias dengan sirip lebar", "price": 25000, "stock": 30, "size": "5 cm", "species": "Betta splendens"},
    {"id": 4, "name": "Ikan Arwana", "description": "Ikan arwana dengan sisik berkilau", "price": 200000, "stock": 5, "size": "30 cm", "species": "Scleropages formosus"},
    {"id": 5, "name": "Ikan Neon Tetra", "description": "Ikan kecil dengan garis neon", "price": 10000, "stock": 40, "size": "2 cm", "species": "Paracheirodon innesi"},
    {"id": 6, "name": "Ikan Oscar", "description": "Ikan besar dan kuat dengan warna hitam", "price": 60000, "stock": 15, "size": "20 cm", "species": "Astronotus ocellatus"},
    {"id": 7, "name": "Ikan Molly", "description": "Ikan molly dengan warna beragam", "price": 12000, "stock": 25, "size": "5 cm", "species": "Poecilia sphenops"},
    {"id": 8, "name": "Ikan Discus", "description": "Ikan berbentuk pipih dengan pola menarik", "price": 80000, "stock": 12, "size": "15 cm", "species": "Symphysodon aequifasciatus"},
    {"id": 9, "name": "Ikan Black Ghost", "description": "Ikan unik berwarna hitam", "price": 45000, "stock": 18, "size": "10 cm", "species": "Apteronotus albifrons"},
    {"id": 10, "name": "Ikan Louhan", "description": "Ikan louhan dengan kepala jenong", "price": 150000, "stock": 8, "size": "25 cm", "species": "Flowerhorn cichlid"}
]

class FishList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(fishes),
            "fishes": fishes
        }

    def post(self):
        data = request.get_json()
        new_fish = {
            "id": len(fishes) + 1,
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "stock": data["stock"],
            "size": data["size"],
            "species": data["species"]
        }
        fishes.append(new_fish)
        return {"error": False, "message": "Fish added", "fish": new_fish}, 201

class FishDetail(Resource):
    def get(self, fish_id):
        fish = next((f for f in fishes if f["id"] == fish_id), None)
        if fish:
            return {"error": False, "message": "success", "fish": fish}
        return {"error": True, "message": "Fish not found"}, 404

    def put(self, fish_id):
        data = request.get_json()
        fish = next((f for f in fishes if f["id"] == fish_id), None)
        if fish:
            fish.update({
                "name": data["name"],
                "description": data["description"],
                "price": data["price"],
                "stock": data["stock"],
                "size": data["size"],
                "species": data["species"]
            })
            return {"error": False, "message": "Fish updated", "fish": fish}
        return {"error": True, "message": "Fish not found"}, 404

    def delete(self, fish_id):
        global fishes
        fishes = [f for f in fishes if f["id"] != fish_id]
        return {"error": False, "message": "Fish deleted"}

class FishSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [f for f in fishes if query in f['name'].lower() or query in f['description'].lower()]
        return {"error": False, "founded": len(result), "fishes": result}

api.add_resource(FishList, '/fishes')
api.add_resource(FishDetail, '/fishes/<int:fish_id>')
api.add_resource(FishSearch, '/fishes/search')

if __name__ == '__main__':
    app.run(debug=True)
