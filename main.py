# ------------------------------------------
# Created by: Karina Torres
# Creation date: 4/27/25
# Last updated: 4/27/25
# Purpose: Process wildfire and PADUS data
#   from selected ecoregions in ArcGIS Pro
# ------------------------------------------

# Access arcpy module
import arcpy
import os

try:
    # -------- Set up data --------

    # Set up workspace
    arcpy.env.workspace = arcpy.GetParameterAsText(0)  # Workspace folder
    arcpy.env.overwriteOutput = True

    # Set up input parameters
    wildfire_feature_class = arcpy.GetParameterAsText(1)    # Path to the wildfire feature class
    ecoregion_shapefile = arcpy.GetParameterAsText(2)       # Path to the ecoregion shapefile
    ecoregion_query = arcpy.GetParameterAsText(3)           # SQL query for filtering ecoregions
    padus_feature_class = arcpy.GetParameterAsText(4)       # Path to the PADUS feature class
    output_folder = arcpy.GetParameterAsText(5)             # Output folder for the geodatabase
    geodatabase_name = "wildfire_output.gdb"                # Name of the geodatabase

    # Construct the full path to the output geodatabase
    output_geodatabase = os.path.join(output_folder, geodatabase_name)

    # Ensure the output geodatabase exists
    if not arcpy.Exists(output_geodatabase):
        arcpy.management.CreateFileGDB(output_folder, geodatabase_name)
        arcpy.AddMessage(f"Created geodatabase: {output_geodatabase}")



    # -------- Process parameter data --------

    # Select ecoregions based on user query
    selected_ecoregions_layer = arcpy.management.MakeFeatureLayer(
        ecoregion_shapefile, "selected_ecoregions_layer", ecoregion_query
    )

    # Create a layer for the wildfire dataset
    wildfire_layer = arcpy.management.MakeFeatureLayer(
        wildfire_feature_class, "wildfire_layer"
    )

    # Select wildfire points within the user-selected ecoregions
    wildfire_selected = arcpy.management.SelectLayerByLocation(
        wildfire_layer, "INTERSECT", selected_ecoregions_layer
    )
    wildfire_selected_output = arcpy.management.CopyFeatures(
        wildfire_selected, f"{output_geodatabase}/wildfire_selected"
    )

    # Create buffers around wildfire points
    buffer_distances = [0.1, 0.5, 1]  # Kilometers
    buffer_outputs = []
    for distance in buffer_distances:
        buffer_output = f"{output_geodatabase}/wildfire_buffer_{int(distance * 1000)}m"
        arcpy.analysis.Buffer(
            wildfire_selected_output, buffer_output, f"{distance} Kilometers",
            dissolve_option="NONE"
        )
        buffer_outputs.append(buffer_output)

    # Join PADUS information to wildfire points
    wildfire_with_padus = arcpy.analysis.SpatialJoin(
        wildfire_selected_output,
        padus_feature_class,
        f"{output_geodatabase}/wildfire_with_padus",
        join_type="KEEP_ALL",  # Keep all wildfire points, even if they don't match PADUS
        match_option="INTERSECT"
    )
    arcpy.AddMessage("Performed spatial join for wildfire points with PADUS.")

    # Add a default value for unmatched records in wildfire points
    arcpy.management.AddField(wildfire_with_padus, "Category", "TEXT", field_length=50)
    arcpy.management.CalculateField(
        wildfire_with_padus,
        "Category",
        "'NOT_IN_PADUS' if !Join_Count! == 0 else !Category!",
        "PYTHON3"
    )
    arcpy.AddMessage("Assigned default value 'NOT_IN_PADUS' to unmatched wildfire points.")

    # Perform PADUS analysis for each wildfire buffer
    buffer_with_padus_outputs = []
    for buffer_output in buffer_outputs:
        buffer_with_padus = arcpy.analysis.SpatialJoin(
            buffer_output,
            padus_feature_class,
            f"{output_geodatabase}/{os.path.basename(buffer_output)}_with_padus",
            join_type="KEEP_ALL",  # Keep all buffer features, even if they don't match PADUS
            match_option="INTERSECT"
        )
        arcpy.AddMessage(f"Performed spatial join for buffer: {buffer_output} with PADUS.")
        
        # Add a default value for unmatched records in the buffer
        arcpy.management.AddField(buffer_with_padus, "Category", "TEXT", field_length=50)
        arcpy.management.CalculateField(
            buffer_with_padus,
            "Category",
            "'NOT_IN_PADUS' if !Join_Count! == 0 else !Category!",
            "PYTHON3"
        )
        arcpy.AddMessage(f"Assigned default value 'NOT_IN_PADUS' to unmatched records in buffer: {buffer_output}.")
        
        buffer_with_padus_outputs.append(buffer_with_padus)



    # -------- Export Data --------

    # Export wildfire points with PADUS information to CSV
    wildfire_csv = os.path.join(output_folder, "wildfire_with_padus.csv")
    arcpy.conversion.TableToTable(
        wildfire_with_padus, output_folder, os.path.basename(wildfire_csv)
    )
    arcpy.AddMessage(f"Exported wildfire points with PADUS information to {wildfire_csv}.")

    # Export buffered wildfire data with PADUS information to CSV
    for buffer_with_padus in buffer_with_padus_outputs:
        # Extract the path to the feature class from the arcpy result object
        buffer_with_padus_path = buffer_with_padus.getOutput(0)
        
        # Construct the CSV file path
        buffer_csv = os.path.join(output_folder, f"{os.path.basename(buffer_with_padus_path)}.csv")
        
        # Export the buffer with PADUS information to CSV
        arcpy.conversion.TableToTable(
            buffer_with_padus_path, output_folder, os.path.basename(buffer_csv)
        )
        arcpy.AddMessage(f"Exported buffer data with PADUS information to {buffer_csv}.")



    # -------- Create and add layers to the map --------

    # Add layers to the map
    aprx = arcpy.mp.ArcGISProject("CURRENT")        # Reference the current ArcGIS Pro project
    map_view = aprx.listMaps()[0]                   # Get the first map in the project

    # Add selected ecoregions to the map
    selected_ecoregions_layer_file = os.path.join(output_folder, "selected_ecoregions.lyrx")
    arcpy.management.SaveToLayerFile(selected_ecoregions_layer, selected_ecoregions_layer_file, "RELATIVE")
    map_view.addDataFromPath(selected_ecoregions_layer_file)  
    arcpy.AddMessage("Added selected ecoregions to the map.")

    # Add wildfire points with PADUS information to the map
    map_view.addDataFromPath(wildfire_with_padus)
    arcpy.AddMessage("Added wildfire points with PADUS information to the map.")

    # Add each buffer with PADUS information to the map
    for buffer_with_padus in buffer_with_padus_outputs:
        buffer_with_padus_path = buffer_with_padus.getOutput(0)  
        map_view.addDataFromPath(buffer_with_padus_path)         
        arcpy.AddMessage(f"Added buffer with PADUS information to the map: {buffer_with_padus_path}")



    arcpy.AddMessage("All processing completed successfully.")



# Handle errors
except Exception as e:
    arcpy.AddError(f"Failed to process wildfire data: {e}")
    raise
