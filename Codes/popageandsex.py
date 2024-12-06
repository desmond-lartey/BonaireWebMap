// Load WorldPop population data and filter for the year 2020 within the Area of Interest (AOI)
var dataset = ee.ImageCollection('WorldPop/GP/100m/pop_age_sex')
                .filterDate('2020-01-01', '2021-01-01')
                .filterBounds(aoi);

// Select relevant bands for population, age, and sex distribution
var selectedBands = dataset.select([
  'population',
  'M_0', 'M_1', 'M_5', 'M_10', 'M_15', 'M_20', 'M_25', 'M_30', 'M_35', 'M_40',
  'M_45', 'M_50', 'M_55', 'M_60', 'M_65', 'M_70', 'M_75', 'M_80',
  'F_0', 'F_1', 'F_5', 'F_10', 'F_15', 'F_20', 'F_25', 'F_30', 'F_35', 'F_40',
  'F_45', 'F_50', 'F_55', 'F_60', 'F_65', 'F_70', 'F_75', 'F_80'
]);

// Aggregate the dataset to a single image by averaging the selected bands
var imageForExport = selectedBands.mean();

// Define visualization parameters for population data
var visualization = {
  bands: ['population'],
  min: 0.0,
  max: 50.0,
  palette: ['24126c', '1fff4f', 'd4ff50']
};

// Set map view centered on Bonaire with an appropriate zoom level
Map.setCenter(-68.2655, 12.2019, 11);
Map.addLayer(imageForExport, visualization, 'Population');

// Export the processed population and demographic data as GeoTIFF
Export.image.toDrive({
  image: imageForExport.clip(aoi),
  description: 'BonairePopulationAgeSex2020',
  scale: 100,
  region: aoi,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e9
});

// Load hexagon grid for zonal statistics
var hexagons = ee.FeatureCollection('projects/ee-desmond/assets/zonalstats');

// Function to calculate and append zonal statistics for a specific band
function calculateZonalStatistics(bandName) {
  var singleBandImage = imageForExport.select([bandName]);
  var statistics = singleBandImage.reduceRegions({
    collection: hexagons,
    reducer: ee.Reducer.mean(),
    scale: 100
  });
  return statistics.map(function(feature) {
    return feature.set('band', bandName);
  });
}

// Perform zonal statistics for all selected bands
var bandNamesList = selectedBands.bandNames();
var bandStatisticsList = bandNamesList.map(calculateZonalStatistics);
var flattenedStatistics = ee.FeatureCollection(bandStatisticsList).flatten();

// Export the zonal statistics as GeoJSON and CSV
Export.table.toDrive({
  collection: flattenedStatistics,
  description: 'HexagonDemographicStatistics',
  fileFormat: 'GeoJSON'
});

Export.table.toDrive({
  collection: flattenedStatistics,
  description: 'HexagonDemographicStatistics_CSV',
  fileFormat: 'CSV'
});
