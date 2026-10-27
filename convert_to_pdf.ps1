param([string]$inputFile, [string]$outputFile)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open((Resolve-Path $inputFile).Path)
    $outPath = [System.IO.Path]::GetFullPath($outputFile)
    $doc.SaveAs([ref]$outPath, [ref]17)
    $doc.Close()
    Write-Host "Converted successfully to $outPath"
} finally {
    $word.Quit()
}
