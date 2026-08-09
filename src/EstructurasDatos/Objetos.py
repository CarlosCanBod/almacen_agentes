from typing import Any


class Palet:
    def __init__(self, x_inicial: int, y_inicial: int, ang_inicial: bool, x_objetivo: int, y_objetivo: int,
                 ang_objetivo: bool) -> None:
        self.pos_x: int = x_inicial
        self.pos_y: int = y_inicial
        # Las estanterias el valor ang actual 1 es vertical y 0 horizontal
        self.ang_actual: bool = ang_inicial

        self.x_objetivo: int = x_objetivo
        self.y_objetivo: int = y_objetivo
        self.ang_objetivo: bool = ang_objetivo

    def __hash__(self) -> int:

        return hash((self.pos_x, self.pos_y, self.ang_actual, self.x_objetivo, self.y_objetivo, self.ang_objetivo))

    def __str__(self) -> str:
        return f"Lugar(x={self.pos_x}, y={self.pos_y}, ori='{self.ang_actual}')"

    def necesita_moverse(self) -> bool:

        if self.ang_actual != self.ang_objetivo:
            return True
        elif self.pos_x != self.x_objetivo:
            return True
        elif self.pos_y != self.y_objetivo:
            return True

        return False


class Estado:
    def __init__(self, r_x: int, r_y: int, r_ang: str, r_levantado: bool, lista_palets: "list[Palet]") -> None:
        self.Robot_x: int = r_x
        self.Robot_y: int = r_y
        self.Robot_orientacion: str = r_ang
        self.Robot_activado: bool = r_levantado
        self.Lista_estanterias: "list[Palet]" = lista_palets

        self.estado_padre: Any = None
        self.costo_g: int = 0
        self.accion: str = "Inicio"

    def asignar_padre(self, padre: "Estado", coste_accion: int, nombre_accion: str) -> None:

        self.estado_padre = padre
        self.costo_g = coste_accion
        self.accion = nombre_accion

    def volver_inicio(self) -> str:

        if self.estado_padre is None:
            return self.accion
        else:
            return self.estado_padre.volver_inicio() + "." + self.accion

    def __eq__(self, otro_estado: object):
        return hash(self) == hash(otro_estado)

    def __hash__(self) -> int:

        hash_palets = 0
        if self.Lista_estanterias is not None:
            for palet in self.Lista_estanterias:
                hash_palets = hash(palet) + hash_palets

        return hash((self.Robot_x, self.Robot_y, self.Robot_orientacion, self.Robot_activado, hash_palets))
