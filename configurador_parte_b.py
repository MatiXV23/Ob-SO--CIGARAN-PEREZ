#!/usr/bin/env python3
#
# configurador_parte_b.py
# Script en Python orientado a objetos para completar las configuraciones manuales
# dejadas por el script de la Parte A.
#
# Ejecutar como root: sudo python3 configurador_parte_b.py
#

import os
import subprocess
import sys
from abc import ABC, abstractmethod

# --- Clases para definir las Políticas de Configuración ---

class Policy(ABC):
    """Clase base abstracta para todas las políticas de configuración."""
    
    @abstractmethod
    def get_description(self) -> str:
        """Devuelve una descripción legible de lo que hace la política."""
        pass
        
    @abstractmethod
    def apply(self):
        """Aplica la lógica de la política en el sistema."""
        pass

class SudoPolicy(Policy):
    """
    Política para denegar la ejecución de comandos de instalación de software
    a una lista de usuarios.
    """
    def __init__(self, restricted_users: list):
        self.restricted_users = restricted_users
        self.sudoers_file = "/etc/sudoers.d/99-restringir-instalacion"
        self.commands_to_block = ["/usr/bin/apt", "/usr/bin/apt-get", "/usr/bin/dpkg"]

    def get_description(self) -> str:
        return f"Restringir comandos de instalación para: {', '.join(self.restricted_users)}"

    def apply(self):
        print(f"  -> Creando archivo de reglas en {self.sudoers_file}...")
        
        # Generar contenido del archivo de sudoers
        header = "# Regla generada por el configurador para denegar instalación de software\n"
        alias = f"Cmnd_Alias INSTALL = {', '.join(self.commands_to_block)}\n"
        rules = "\n".join([f"{user}  ALL=(ALL) !INSTALL" for user in self.restricted_users])
        
        content = header + alias + rules + "\n"
        
        try:
            with open(self.sudoers_file, "w") as f:
                f.write(content)
            
            # **Paso de seguridad CRÍTICO**: Validar la sintaxis antes de continuar.
            subprocess.run(["visudo", "-c", "-f", self.sudoers_file], check=True, capture_output=True)
            print("  -> ¡Éxito! La sintaxis del archivo sudoers es correcta.")
        except (IOError, subprocess.CalledProcessError) as e:
            print(f"  -> ERROR FATAL: No se pudo crear o validar el archivo de sudoers. Mensaje: {e}", file=sys.stderr)
            # Limpiar si la validación falla para no romper el sistema
            if os.path.exists(self.sudoers_file):
                os.remove(self.sudoers_file)
            sys.exit(1)


class BrowserPolicy(Policy):
    """
    Política para restringir el uso del navegador a un usuario específico
    mediante un grupo de permisos.
    """
    def __init__(self, restricted_user: str, permitted_users: list, browser_path="/usr/bin/firefox"):
        self.restricted_user = restricted_user
        self.permitted_users = permitted_users
        self.browser_path = browser_path
        self.group_name = "web-access"

    def get_description(self) -> str:
        return f"Restringir uso del navegador a '{self.restricted_user}'"

    def apply(self):
        if not os.path.exists(self.browser_path):
            print(f"  -> ADVERTENCIA: Navegador no encontrado en '{self.browser_path}'. Omitiendo política.", file=sys.stderr)
            return

        try:
            print(f"  -> Creando grupo '{self.group_name}' (si no existe)...")
            subprocess.run(["groupadd", self.group_name], stderr=subprocess.DEVNULL)

            print(f"  -> Asignando propiedad del navegador al grupo '{self.group_name}'...")
            subprocess.run(["chgrp", self.group_name, self.browser_path], check=True)

            print("  -> Estableciendo permisos de ejecución (750) en el navegador...")
            os.chmod(self.browser_path, 0o750) # rwxr-x---

            print(f"  -> Añadiendo usuarios permitidos al grupo '{self.group_name}'...")
            for user in self.permitted_users:
                subprocess.run(["usermod", "-aG", self.group_name, user], check=True)
            
            print(f"  -> ¡Éxito! El usuario '{self.restricted_user}' fue excluido del acceso.")
        except (subprocess.CalledProcessError) as e:
            print(f"  -> ERROR: Falló un comando del sistema. Mensaje: {e}", file=sys.stderr)
            sys.exit(1)


# --- Clase Orquestadora ---

class ConfigManager:
    """Gestiona y aplica una lista de políticas de configuración."""
    def __init__(self, policies_to_apply: list[Policy]):
        self.policies = policies_to_apply

    def run(self):
        self._ensure_root()
        print("=====================================================")
        print("  Ejecutando Configurador de Sistema - Parte B")
        print("=====================================================")
        
        for i, policy in enumerate(self.policies):
            print(f"\n[Política {i+1}/{len(self.policies)}]: {policy.get_description()}")
            policy.apply()
            
        print("\n=====================================================")
        print("  Todas las políticas se aplicaron correctamente.")
        print("=====================================================")

    def _ensure_root(self):
        """Verifica que el script se esté ejecutando como usuario root."""
        if os.geteuid() != 0:
            print("Error: Este script debe ejecutarse con privilegios de superusuario.", file=sys.stderr)
            print("Por favor, ejecútalo así: sudo python3 configurador_parte_b.py", file=sys.stderr)
            sys.exit(1)

# --- Punto de Entrada Principal ---

if __name__ == "__main__":
    # Define aquí las políticas que quieres aplicar
    all_policies = [
        SudoPolicy(restricted_users=['contaduria', 'rrpp']),
        BrowserPolicy(
            restricted_user='recepcion',
            permitted_users=['admin', 'soporte', 'contaduria', 'rrpp']
        )
    ]
    
    # Crea el gestor y ejecuta la configuración
    manager = ConfigManager(policies_to_apply=all_policies)
    manager.run()