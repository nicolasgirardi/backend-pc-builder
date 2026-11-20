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