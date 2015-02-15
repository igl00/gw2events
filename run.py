# Compiles the qrc assets before starting the program
import build_utils
import main

build_utils.compile_assets()  # Compile the qrc assets
# build_utils.compile_ui()  # Compile the ui files
main.start_app()  # Start the app