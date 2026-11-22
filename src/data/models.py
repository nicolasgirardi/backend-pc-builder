from sqlmodel import Field, SQLModel


class Cpu(SQLModel, table=True):
    __tablename__ = "cpu"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    general_performance: int
    gaming_performance: int
    power: int
    igpu: bool = False
    igpu_performance: int = 0
    socket: str
    ram_type: str
    cooler: bool = False
    upgradable: int


class Motherboard(SQLModel, table=True):
    __tablename__ = "motherboard"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    socket: str
    ram_type: str
    ports: int
    wifi: int
    ethernet: int
    power: int
    nvme: int


class Cooler(SQLModel, table=True):
    __tablename__ = "cooler"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    noise: int
    power: int


class Ram(SQLModel, table=True):
    __tablename__ = "ram"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    type: str
    capacity: int
    speed: int
    sticks: int


class Gpu(SQLModel, table=True):
    __tablename__ = "gpu"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    gaming_performance: int
    productivity_performance: int
    power: int
    vram: int
    technologies: int


class Storage(SQLModel, table=True):
    __tablename__ = "storage"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    capacity: int
    speed: int


class Psu(SQLModel, table=True):
    __tablename__ = "psu"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    power: int
    rating: int


class CasePc(SQLModel, table=True):
    __tablename__ = "casepc"

    id: int | None = Field(default=None, primary_key=True)
    model: str
    price: int
    url: str
    rgb: int

class FullPcBuild(SQLModel, table=True):
    __tablename__ = "full_pc_build"

    cpu_id: int = Field(foreign_key="cpu.id", primary_key=True)
    motherboard_id: int = Field(foreign_key="motherboard.id", primary_key=True)
    cooler_id: int = Field(foreign_key="cooler.id", primary_key=True)
    ram_id: int = Field(foreign_key="ram.id", primary_key=True)
    gpu_id: int = Field(foreign_key="gpu.id", primary_key=True)
    storage_id: int = Field(foreign_key="storage.id", primary_key=True)
    psu_id: int = Field(foreign_key="psu.id", primary_key=True)
    casepc_id: int = Field(foreign_key="casepc.id", primary_key=True)

    cpu_general_performance: int
    cpu_gaming_performance: int
    upgradable: int
    gpu_gaming_performance: int
    gpu_productivity_performance: int
    vram: int
    rgb: int
    noise: int
    ports: int
    wifi: int
    ethernet: int
    nvme: int
    rating: int
    ram_capacity: int
    ram_speed: int
    storage_capacity: int
    storage_speed: int
    price: int