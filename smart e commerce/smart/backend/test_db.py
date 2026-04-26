from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:devi7977%40dhanush@localhost:3306/smart_ecommerce")

conn = engine.connect()
print("✅ Connected successfully!")
conn.close()