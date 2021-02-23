from sqlalchemy import create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    discount_percent = Column(Integer)

    def __repr__(self):
        return "<Product(name='%s', description='%s', price='%s', discount_percent='%s')>" % (self.name, self.description, self.price, self.discount_percent)


def initializeDataBase():
    Base.metadata.create_all(engine) #TO CREATE TABLES (ALL CLASSES IN HERE)
    # createSession()

# def createSession():
#     session = Session()    

def getProductById(productId):
    product = session.query(Product).filter_by(id=productId).first()
    return product

def getProducts():
    products = session.query(Product).filter_by().all()
    return products

def addProduct(name, description, price, discount_percent):
    newProduct = Product(name=name, description=description, price=price, discount_percent=discount_percent)
    session.add(newProduct)
    # session.new # RETURN ALL THE NEW PRODUCTS CREATED SO FAR
    session.commit()
    
def addProducts():
    return None
    # session.add_all([
    # Product(name="bike XML", description="Red bike", price=100.00, discout_percent=10),
    # Product(name="bike OLX", description="Blue bike", price=200.00, discout_percent=10),
    # Product(name="bike GAP", description="Green bike", price=150.00, discout_percent=10)])

def updateProduct(productId, name, description, price, discount_percent):
    product = session.query(Product).filter_by(id=productId).first()
    product.name = name
    product.description = description
    product.price = price
    product.discount_percent = discount_percent
    # session.dirty #RETURNS ALL THE UPDATES IN PRODUCTS SO FAR
    session.commit()

def deleteProduct(productId):
    product = session.query(Product).filter_by(id=productId).first()
    session.delete(product)
    session.commit()

def rollback():
    existingProduct = Product(name="Nome Correto", description="Descrição correta", price=50.00, discout_percent=10)
    existingProduct.name = 'Nome Correto Errado'
    session.add(existingProduct)
    fakeProduct = Product(name="Nome Errado", description="Descrição correta", price=50.00, discout_percent=10)
    session.add(fakeProduct)
    
    session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all() #WILL GET: "NOME CORRETO ERRADO" & "NOME ERRADO"
    
    session.rollback() #THAT WILL ROLLBACK 
    

initializeDataBase()
addProduct("Bike Maneira", "Vermelha", 150, 10)
addProduct("Bike Méh", "Azul", 150, 10)

for instance in session.query(Product).order_by(Product.id):
    print(instance.id, instance.name, instance.description)

deleteProduct(2)

for instance in session.query(Product).order_by(Product.id):
    print(instance.id, instance.name, instance.description)

# COMO PERSISTIR OS DADOS? COMO DEIXAR A APLICAÇÃO RODANDO? PRECISO DE UM SERVIDOR RODANDO EM UMA PORTA COM ESSE CÓDIGO?
# - POSSO COLOCAR TUDO DENTRO DA API-FLASK