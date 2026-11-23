from pydantic import BaseModel

from data.models import Cpu, Gpu, CasePc, Cooler, Ram, Psu, Storage, Motherboard, FullPcBuild
class Ids:
    def __init__(self, cpu_id: int, gpu_id: int, case_id: int, cooler_id: int, ram_id: int, psu_id: int, storage_id: int, motherboard_id: int):
        self.cpu_id = cpu_id
        self.gpu_id = gpu_id
        self.case_id = case_id
        self.cooler_id = cooler_id
        self.ram_id = ram_id
        self.psu_id = psu_id
        self.storage_id = storage_id
        self.motherboard_id = motherboard_id

class BudgetIds:
    def __init__(self, cpu_id: int, case_id: int, ram_id: int, psu_id: int, storage_id: int, motherboard_id: int):
        self.cpu_id = cpu_id
        self.case_id = case_id
        self.ram_id = ram_id
        self.psu_id = psu_id
        self.storage_id = storage_id
        self.motherboard_id = motherboard_id

class PC:
    def __init__(self, cpu: Cpu, gpu: Gpu, case: CasePc, cooler: Cooler, ram: Ram, psu: Psu, storage: Storage, motherboard: Motherboard):
        self.cpu = cpu
        self.gpu = gpu
        self.case = case
        self.cooler = cooler
        self.ram = ram
        self.psu = psu
        self.storage = storage
        self.motherboard = motherboard
        self.price = self.cpu.price + self.motherboard.price + self.cooler.price + self.ram.price + self.gpu.price + self.storage.price + self. psu.price + self.case.price

    def get_ids(self) -> Ids | None:
        if self.cpu.id is None:
            return None
        if self.gpu.id is None:
            return None
        if self.case.id is None:
            return None
        if self.cooler.id is None:
            return None
        if self.ram.id is None:
            return None
        if self.psu.id is None:
            return None
        if self.storage.id is None:
            return None
        if self.motherboard.id is None:
            return None
        return Ids(self.cpu.id, self.gpu.id, self.case.id, self.cooler.id, self.ram.id, self.psu.id, self.storage.id, self.motherboard.id)

    def to_full_pc_build(self, budget) -> FullPcBuild | None:
        ids = self.get_ids()
        if ids is None:
            return None

        return FullPcBuild(
            cpu_id=ids.cpu_id,
            motherboard_id=ids.motherboard_id,
            cooler_id=ids.cooler_id,
            ram_id=ids.ram_id,
            gpu_id=ids.gpu_id,
            storage_id=ids.storage_id,
            psu_id=ids.psu_id,
            casepc_id=ids.case_id,
            cpu_general_performance=self.cpu.general_performance,
            cpu_gaming_performance=self.cpu.gaming_performance,
            gpu_gaming_performance=self.gpu.gaming_performance,
            gpu_productivity_performance=self.gpu.productivity_performance,
            vram=self.gpu.vram,
            upgradable=self.cpu.upgradable,
            rgb=self.case.rgb,
            noise=self.cooler.noise,
            ports=self.motherboard.ports,
            wifi=self.motherboard.wifi,
            ethernet=self.motherboard.ethernet,
            nvme=self.motherboard.nvme,
            rating=self.psu.rating,
            ram_capacity=self.ram.capacity,
            ram_speed=self.ram.speed,
            storage_capacity=self.storage.capacity,
            storage_speed=self.storage.speed,
            price= 1 + (self.price*10 // budget),
        )
    def to_pc_build(self, score) -> PcBuild:
        return PcBuild(
            cpu_model=self.cpu.model,
            cpu_link= self.cpu.url,
            motherboard_model=self.motherboard.model,
            motherboard_link=self.motherboard.url,
            cooler_model=self.cooler.model,
            cooler_link=self.cooler.url,
            ram_model=self.ram.model,
            ram_link=self.ram.url,
            ram_sticks=self.ram.sticks,
            gpu_model=self.gpu.model,
            gpu_link=self.gpu.url,
            storage_model=self.storage.model,
            storage_link=self.storage.url,
            psu_model=self.psu.model,
            psu_link=self.psu.url,
            case_model=self.case.model,
            case_link=self.case.url,
            price=self.price,
            score=score,
        )

class BudgetPc:
    def __init__(self, cpu: Cpu, case: CasePc, ram: Ram, psu: Psu, storage: Storage, motherboard: Motherboard):
        self.cpu = cpu
        self.case = case
        self.ram = ram
        self.psu = psu
        self.storage = storage
        self.motherboard = motherboard
        self.price = self.cpu.price + self.motherboard.price + self.ram.price + self.storage.price + self. psu.price + self.case.price

    def get_ids(self) -> BudgetIds | None:
        if self.cpu.id is None:
            return None
        if self.case.id is None:
            return None
        if self.ram.id is None:
            return None
        if self.psu.id is None:
            return None
        if self.storage.id is None:
            return None
        if self.motherboard.id is None:
            return None
        return BudgetIds(self.cpu.id, self.case.id, self.ram.id, self.psu.id, self.storage.id, self.motherboard.id)

    def to_full_pc_build(self, budget) -> FullPcBuild | None:
        ids = self.get_ids()
        if ids is None:
            return None

        return FullPcBuild(
            cpu_id=ids.cpu_id,
            motherboard_id=ids.motherboard_id,
            cooler_id=ids.cpu_id,
            ram_id=ids.ram_id,
            gpu_id=ids.cpu_id,
            storage_id=ids.storage_id,
            psu_id=ids.psu_id,
            casepc_id=ids.case_id,
            cpu_general_performance=self.cpu.general_performance,
            cpu_gaming_performance=self.cpu.gaming_performance,
            gpu_gaming_performance=self.cpu.igpu_performance,
            gpu_productivity_performance=self.cpu.igpu_performance,
            vram=2,
            upgradable=self.cpu.upgradable,
            rgb=self.case.rgb,
            noise=10,
            ports=self.motherboard.ports,
            wifi=self.motherboard.wifi,
            ethernet=self.motherboard.ethernet,
            nvme=self.motherboard.nvme,
            rating=self.psu.rating,
            ram_capacity=self.ram.capacity,
            ram_speed=self.ram.speed,
            storage_capacity=self.storage.capacity,
            storage_speed=self.storage.speed,
            price= 1 + (self.price*10 // budget),
        )
    def to_pc_build(self, score) -> PcBuild:
        return PcBuild(
            cpu_model=self.cpu.model,
            cpu_link= self.cpu.url,
            motherboard_model=self.motherboard.model,
            motherboard_link=self.motherboard.url,
            cooler_model="Stock Cooler",
            cooler_link=self.cpu.url,
            ram_model=self.ram.model,
            ram_link=self.ram.url,
            ram_sticks=self.ram.sticks,
            gpu_model="iGPU",
            gpu_link=self.cpu.url,
            storage_model=self.storage.model,
            storage_link=self.storage.url,
            psu_model=self.psu.model,
            psu_link=self.psu.url,
            case_model=self.case.model,
            case_link=self.case.url,
            price=self.price,
            score=score,
        )

class PcBuild(BaseModel):
    cpu_model: str
    cpu_link: str
    motherboard_model: str
    motherboard_link: str
    cooler_model: str
    cooler_link: str
    ram_model: str
    ram_link: str
    ram_sticks: int
    gpu_model: str
    gpu_link: str
    storage_model: str
    storage_link: str
    psu_model: str
    psu_link: str
    case_model: str
    case_link: str
    price: int
    score: float
