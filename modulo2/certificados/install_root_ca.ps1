# Script de instalacion de Root CA para el proyecto COIL Grupo 2
# Permite validar el certificado SSL en Windows y navegadores (Chrome, Edge)
# otorgando los puntos extra (BONUS) al eliminar advertencias de seguridad.

$certPath = Join-Path $PSScriptRoot "COIL_Group2_Root_CA.crt"

if (-not (Test-Path $certPath)) {
    Write-Error "No se encontro el archivo de certificado CA: $certPath"
    exit 1
}

Write-Host "Instalando COIL Group 2 Root CA en el almacen de Autoridades de Certificacion Raiz de Confianza..."
Import-Certificate -FilePath $certPath -CertStoreLocation "Cert:\CurrentUser\Root" | Out-Null
Write-Host "Certificado CA instalado exitosamente en Cert:\CurrentUser\Root."
Write-Host "Cualquier navegador basado en Chromium (Edge/Chrome) reconocera https://www.coil-group2.com y https://10.51.76.174 como conexiones seguras y confiables."
