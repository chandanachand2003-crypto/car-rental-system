from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['car_rental']

# Clear existing cars
db.cars.delete_many({})

# Car data with local image filenames
cars_data = [
    {
        'brand': 'Toyota', 'model': 'Innova Crysta', 'seats': 7, 'rent': 2500,
        'mileage': 13.0, 'fuel_type': 'Diesel', 'transmission': 'Manual/Automatic',
        'engine': '2.4L Diesel, 2393cc', 'image': 'innova_crysta.jpg', 'available': True
    },
    {
        'brand': 'Toyota', 'model': 'Fortuner', 'seats': 7, 'rent': 4500,
        'mileage': 14.0, 'fuel_type': 'Diesel', 'transmission': 'Manual/Automatic',
        'engine': '2.8L Diesel, 2755cc', 'image': 'fortuner.jpg', 'available': True
    },
    {
        'brand': 'Honda', 'model': 'City', 'seats': 5, 'rent': 1800,
        'mileage': 18.4, 'fuel_type': 'Petrol', 'transmission': 'CVT',
        'engine': '1.5L Petrol, 1497cc', 'image': 'honda_city.jpg', 'available': True
    },
    {
        'brand': 'Honda', 'model': 'Amaze', 'seats': 5, 'rent': 1500,
        'mileage': 18.65, 'fuel_type': 'Petrol', 'transmission': 'CVT',
        'engine': '1.2L Petrol, 1199cc', 'image': 'honda_amaze.jpg', 'available': True
    },
    {
        'brand': 'Hyundai', 'model': 'Creta', 'seats': 5, 'rent': 2200,
        'mileage': 17.0, 'fuel_type': 'Petrol', 'transmission': 'Manual/Automatic',
        'engine': '1.5L Petrol, 1497cc', 'image': 'hyundai_creta.jpg', 'available': True
    },
    {
        'brand': 'Hyundai', 'model': 'Alcazar', 'seats': 7, 'rent': 2800,
        'mileage': 18.1, 'fuel_type': 'Petrol', 'transmission': 'Automatic',
        'engine': '1.5L Petrol, 1482cc', 'image': 'hyundai_alcazar.jpg', 'available': True
    },
    {
        'brand': 'Maruti Suzuki', 'model': 'Ertiga', 'seats': 7, 'rent': 1600,
        'mileage': 20.51, 'fuel_type': 'Petrol', 'transmission': 'Manual/Automatic',
        'engine': '1.5L Petrol, 1462cc', 'image': 'ertiga.jpg', 'available': True
    },
    {
        'brand': 'Maruti Suzuki', 'model': 'Swift', 'seats': 5, 'rent': 1200,
        'mileage': 24.80, 'fuel_type': 'Petrol', 'transmission': 'Manual/AMT',
        'engine': '1.2L Petrol, 1197cc', 'image': 'swift.jpg', 'available': True
    },
    {
        'brand': 'Tata', 'model': 'Nexon', 'seats': 5, 'rent': 1700,
        'mileage': 17.44, 'fuel_type': 'Petrol', 'transmission': 'Manual/AMT',
        'engine': '1.2L Turbo Petrol, 1199cc', 'image': 'nexon.jpg', 'available': True
    },
    {
        'brand': 'Tata', 'model': 'Harrier', 'seats': 5, 'rent': 2600,
        'mileage': 16.8, 'fuel_type': 'Diesel', 'transmission': 'Manual/Automatic',
        'engine': '2.0L Diesel, 1956cc', 'image': 'harrier.jpg', 'available': True
    },
    {
        'brand': 'Mahindra', 'model': 'XUV700', 'seats': 7, 'rent': 3200,
        'mileage': 16.57, 'fuel_type': 'Diesel', 'transmission': 'Manual/Automatic',
        'engine': '2.2L Diesel, 2184cc', 'image': 'xuv700.jpg', 'available': True
    },
    {
        'brand': 'Mahindra', 'model': 'Scorpio-N', 'seats': 7, 'rent': 3000,
        'mileage': 15.94, 'fuel_type': 'Diesel', 'transmission': 'Manual/Automatic',
        'engine': '2.2L Diesel, 2184cc', 'image': 'scorpio.jpg', 'available': True
    },
    {
        'brand': 'Kia', 'model': 'Seltos', 'seats': 5, 'rent': 2300,
        'mileage': 17.0, 'fuel_type': 'Petrol', 'transmission': 'Manual/Automatic',
        'engine': '1.5L Petrol, 1497cc', 'image': 'seltos.jpg', 'available': True
    },
    {
        'brand': 'Kia', 'model': 'Carens', 'seats': 7, 'rent': 2400,
        'mileage': 15.58, 'fuel_type': 'Petrol', 'transmission': 'Manual/Automatic',
        'engine': '1.5L Petrol, 1497cc', 'image': 'carens.jpg', 'available': True
    },
    {
        'brand': 'Ford', 'model': 'EcoSport', 'seats': 5, 'rent': 1900,
        'mileage': 15.9, 'fuel_type': 'Petrol', 'transmission': 'Manual/Automatic',
        'engine': '1.5L Petrol, 1497cc', 'image': 'ecosport.jpg', 'available': True
    },
    {
        'brand': 'BMW', 'model': 'X5', 'seats': 5, 'rent': 8000,
        'mileage': 12.0, 'fuel_type': 'Diesel', 'transmission': 'Automatic',
        'engine': '3.0L Diesel, 2993cc', 'image': 'bmw_x5.jpg', 'available': True
    },
    {
        'brand': 'Mercedes-Benz', 'model': 'GLS', 'seats': 7, 'rent': 12000,
        'mileage': 12.0, 'fuel_type': 'Diesel', 'transmission': 'Automatic',
        'engine': '3.0L Diesel, 2925cc', 'image': 'mercedes_gls.jpg', 'available': True
    }
]

# Insert all cars
result = db.cars.insert_many(cars_data)
print(f"✅ Successfully inserted {len(result.inserted_ids)} cars into the database!")

print("\n📋 Cars in database:")
for car in db.cars.find():
    print(f"  • {car['brand']} {car['model']} - ₹{car['rent']}/day - {car['mileage']} kmpl")

print("\n🎉 Database populated successfully!")
print("\nNote: Make sure to download and place car images in the 'uploads/' folder")
print("Image filenames needed:")
for car in cars_data:
    print(f"  - {car['image']}")
