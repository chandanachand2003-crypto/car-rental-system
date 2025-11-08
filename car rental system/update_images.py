from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['car_rental']

# Update each car to use local image filename instead of URL
updates = [
    {'brand': 'Toyota', 'model': 'Innova Crysta', 'image': 'innova_crysta.jpg'},
    {'brand': 'Toyota', 'model': 'Fortuner', 'image': 'fortuner.jpg'},
    {'brand': 'Honda', 'model': 'City', 'image': 'honda_city.jpg'},
    {'brand': 'Honda', 'model': 'Amaze', 'image': 'honda_amaze.jpg'},
    {'brand': 'Hyundai', 'model': 'Creta', 'image': 'hyundai_creta.jpg'},
    {'brand': 'Hyundai', 'model': 'Alcazar', 'image': 'hyundai_alcazar.jpg'},
    {'brand': 'Maruti Suzuki', 'model': 'Ertiga', 'image': 'ertiga.jpg'},
    {'brand': 'Maruti Suzuki', 'model': 'Swift', 'image': 'swift.jpg'},
    {'brand': 'Tata', 'model': 'Nexon', 'image': 'nexon.jpg'},
    {'brand': 'Tata', 'model': 'Harrier', 'image': 'harrier.jpg'},
    {'brand': 'Mahindra', 'model': 'XUV700', 'image': 'xuv700.jpg'},
    {'brand': 'Mahindra', 'model': 'Scorpio-N', 'image': 'scorpio.jpg'},
    {'brand': 'Kia', 'model': 'Seltos', 'image': 'seltos.jpg'},
    {'brand': 'Kia', 'model': 'Carens', 'image': 'carens.jpg'},
    {'brand': 'Ford', 'model': 'EcoSport', 'image': 'ecosport.jpg'},
    {'brand': 'BMW', 'model': 'X5', 'image': 'bmw_x5.jpg'},
    {'brand': 'Mercedes-Benz', 'model': 'GLS', 'image': 'mercedes_gls.jpg'}
]

for update in updates:
    db.cars.update_one(
        {'brand': update['brand'], 'model': update['model']},
        {'$set': {'image': update['image']}}
    )
    print(f"✅ Updated {update['brand']} {update['model']} to use {update['image']}")

print("\n🎉 All car images updated to local files!")
