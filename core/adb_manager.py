import asyncio
import os
from tkinter import messagebox


class ADBManager:
    """Gerencia as interações com o ADB usando asyncio."""

    def __init__(self, logger):
        self.logger = logger
        self.adb_path = os.path.join(os.path.dirname(__file__), "..", "tools", "adb.exe")
        self.adb_path = os.path.abspath(self.adb_path)

    async def _run_cmd(self, cmd):
        """Executa comando ADB de forma assíncrona e retorna stdout/stderr"""
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode(errors="ignore"), stderr.decode(errors="ignore")

    async def verificar_adb(self):
        stdout, _ = await self._run_cmd([self.adb_path, "version"])
        self.logger.log(stdout)
        if "Android Debug Bridge" in stdout:
            self.logger.log("ADB encontrado!\n")
            return True
        else:
            messagebox.showerror("Erro", "ADB não encontrado na pasta tools.")
            return False

    async def conectar_dispositivo(self):
        stdout, _ = await self._run_cmd([self.adb_path, "devices"])
        self.logger.log(stdout)
        linhas = stdout.strip().split("\n")

        if len(linhas) <= 1:
            messagebox.showerror("Erro", "Nenhum dispositivo encontrado.\nAtive a Depuração USB e conecte via cabo.")
            return False

        dispositivos = [linha.split("\t")[0] for linha in linhas[1:] if "device" in linha]
        if dispositivos:
            self.logger.log(f"Dispositivo conectado: {dispositivos[0]}\n")
            return True
        else:
            messagebox.showerror("Erro", "Nenhum dispositivo pronto para comunicação.")
            return False

    async def listar_pacotes(self, filtro=""):
        stdout, stderr = await self._run_cmd([self.adb_path, "shell", "pm", "list", "packages", "--user", "0"])
        if stderr:
            self.logger.log(stderr)

        self.logger.log("Saída do comando 'pm list packages':")
        self.logger.log(stdout)

        packages = []
        for line in stdout.splitlines():
            if line.startswith("package:"):
                pkg = line.replace("package:", "").strip()
                packages.append(pkg)

        if filtro:
            filtro = filtro.lower()
            packages = [p for p in packages if filtro in p.lower()]

        return packages

    async def desinstalar(self, pacotes):
        for pkg in pacotes:
            cmd = [self.adb_path, "shell", "pm", "uninstall", "-k", "--user", "0", pkg]
            self.logger.log(f"\nExecutando: {' '.join(cmd)}")
            stdout, stderr = await self._run_cmd(cmd)
            self.logger.log(stdout or stderr)
