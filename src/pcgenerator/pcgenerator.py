from typing import List

from data.models import Cpu, Gpu, CasePc, Cooler, Ram, Psu, Storage, Motherboard
from pc.pc import PC


class PCGenerator:
    def __init__(self, cpus: List[Cpu], gpus: List[Gpu], casepc: List[CasePc],coolers: List[Cooler], ram: List[Ram], psus: List[Psu], storages: List[Storage], motherboards: List[Motherboard]):
        self.cpus = cpus
        self.gpus = gpus
        self.casepc = casepc
        self.coolers = coolers
        self.ram = ram
        self.psus = psus
        self.storages = storages
        self.motherboards = motherboards

    def generate(self, budget: int) -> List[PC]:
        pcs: List[PC] = []
        for cpu in self.cpus:
            if cpu.price > budget:
                continue
            price1 = cpu.price
            power1 = cpu.power
            for mother in self.motherboards:
                if price1 + mother.price > budget or cpu.power > mother.power:
                    continue
                if mother.ram_type != cpu.ram_type:
                    continue
                if mother.socket != cpu.socket:
                    continue
                price2 = price1 + mother.price
                for cooler in self.coolers:
                    if price2 + cooler.price > budget or cpu.power > cooler.power:
                        continue
                    price3 = price2 + cooler.price
                    for ram in self.ram:
                        if price3 + ram.price > budget:
                            continue
                        if ram.type != cpu.ram_type:
                            continue
                        price4 = price3 + ram.price
                        for gpu in self.gpus:
                            if price4 + gpu.price > budget:
                                continue
                            price5 = price4 + gpu.price
                            power2 = (power1 + gpu.power + 100) * 1.3
                            for storage in self.storages:
                                if price5 + storage.price > budget:
                                    continue
                                price6 = price5 + storage.price
                                for psu in self.psus:
                                    if power2 > psu.power or price6 + psu.price > budget:
                                        continue
                                    for case in self.casepc:
                                        if price6 + case.price > budget:
                                            continue
                                        new_pc = PC(cpu,gpu,case,cooler,ram,psu,storage,mother)
                                        if new_pc.price < budget:
                                            pcs.append(new_pc)
        return pcs