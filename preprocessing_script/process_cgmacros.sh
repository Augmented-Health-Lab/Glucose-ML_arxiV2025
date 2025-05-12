# Input and output folder paths
INPUT_FOLDER="../CGMacros"
OUTPUT_FOLDER1="../11_CGMacros/Libre GL/"
OUTPUT_FOLDER2="../11_CGMacros/Dexcom GL/"

# Run the Python script
python3 cgmacros_main.py "$INPUT_FOLDER" "$OUTPUT_FOLDER1"
python3 cgmacros_main.py "$INPUT_FOLDER" "$OUTPUT_FOLDER2"