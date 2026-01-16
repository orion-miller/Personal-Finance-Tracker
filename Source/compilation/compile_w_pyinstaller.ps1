#Get the absolute path of the script's directory
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

#Define paths for spec file and output folders
$mainScript = Join-Path $baseDir "pyinstaller_config.spec"
$buildDir = Join-Path $baseDir "../../builds/Finance Tracker 1.0"
$tempDir = Join-Path $baseDir "../../builds/temp"

#Clean up build directory if not empty
if (Test-Path $buildDir) {
    Remove-Item -Path $buildDir -Recurse -Force
    Write-Host "Cleaned out previous data in $buildDir"
}
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
    Write-Host "Cleaned out previous data in $tempDir"
}

#Build the pyinstaller cmd
$pyinstallerArgs = @(
    "--clean", #Clean cache
    "--distpath", $buildDir #Output directory
    "--workpath", $tempDir  #Temp directory
    $mainScript
)

#Run PyInstaller
& pyinstaller $pyinstallerArgs

#Indicate if successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: Converted $inputUI to $outputPY"
} else {
    Write-Host "Error: Failed to convert $inputUI to $outputPY"    
}