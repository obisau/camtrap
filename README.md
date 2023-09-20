# Modelling BRUVS dataset into Camtrap DP and GBIF Unified Model (UM).

Link to [presentation slide](camtrap_gum_mapping_29032023.pdf)

## BRUVS data selection
- BRUVS observations at Ningloo Marine Park, Western Australia. 

    This dataset is BRUVS data from 5 surveys at the Ningaloo Reef, Western Australia in 2019. It is part of the Marine Biodiversity Hub D3 project (https://www.nespmarine.edu.au/project/project-d3-implementing-monitoring-amps-and-status-marine-biodiversity-assets-continental) and has been downloaded from GlobalArchive (https://globalarchive.org/geodata/data/project/get/254) in January 2021. Video and images from the 5 BRUV trips are available at the CSIRO Data Access Portal. See Keesing, John; Langlois, Tim (2021): August 2019 Ningaloo DMR BRUV field trip - part 1of 3. v2. CSIRO. Data Collection. https://doi.org/10.25919/b9r3-x356 and the links to related dataset records.

## Download data from Global Archive/CSIRO DAP
Data available at:
- [IPT](https://www.marine.csiro.au/ipt/resource.do?r=globalarchive_ningaloo_d3_bruvs) 
- [Global Archive](https://globalarchive.org/geodata/data/project/get/254) 
- [CSIRO DAP](https://data.csiro.au/collection/csiro:48753?q=bruv%201%20of%20&_st=keyword&_str=5&_si=4)

## Create Camtrap DP using frictionless framework

- CamtrapDP example https://github.com/tdwg/camtrap-dp/tree/main/example
- Create Data Package Metadata based on [camtrap-dp-profile](https://raw.githubusercontent.com/tdwg/camtrap-dp/main/camtrap-dp-profile.json)
- Create Data Resources based on 
    - deployments [schema](https://raw.githubusercontent.com/tdwg/camtrap-dp/main/deployments-table-schema.json)
    - media [schema](https://raw.githubusercontent.com/tdwg/camtrap-dp/main/media-table-schema.json)
    - media-observations [schema](https://raw.githubusercontent.com/tdwg/camtrap-dp/main/media-observations-table-schema.json)
    - event-observations [schema](https://raw.githubusercontent.com/tdwg/camtrap-dp/main/event-observations-table-schema.json)
- Wrote a python [script](https://bitbucket.csiro.au/projects/CIDC/repos/idc-python-scripts/browse/camtrap/camtrap_dp.py) to create necessary data resources for Camtrap DP.

### Questions?
- How to add stereo imagery (two video files) in media resource?
- How to add depth field in observation resource?
- 

## Loading Camtrap DP dataset into IPT

- Created new IPT resource with newly created Camtrap DP in https://ipt3.gbif-uat.org/ 
### Issues:
 - After adding Contributors under Metadata section, the content doesn't shows up.


## Modelling Camtrap DP dataset into GBIF Unified Model
- Following guidelines from https://github.com/gbif/model-material/blob/master/data-mapping.md for data mapping.
- Create Postgres docker container
- Created table as defined in [schema.sql](https://raw.githubusercontent.com/gbif/model-material/master/schema.sql). 
- Examples available at https://github.com/gbif/model-tests/tree/master/camtrapdp/files