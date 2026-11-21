import os
from typing import TypeVar
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine, text, select

# Tipo genérico para aceptar cualquier modelo (Cpu, Gpu, Ram, etc.)
T = TypeVar("T", bound=SQLModel)


class Database:
    def __init__(self):
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        self.engine = create_engine(
            database_url,
            connect_args={"sslmode": "require"},
            pool_pre_ping=True,
        )

    def get_session(self):
        """Generador de sesiones para usar con Depends() en FastAPI."""
        with Session(self.engine) as session:
            yield session

    def check_connection(self, session: Session) -> str:
        """Verifica la conexión y devuelve la versión de PostgreSQL."""
        resultado = session.execute(text("SELECT version();")).first()
        return resultado[0] if resultado else "Desconocida"

    def crear_registro(self, session: Session, item: T) -> T:
        if hasattr(item, "id"):
            item.id = None
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    def obtener_todos(self, session: Session, modelo: type[T]) -> list[T]:
        """Devuelve una lista con todos los registros de la tabla indicada."""
        statement = select(modelo)
        return list(session.exec(statement).all())


# Instancia única (Singleton) para importar en toda la app
db = Database()