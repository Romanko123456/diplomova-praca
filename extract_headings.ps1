
[xml]$docx = Get-Content "c:\Users\Legion\Desktop\skola\DPText\temp_docx\word\document.xml"
$nm = new-object System.Xml.XmlNamespaceManager($docx.NameTable)
$nm.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

$paragraphs = $docx.SelectNodes("//w:p", $nm)
foreach ($p in $paragraphs) {
    $style = $p.SelectSingleNode("w:pPr/w:pStyle", $nm)
    if ($style) {
        $val = $style.Attributes["w:val"].Value
        if ($val -match "Heading" -or $val -match "Nadpis" -or $val -match "Title" -or $val -match "Titul") {
            $text = ""
            $runs = $p.SelectNodes("w:r/w:t", $nm)
            foreach ($r in $runs) { $text += $r.InnerText }
            if ($text.Trim().Length -gt 0) {
                Write-Output "$val : $text"
            }
        }
    }
}
