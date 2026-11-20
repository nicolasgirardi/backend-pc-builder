import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, create_engine, text
from data.models import Cpu, Gpu, CasePc, Cooler, Ram, Psu, Storage, Motherboard

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True  # Verifica que la conexión siga viva (muy útil en el plan gratuito de Render)
)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# 3. Inicializar FastAPI
app = FastAPI()

# 4. Endpoints sobre tus datos existentes
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/ping-db")
def probar_conexion_bd(session: SessionDep):
    try:
        resultado = session.execute(text("SELECT version();")).first()
        return {
            "estado": "Conectado exitosamente a Render",
            "postgres_version": resultado[0] if resultado else "Desconocida"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al conectar con la base de datos: {str(e)}"
        )


@app.post("/cpu/", response_model=Cpu, status_code=status.HTTP_201_CREATED)
def crear_cpu(cpu:Cpu, session: SessionDep):
    cpu.id = None
    session.add(cpu)
    session.commit()
    session.refresh(cpu)  # Recupera el ID asignado por la base de datos
    return cpu

@app.post("/motherboard/", response_model=Motherboard, status_code=status.HTTP_201_CREATED)
def crear_motherboard(motherboard: Motherboard, session: SessionDep):
    motherboard.id = None
    session.add(motherboard)
    session.commit()
    session.refresh(motherboard)  # Recupera el ID asignado por la base de datos
    return motherboard


@app.post("/cooler/", response_model=Cooler, status_code=status.HTTP_201_CREATED)
def crear_cooler(cooler: Cooler, session: SessionDep):
    cooler.id = None
    session.add(cooler)
    session.commit()
    session.refresh(cooler)
    return cooler


@app.post("/ram/", response_model=Ram, status_code=status.HTTP_201_CREATED)
def crear_ram(ram: Ram, session: SessionDep):
    ram.id = None
    session.add(ram)
    session.commit()
    session.refresh(ram)
    return ram


@app.post("/gpu/", response_model=Gpu, status_code=status.HTTP_201_CREATED)
def crear_gpu(gpu: Gpu, session: SessionDep):
    gpu.id = None
    session.add(gpu)
    session.commit()
    session.refresh(gpu)
    return gpu


@app.post("/storage/", response_model=Storage, status_code=status.HTTP_201_CREATED)
def crear_storage(storage: Storage, session: SessionDep):
    storage.id = None
    session.add(storage)
    session.commit()
    session.refresh(storage)
    return storage


@app.post("/psu/", response_model=Psu, status_code=status.HTTP_201_CREATED)
def crear_psu(psu: Psu, session: SessionDep):
    psu.id = None
    session.add(psu)
    session.commit()
    session.refresh(psu)
    return psu


@app.post("/casepc/", response_model=CasePc, status_code=status.HTTP_201_CREATED)
def crear_casepc(casepc: CasePc, session: SessionDep):
    casepc.id = None
    session.add(casepc)
    session.commit()
    session.refresh(casepc)
    return casepc