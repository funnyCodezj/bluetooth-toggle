CreateObject("Shell.Application").ShellExecute "python", Chr(34) & "bluetooth_toggle.py" & Chr(34), CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName), "runas", 1
