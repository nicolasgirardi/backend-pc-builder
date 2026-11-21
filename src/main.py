from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Query
from sqlmodel import Session
from database.database import db
from data.models import Cpu, Gpu, CasePc, Cooler, Ram, Psu, Storage, Motherboard, FullPcBuild
from pc.pc import PcBuild
from topsis.topsis import best_pcs, Categories
from pcgenerator.pcgenerator import PCGenerator

SessionDep = Annotated[Session, Depends(db.get_session)]

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/ping-db")
def probar_conexion_bd(session: SessionDep):
    try:
        version = db.check_connection(session)
        return {
            "estado": "Conectado exitosamente a Render",
            "postgres_version": version,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al conectar con la base de datos: {str(e)}",
        )


@app.post("/cpu/", response_model=Cpu, status_code=status.HTTP_201_CREATED)
def crear_cpu(cpu: Cpu, session: SessionDep):
    return db.crear_registro(session, cpu)


@app.post("/motherboard/", response_model=Motherboard, status_code=status.HTTP_201_CREATED)
def crear_motherboard(motherboard: Motherboard, session: SessionDep):
    return db.crear_registro(session, motherboard)


@app.post("/cooler/", response_model=Cooler, status_code=status.HTTP_201_CREATED)
def crear_cooler(cooler: Cooler, session: SessionDep):
    return db.crear_registro(session, cooler)


@app.post("/ram/", response_model=Ram, status_code=status.HTTP_201_CREATED)
def crear_ram(ram: Ram, session: SessionDep):
    return db.crear_registro(session, ram)


@app.post("/gpu/", response_model=Gpu, status_code=status.HTTP_201_CREATED)
def crear_gpu(gpu: Gpu, session: SessionDep):
    return db.crear_registro(session, gpu)


@app.post("/storage/", response_model=Storage, status_code=status.HTTP_201_CREATED)
def crear_storage(storage: Storage, session: SessionDep):
    return db.crear_registro(session, storage)


@app.post("/psu/", response_model=Psu, status_code=status.HTTP_201_CREATED)
def crear_psu(psu: Psu, session: SessionDep):
    return db.crear_registro(session, psu)


@app.post("/casepc/", response_model=CasePc, status_code=status.HTTP_201_CREATED)
def crear_casepc(casepc: CasePc, session: SessionDep):
    return db.crear_registro(session, casepc)

@app.get("/cpu/", response_model=list[Cpu])
def listar_cpus(session: SessionDep):
    return db.obtener_todos(session, Cpu)


@app.get("/motherboard/", response_model=list[Motherboard])
def listar_motherboards(session: SessionDep):
    return db.obtener_todos(session, Motherboard)


@app.get("/cooler/", response_model=list[Cooler])
def listar_coolers(session: SessionDep):
    return db.obtener_todos(session, Cooler)


@app.get("/ram/", response_model=list[Ram])
def listar_rams(session: SessionDep):
    return db.obtener_todos(session, Ram)


@app.get("/gpu/", response_model=list[Gpu])
def listar_gpus(session: SessionDep):
    return db.obtener_todos(session, Gpu)


@app.get("/storage/", response_model=list[Storage])
def listar_storages(session: SessionDep):
    return db.obtener_todos(session, Storage)


@app.get("/psu/", response_model=list[Psu])
def listar_psus(session: SessionDep):
    return db.obtener_todos(session, Psu)


@app.get("/casepc/", response_model=list[CasePc])
def listar_casepcs(session: SessionDep):
    return db.obtener_todos(session, CasePc)

@app.get("/best-pcs/", response_model=list[PcBuild])
def listar_best_pcs(
        categories: Annotated[Categories, Query()],
        budget: int,
        session: SessionDep,
):
    cpu = db.obtener_todos(session, Cpu)
    mother = db.obtener_todos(session, Motherboard)
    cooler = db.obtener_todos(session, Cooler)
    ram = db.obtener_todos(session, Ram)
    gpu = db.obtener_todos(session, Gpu)
    storage = db.obtener_todos(session, Storage)
    psu = db.obtener_todos(session, Psu)
    casepc = db.obtener_todos(session, CasePc)
    generator = PCGenerator(cpu, gpu, casepc, cooler,ram, psu, storage, mother)
    weights = list(categories.model_dump().values())
    pcs = generator.generate(budget)
    full_build_list = []
    for pc in pcs:
        new_pc = pc.to_full_pc_build(categories.price)
        if new_pc is None:
            continue
        full_build_list.append(new_pc)
    results = best_pcs(full_build_list, weights)
    final_results = []
    for index, score in results:
        final_results.append(pcs[index].to_pc_build(score))
    return final_results