// Load the GPWv4.11 Population Count ImageCollection
var gpwCollection = ee.ImageCollection('CIESIN/GPWv411/GPW_Population_Count');

// Load the neighborhoods FeatureCollection for Bonaire
var neighborhoods = ee.FeatureCollection('projects/ee-desmond/assets/zonalstatsbonaire');

// Filter the population dataset for the year 2020 and select the relevant band
var year2020Image = gpwCollection.filter(ee.Filter.calendarRange(2020, 2020, 'year')).first();
var population2020 = year2020Image.select('population_count');

// Function to calculate zonal statistics for each neighborhood
function calculateZonalStatistics(feature) {
  var stats = population2020.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: feature.geometry(),
    scale: 927.67, // Resolution of the population data
    maxPixels: 1e9
  });
  return feature.set('population_2020', stats.get('population_count'));
}

// Apply the zonal statistics function to all neighborhoods
var updatedNeighborhoods = neighborhoods.map(calculateZonalStatistics);

// Export the updated FeatureCollection with population data for the year 2020
Export.table.toDrive({
  collection: updatedNeighborhoods,
  description: 'NeighborhoodPopulation2020',
  fileFormat: 'CSV',
  folder: 'GEE'
});
