## Information from ENTSO-E on energy transfer from/to Ukraine starting from 2024

information taken from these pages on the website: [transparency.entsoe.eu](https://transparency.entsoe.eu/transmission-domain/physicalFlow/show?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_CTY&atch=false&dateTime.dateTime=11.07.2024+00:00%7CCET%7CDAY&border.values=CTY%7C10Y1001C--00003F!CTY_CTY%7C10Y1001C--00003F_CTY_CTY%7C10YPL-AREA-----S&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2))

run the backfill:
```bash
./backfill.sh -s 2024-07-21 -e 2024-08-17
```

assemble outputs:

```bash
python assemble.py
```
