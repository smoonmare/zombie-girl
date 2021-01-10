import cx_Freeze


executables = [cx_Freeze.Executable('run.py')]

cx_Freeze.setup(
    name='Zombie VS World',
    options={'build_exe': {'packages':['pygame'], 'include_files':['png/']}},
    executables = executables
)