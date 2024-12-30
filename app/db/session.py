
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_name}"


engine:AsyncEngine = create_async_engine(sqlite_url,echo=True)
# Configura un creador de sesiones asíncronas
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Inicializar la base de datos
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Función de dependencia para obtener la sesión
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

