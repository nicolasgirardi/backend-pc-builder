import gc
import numpy as np
from pydantic import BaseModel
from data.models import FullPcBuild
from pc.pc import PcBuild


class Categories(BaseModel):
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

    def to_weights_list(self) -> list[int]:
        return [
            self.cpu_general_performance,
            self.cpu_gaming_performance,
            self.upgradable,
            self.gpu_gaming_performance,
            self.gpu_productivity_performance,
            self.vram,
            self.rgb,
            self.noise,
            self.ports,
            self.wifi,
            self.ethernet,
            self.nvme,
            self.rating,
            self.ram_capacity,
            self.ram_speed,
            self.storage_capacity,
            self.storage_speed,
            self.price,
        ]


CRITERIOS = [
    "cpu_general_performance",
    "cpu_gaming_performance",
    "upgradable",
    "gpu_gaming_performance",
    "gpu_productivity_performance",
    "vram",
    "rgb",
    "noise",
    "ports",
    "wifi",
    "ethernet",
    "nvme",
    "rating",
    "ram_capacity",
    "ram_speed",
    "storage_capacity",
    "storage_speed",
    "price",
]

impact = [
    "+",  # cpu_general_performance
    "+",  # cpu_gaming_performance
    "+",  # Upgradable
    "+",  # gpu_gaming_performance
    "+",  # gpu_productivity_performance
    "+",  # vram
    "+",  # rgb
    "-",  # noise
    "+",  # ports
    "+",  # wifi
    "+",  # ethernet
    "+",  # nvme
    "+",  # rating
    "+",  # ram_capacity
    "+",  # ram_speed
    "+",  # storage_capacity
    "+",  # storage_speed
    "-",  # price
]


def topsis(
        decision_matrix, weights, impacts, top_n: int = 5
) -> list[tuple[int, float]]:
    x = np.array(decision_matrix, dtype=np.float32)
    w = np.array(weights, dtype=np.float32)

    # Validaciones básicas
    if x.shape[1] != len(w) or x.shape[1] != len(impacts):
        raise ValueError(
            "El número de criterios debe coincidir con los pesos e impactos."
        )

    # 1. Normalización vectorial (protegida contra columnas en cero)
    norma = np.sqrt(np.sum(x ** 2, axis=0))
    norma[norma == 0] = 1.0
    r = x / norma

    # 2. Matriz normalizada ponderada
    v = r * w

    # 3. Determinar soluciones ideales positiva (A+) y negativa (A-)
    ideal_pos = np.zeros(x.shape[1])
    ideal_neg = np.zeros(x.shape[1])

    for j in range(x.shape[1]):
        if impacts[j] == "+":
            ideal_pos[j] = np.max(v[:, j])
            ideal_neg[j] = np.min(v[:, j])
        elif impacts[j] == "-":
            ideal_pos[j] = np.min(v[:, j])
            ideal_neg[j] = np.max(v[:, j])
        else:
            raise ValueError("Los impactos solo pueden ser '+' o '-'.")

    # 4. Cálculo de distancias euclidianas
    s_pos = np.sqrt(np.sum((v - ideal_pos) ** 2, axis=1))
    s_neg = np.sqrt(np.sum((v - ideal_neg) ** 2, axis=1))

    # 5. Score TOPSIS
    score = s_neg / (s_pos + s_neg + 1e-12)

    # 6. Obtener las posiciones ordenadas de mayor a menor y emparejar con su score
    top_indices = np.argsort(score)[::-1][:top_n]

    del x
    del w
    del norma
    del r
    gc.collect()

    return [(int(idx), float(score[idx])) for idx in top_indices]


def best_pcs(pcs: list[FullPcBuild], weights: list[int]) -> list[tuple[int, float]]:
    matriz = np.array(
        [[getattr(pc, col) for col in CRITERIOS] for pc in pcs],
        dtype=float,
    )
    return topsis(matriz, weights, impact, 5)


def solve_optimization(pcs, categories) -> list[PcBuild]:
    weights = categories.to_weights_list()
    full_build_list = []
    final_results = []
    for pc in pcs:
        new_pc = pc.to_full_pc_build(categories.price)
        if new_pc is None:
            continue
        full_build_list.append(new_pc)
    if len(full_build_list) > 0:
        results = best_pcs(full_build_list, weights)
        for index, score in results:
            final_results.append(pcs[index].to_pc_build(score))
    return final_results
