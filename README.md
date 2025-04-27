# PADUS Wildfire Analysis Tool (PWAT)

> ### Quick start:
> 1. Download wildfire_tool.zip
> 2. Extract folder contents in an ArcGIS Pro project
> 3. Run the tool using the provided sample data or your own data


**Wildfires are important natural disturbances in fire-dependent ecosystems, but they can pose hazards to society and natural resources when occurring as a result of fire suppression or occurring outside of their historic fire regime** (Parks et al., 2025; Doerr & Santín, 2016). One way that **wildfire risk** can be mitigated is by understanding the likelihood of a wildfire occurring, which is often examined using **fire occurrence modelling of wildfire ignition points** (Miller and Ager, 2013). Binomial generalized linear models, for example, can be created to understand how different human accessibility, vegetative, and climatic variables influence the probability of an ignition (Costafreda-Aumedes et al., 2017). There are many publicly available and remotely sensed datasets that can be used to represent these variables in fire occurrence modelling. ***However, accessing and working with these datasets is extremely time-consuming.*** This represents a challenge for managers and scientists that regularly need to create and update predictive wildfire models for relatively large geographic areas. 

The **PADUS Wildfire Analysis Tool (PWAT)** attempts to address this problem by automating the extraction of data from the Protected Areas Database of the United States (PADUS), a publicly available dataset that contains polygon features of locally to federally protected areas in the U.S. (USGS GAP, 2024). The tool will allow users to quickly join information from the PADUS to their wildfire records. Additionally, users will be able to select wildfire records from one or more ecoregions and create buffered points. The exported data will be displayed on the ArcGIS Pro map for visualizations, and it will be exported into a geodatabase. The individual datasets will also be converted to CSV files, which are ready to use for fire occurrence modelling in other applications (e.g., RStudio). 



## Summary for Accessing and Running PWAT:

The PADUS Wildfire Analysis Tool (PWAT) allows users to query ecoregions to narrow their wildfire dataset and create buffered points of their wildfire records with the PADUS feature information (if applicable). Any feature class of wildfire points and any ecoregion shapefile can be used, but this summary refers to the FPA-FOD feature class and the Level 2 Ecoregions of North America shapefile, which are used as the sample and default values provided by PWAT.

### PWAT requires six components in order to run: 

1.	A **workspace folder** that contains the toolbox, scripts folder, and data folder
    - The default provided is the main folder within the zip file.
3.	A feature class of **wildfire records**
    - The sample and default provided is the fire feature class within the Fire Program Analysis Fire Occurrence Database (FPA-FOD) geodatabase (Short, 2022)
4.	A feature class of **ecoregions**
    - The sample and default provided is the US EPA Level 2 Ecoregions of North America (U.S. EPA, 2024)
5.	**SQL Query** to narrow wildfire records to one or more desired ecoregions
    - The default provided is an ecoregion of the Northeastern U.S.
6.	A feature class of **PADUS** from the PADUS geodatabase
    - The sample and default provided is the combined PADUS feature class within the PADUS geodatabase
7.	An **output folder**
    - The default provided is nested within the “Data” folder of the main “wildfire_tool” folder.
    - A layer, four CSV files, and a geodatabase will be saved here.

> [!IMPORTANT]
> To run the PWAT, you must first [download the zip file](PADUS_Wildfire_Analysis_Tool.zip)
 containing the source code and data from my Github page: https://github.com/KTorres23/wildfire_project.

You should open a new project in ArcGIS Pro, unzip this file, place it in your new project folder, and access the PWAT through the Catalog pane.

You must specify the location of the components described above. The default values of the file paths are not relative, but the paths can be inspected to select the correct files within the sample data. Any SQL query can be specified to narrow the wildfire feature class to records within the ecoregion(s) selected with the query.

> For example, to run PWAT on wildfire records in the southeastern U.S., you can enter the following string into the text box: “NA_L2CODE = ‘8.3’ Or NA_L2CODE = ‘8.4’ Or NA_L2CODE = ‘8.5’”. Note that you can use other fields within the ecoregion shapefile, like “NA_L1KEY,” if desired. The tool can use any feature class within the PADUS, but the feature class with all the protected areas is selected as the default value.

The “outputs” folder will produce multiple files that can be used for further manipulation or visualization in ArcGIS Pro or for importing to another application for fire occurrence modelling. A geodatabase will be created with 8 files:

- Original wildfire points data
- Wildfire points data with PADUS information
- Buffered wildfire points data
  - (3 files with buffer diameters of 100m, 500m, and 1000m)
- Buffered wildfire points data with PADUS information
  - (3 files with buffer diameters of 100m, 500m, and 1000m) 

Additionally, the “outputs” folder will have 8 CSV and XML files with the wildfire points and buffered data with PADUS information. There is also a layer file of the ecoregions selected through your query.

> [!NOTE]
> The tool processing time takes around 5 minutes, depending on the system.


## References
* Costafreda-Aumedes, S., Comas, C., & Vega-Garcia, C. (2017). Human-caused fire occurrence modelling in perspective: A review. *International Journal of Wildland Fire*, 26(12), 983–998. https://doi.org/10.1071/WF17026
* Doerr, S. H., & Santín, C. (2016). Global trends in wildfire and its impacts: Perceptions versus realities in a changing world. *Philosophical Transactions of the Royal Society B: Biological Sciences*, 371(1696), 20150345. https://doi.org/10.1098/rstb.2015.0345
* Miller, C., & Ager, A. A. (2013). A review of recent advances in risk analysis for wildfire management. *International Journal of Wildland Fire*, 22(1), 1. https://doi.org/10.1071/WF11114
* Parks, S. A., Guiterman, C. H., Margolis, E. Q., Lonergan, M., Whitman, E., Abatzoglou, J. T., Falk, D. A., Johnston, J. D., Daniels, L. D., Lafon, C. W., Loehman, R. A., Kipfmueller, K. F., Naficy, C. E., Parisien, M.-A., Portier, J., Stambaugh, M. C., Williams, A. P., Wion, A. P., & Yocom, L. L. (2025). A fire deficit persists across diverse North American forests despite recent increases in area burned. *Nature Communications*, 16(1), 1493. https://doi.org/10.1038/s41467-025-56333-8
* U.S. Geological Survey (USGS) Gap Analysis Project (GAP). (2024). Protected Areas Database of the United States (PAD-US) 4: U.S. Geological Survey data release, https://doi.org/10.5066/P96WBCHS. 

