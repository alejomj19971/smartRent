from database  import Base
from sqlalchemy import Column,Integer,String,Boolean
class Casas(Base):
    __tablename__ = 'casas'
    
    id=Column(Integer,primary_key=True,index=True)
    title= Column(String)
    price= Column(Integer)
    toilet= Column(Integer)
    bedroom=Column(Integer)
    squareMeters= Column(Integer)
    parking= Column(Integer)
    active=Column(Boolean,default=False)



