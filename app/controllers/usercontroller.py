from sqlalchemy.exc import IntegrityError
from app.utils.secury import encrypt_data
from app.database.configuration import Session, engine
from sqlalchemy.future import select
from app.database.schemas import User
import uuid

async def create_user(user: User) -> str:
  user.password = encrypt_data(user.password)
  # user.uuid = str(uuid.uuid4())

  # Abrindo uma sessão no banco
  async with Session() as s:
    try:
      s.add(user) # Adicionar usuário ao banco
      await s.commit() # Confirmando as alterações
      await s.refresh(user) # Recarregando os dados do usuário
    except Exception as e:
      await s.rollback() # Desfazer as alterações

      raise e # Retornar None

    return user.uuid # Retornando o UUID do usuário cadastrado

# Função que permite autenticar o usuário
async def authentication(email: str, password: str) -> dict:
  password = encrypt_data(password)

  # Abrindo uma sessão no banco
  async with Session() as s:
    query = await s.execute(
      select(User.uuid , User.name, User.email).where(User.email == email, User.password == password)
    ) # Selecionando alguns campos de usuário que tenha email e senha correspondente ao que foi passado

    return query.first()