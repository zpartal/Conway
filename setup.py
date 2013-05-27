from cx_Freeze import setup, Executable
 
exe = Executable(
    script="conway.pyw",
    base="Win32GUI",
    )
 
setup(
    name = "Conway",
    version = "0.1",
    description = "Conway Game of Life",
    executables = [exe]
    )