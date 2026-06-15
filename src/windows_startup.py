"""
windows_startup.py

Controla a inicializacao automatica do widget no login do usuario Windows.
"""

import os
import subprocess
import sys

try:
    import winreg
except ImportError:  # pragma: no cover - permite importar fora do Windows
    winreg = None


NOME_ENTRADA = "TokenWidget"
CHAVE_RUN = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _comando_inicializacao():
    """Monta o comando adequado para o executavel empacotado ou modo dev."""
    partes = [os.path.abspath(sys.executable)]
    if not getattr(sys, "frozen", False):
        partes.append(os.path.join(os.path.dirname(__file__), "main.py"))
    return subprocess.list2cmdline(partes)


def esta_ativada():
    """Retorna True quando existe uma entrada de inicializacao para o widget."""
    if winreg is None:
        return False
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, CHAVE_RUN, 0, winreg.KEY_READ
        ) as chave:
            winreg.QueryValueEx(chave, NOME_ENTRADA)
        return True
    except FileNotFoundError:
        return False
    except OSError:
        return False


def ativar():
    """Adiciona o widget na inicializacao do usuario atual."""
    if winreg is None:
        raise OSError("recurso disponivel apenas no Windows")
    with winreg.CreateKeyEx(
        winreg.HKEY_CURRENT_USER, CHAVE_RUN, 0, winreg.KEY_SET_VALUE
    ) as chave:
        winreg.SetValueEx(
            chave, NOME_ENTRADA, 0, winreg.REG_SZ, _comando_inicializacao()
        )


def desativar():
    """Remove o widget da inicializacao do usuario atual."""
    if winreg is None:
        raise OSError("recurso disponivel apenas no Windows")
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, CHAVE_RUN, 0, winreg.KEY_SET_VALUE
        ) as chave:
            winreg.DeleteValue(chave, NOME_ENTRADA)
    except FileNotFoundError:
        pass
