# Instructions

{{< tabs "uniqueid" >}}
{{< tab "Linux" >}} 

## Bash

```bash
OSSEMVERSION=$(curl "{{< ref "/" >}}OSSEM-CDM.version"); \
wget "{{< ref "/" >}}OSSEM-CDM${OSSEMVERSION}.json"
``` 
{{< /tab >}}
{{< tab "Windows" >}}

## Powershell

```powershell
$OSSEMVERSION=$((Invoke-WebRequest "{{< ref "/" >}}OSSEM-CDM.version").Content); Invoke-WebRequest -OutFile "OSSEM-CDM${OSSEMVERSION}.json" "{{< ref "/" >}}OSSEM-CDM${OSSEMVERSION}.json"
```
{{< /tab >}}
{{< /tabs >}}







