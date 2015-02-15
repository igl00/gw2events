# Compiles the qrc assets before starting the program
import build_utils
import main

build_utils.compile_assets()  # Compile the qrc assets
print("Starting GW2 Events...")
main.start_app()  # Start the app