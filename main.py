from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# إنشاء قاعدة بيانات باستخدام SQLAlchemy
Base = declarative_base()

# تعريف الفئة (Category)
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # علاقة واحد إلى متعدد (One-to-Many) مع المنتجات
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

# تعريف الفئة (Product)
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    # علاقة مع الفئة (Category)
    category = relationship('Category', back_populates='products')
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, category_id={self.category_id})>"

# إنشاء الاتصال بقاعدة البيانات
engine = create_engine('sqlite:///store.db', echo=True)

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(engine)

# إنشاء الجلسة
Session = sessionmaker(bind=engine)
session = Session()

# CRUD-عمليات:

# 1. إنشاء الفئات والمنتجات (Create)
def create_category(name):
    category = Category(name=name)
    session.add(category)
    session.commit()
    print(f"Category '{name}' created.")

def create_product(name, price, category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if category:
        product = Product(name=name, price=price, category_id=category.id)
        session.add(product)
        session.commit()
        print(f"Product '{name}' created in category '{category_name}'.")
    else:
        print(f"Category '{category_name}' not found.")

# 2. قراءة المنتجات حسب الفئة (Read)
def read_products_by_category(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if category:
        products = category.products
        for product in products:
            print(product)
    else:
        print(f"Category '{category_name}' not found.")

# 3. تحديث الفئة المرتبطة بالمنتج (Update)
def update_product_category(product_name, new_category_name):
    product = session.query(Product).filter_by(name=product_name).first()
    if product:
        new_category = session.query(Category).filter_by(name=new_category_name).first()
        if new_category:
            product.category_id = new_category.id
            session.commit()
            print(f"Product '{product_name}' updated to category '{new_category_name}'.")
        else:
            print(f"Category '{new_category_name}' not found.")
    else:
        print(f"Product '{product_name}' not found.")

# 4. حذف الفئة مع جميع المنتجات المرتبطة (Delete)
def delete_category(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if category:
        session.delete(category)
        session.commit()
        print(f"Category '{category_name}' and its products have been deleted.")
    else:
        print(f"Category '{category_name}' not found.")

# أمثلة على استخدام CRUD-عمليات:
create_category('Electronics')
create_category('Clothing')

create_product('Laptop', 1000, 'Electronics')
create_product('Smartphone', 700, 'Electronics')
create_product('T-shirt', 20, 'Clothing')

print("\nProducts in 'Electronics' category:")
read_products_by_category('Electronics')

print("\nUpdating 'Laptop' to 'Clothing' category:")
update_product_category('Laptop', 'Clothing')

print("\nProducts in 'Clothing' category after update:")
read_products_by_category('Clothing')

print("\nDeleting 'Electronics' category:")
delete_category('Electronics')

print("\nProducts in 'Electronics' category after deletion:")
read_products_by_category('Electronics')

# غلق الجلسة
session.close()
