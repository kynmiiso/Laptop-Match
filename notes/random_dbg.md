ANOMALY
```python
15 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
16 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
35 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
62 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
196 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
220 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
235 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
249 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
272 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
285 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
333 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
347 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
352 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
397 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
446 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
450 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
477 ['display(in inch)', 'id', 'name', 'os', 'processing power', 'processor', 'ram', 'storage']
508 ['display(in inch)', 'id', 'name', 'os', 'processing power', 'processor', 'ram', 'storage']
514 ['display(in inch)', 'id', 'name', 'os', 'processing power', 'processor', 'ram', 'storage']
```

IDS
```
15, 16,  35,  62, 196, 220, 235, 249, 272, 285, 333, 347, 352, 397, 446, 450 ,477,508, 514
```

SAMPLE
```
446,Lenovo V15 G2 Core i3 11th Gen,37500,Intel Core i3 Processor (11th Gen),8 GB DDR4 RAM,64 bit Windows 11 Operating System,1 TB HDD|256 GB SSD,15.6,4.4,53,3
15,HP 14s Intel Core i3 11th Gen,37990,Intel Core i3 Processor (11th Gen),8 GB DDR4 RAM,64 bit Windows 11 Operating System,256 GB SSD,14,4.2,1779,160
```
---
> switched approaches

ANOMALY V2
```python
15 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
16 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
35 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
62 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
196 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
220 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
235 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
249 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
272 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
285 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
333 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
348 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
352 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
369 ['display(in inch)', 'id', 'name', 'os', 'processing power', 'processor', 'ram', 'storage']
397 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
447 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
451 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
478 ['display(in inch)', 'id', 'name', 'os', 'processing power', 'processor', 'ram', 'storage']
509 ['display(in inch)', 'id', 'name', 'os', 'processing power', 'processor', 'ram', 'storage']
515 ['display(in inch)', 'id', 'name', 'os', 'processing power', 'processor', 'ram', 'storage']
```

SAMPLE
```
16 ['display(in inch)', 'id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']
62 ['id', 'name', 'os', 'price(in Rs.)', 'processing power', 'processor', 'ram', 'storage']

16,HP Ryzen 5 Hexa Core 5500U,49123,AMD Ryzen 5 Hexa Core Processor,16 GB DDR4 RAM,64 bit Windows 11 Operating System,512 GB SSD,15.6,4.3,328,34
62,Lenovo IdeaPad 3 Core i5 12th Gen,56049,Intel Core i5 Processor (12th Gen),8 GB DDR4 RAM,64 bit Windows 11 Operating System,512 GB SSD,15.6,4.2,247,21
```

ANOMALY V2 + ID it is matched with (`print(id_, n['id'], [i for i in n2 if i not in no_issue])`)
```python
15 348 ['display(in inch)', 'id', 'name', 'price(in Rs.)']  # *price 348 exists, id 348 also exists. probably*
16 196 ['display(in inch)', 'id', 'name', 'price(in Rs.)']
35 333 ['display(in inch)', 'id', 'name', 'price(in Rs.)']
62 16 ['id', 'name', 'price(in Rs.)']  # *display 16 in duplicate; which may be why display doesn't show here*
196 16 ['id', 'name', 'price(in Rs.)']
220 16 ['id', 'name', 'price(in Rs.)']
235 16 ['id', 'name', 'price(in Rs.)']
249 16 ['id', 'name', 'price(in Rs.)']
272 369 ['display(in inch)', 'id', 'name', 'price(in Rs.)']
285 16 ['id', 'name', 'price(in Rs.)']
333 35 ['id', 'name', 'price(in Rs.)']  # *the fucking size 35 display*
348 15 ['id', 'name', 'price(in Rs.)']
352 515 ['display(in inch)', 'id', 'name', 'price(in Rs.)']
369 272 ['display(in inch)', 'id', 'name']
397 478 ['display(in inch)', 'id', 'name', 'price(in Rs.)']
447 15 ['id', 'name', 'price(in Rs.)']
451 16 ['id', 'name', 'price(in Rs.)']
478 397 ['display(in inch)', 'id', 'name']
509 272 ['display(in inch)', 'id', 'name']
515 352 ['display(in inch)', 'id', 'name']
```
> *notice that the IDs on the right <= 16 ==> no "display"*
