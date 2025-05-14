import React, { useEffect, useState } from 'react';
import { FeatureLayer } from '@arcgis/core/layers/FeatureLayer';

const App = () => {
  const [data, setData] = useState([]);
  const [layer, setLayer] = useState(null);

  useEffect(() => {
    const featureLayer = new FeatureLayer({
      url: 'https://feature-layer-url'
    });

    featureLayer.definitionExpression = ''; // Example filter condition
    setLayer(featureLayer);

    const fetchData = async () => {
      const response = await featureLayer.queryFeatures();
      setData(response.features.map(f => f.attributes));
    };

    fetchData();
  }, []);

  const exportToCSV = () => {
    const csvContent = 'data:text/csv;charset=utf-8,' + data.map(e => Object.values(e).join(',')).join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'exported_data.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <h1>Data Filter & Export</h1>
      {layer && <p>Filter Data_KS </p>}
      <button onClick={exportToCSV}>Export Data</button>
    </div>
  );
};

export default App;




//Link for export option esri community
//https://community.esri.com/t5/arcgis-experience-builder-questions/experience-builder-export-option/td-p/1505822
