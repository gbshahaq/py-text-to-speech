<#About this script:
    1. Powershell - because I'm on Windows and it's comfortable
    2. AWS is simpler setup - just calling AWS CLI. IAM user specifically for Polly permissions
       set in local .aws credentials file and referenced as a profile.
    3. Azure was a pain - and this script requires local admin to run. Some prerequsites for install
       required too: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/spx-basics?tabs=windowsinstall%2Cterminal
    4. Some differences in parameters required
         - both allow output to 8khz mp3 suitable for IVR use
         - engine and text-type required by AWS - not by MS
         - voice id on AWS is just the name - MS is locale+name+engine
    

#>

#constants
$xlFile = "C:\Users\Me\Prompts-TTS.xlsx"
$sheetName = "Sheet1"
$path = "C:\Temp\TTS\"

#source of data - Excel workbook
$objExcel = New-Object -ComObject Excel.Application
$workBook = $objExcel.Workbooks.Open($xlFile)
$sheet = $workBook.Worksheets.Item($sheetName)
$objExcel.Visible=$false

$rowMax = ($sheet.UsedRange.Rows).count

#set starting coordinates for data fetch
$rowPrompt, $colPrompt = 1,1
$rowLang, $colLang = 1,3
$rowProvider, $colProvider = 1,4
$rowVoice, $colVoice = 1,5
$rowEngine, $colEngine = 1,6
$rowText, $colText = 1,7
$rowSSML, $colSSML = 1,8

#loop until the last row of data
for ($i=1; $i -le $rowMax-1; $i++)
{
    $prompt = $sheet.Cells.Item($rowPrompt+$i, $colPrompt).text        #promptId (internal)
    $provider = $sheet.Cells.Item($rowProvider+$i, $colProvider).text  #Amazon or Microsoft
    $lang = $sheet.Cells.Item($rowLang+$i, $colLang).text              #locale
    $voice = $sheet.Cells.Item($rowVoice+$i, $colVoice).text           #voice name from provider
    $engine = $sheet.Cells.Item($rowEngine+$i, $colEngine).text        #Standard or Neural
    $ssml = $sheet.Cells.Item($rowSSML+$i, $colSSML).text.Trim('"')    #text with <speak> tags. MS/AWS implement SSML differently...
    $vtext = $sheet.Cells.Item($rowText+$i, $colText).text             #text of the prompt
    $awsengine = $engine.ToLower() # aws literals are lcase            #AWS specfies lower case
    $msvoice = $lang + "-" + $voice + $engine                          #MS uses the "shortname" and not "displayname"
#    Write-Host $msvoice

    $inArr = @($prompt,$lang, $voice, $engine, $ssml)
#    write-host $inArr

    if($ssml -ne "<speak></speak>")  #skip blank text
    {

        $mp3Name = $inArr[0],$inArr[1],$inArr[2],$inArr[3] -join "_"
        $outPath = $path + $mp3Name + ".mp3"

        if($provider -eq "Amazon") {
            aws polly synthesize-speech --output-format mp3 --sample-rate 8000 --profile PollyService --text-type ssml --engine $awsengine --voice-id $voice --text $ssml $outPath
       }else {                        
            spx synthesize --format riff-8khz-16bit-mono-pcm --voice $msvoice --text $vtext --audio output $outPath        
        }
         Write-Host ($outPath + " from " + $provider + " saved")
    }
}

$objExcel.quit()
