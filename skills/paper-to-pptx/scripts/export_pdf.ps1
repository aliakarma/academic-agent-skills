# Export a .pptx to PDF through Microsoft PowerPoint (true font and equation rendering).
# This PC has no LibreOffice, so PowerPoint COM is the renderer.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File export_pdf.ps1 -Pptx path\Research_Presentation.pptx
param([Parameter(Mandatory = $true)][string]$Pptx)
$pptxFull = (Resolve-Path $Pptx).Path
$pdf = [System.IO.Path]::ChangeExtension($pptxFull, ".pdf")
$app = New-Object -ComObject PowerPoint.Application
try {
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $deck = $app.Presentations.Open($pptxFull, $true, $false, $false)
    $deck.SaveAs($pdf, 32)   # ppSaveAsPDF
    Write-Output ("slides: " + $deck.Slides.Count)
    $deck.Close()
} finally {
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
Write-Output "wrote $pdf"
