#Get the absolute path of the script's directory
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

#Define full paths and run the conversion for each window
$inputUI = Join-Path $baseDir "mainwindow.ui"
$outputPY = Join-Path $baseDir "mainwindow.py"
& pyside6-uic $inputUI -o $outputPY

#Indicate if successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: Converted $inputUI to $outputPY"
} else {
    Write-Host "Error: Failed to convert $inputUI to $outputPY"    
}