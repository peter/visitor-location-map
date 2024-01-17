import { useState, useEffect } from 'react';
import {APIProvider, Map, Marker} from '@vis.gl/react-google-maps';
import './App.css'

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

type Location = {
  lat: number;
  lng: number;
}

function average(values: number[]): number | undefined {
  if (!values || values.length === 0) return undefined;
  return values.reduce((a, b) => a + b) / values.length;
}

async function fetchLocations(): Promise<Location[]> {
  const result = await fetch(`${API_BASE_URL}/visitor-locations`);
  const data = await result.json()
  return data.locations;
}

function getCenterLocation(locations: Location[]): Location | undefined {
  if (!locations || locations.length === 0) return undefined;
  return {
    lat: average(locations.map((location) => location.lat)) as number,
    lng: average(locations.map((location) => location.lng)) as number,
  }
}


const App = () => {
  const [locations, setLocations] = useState<Location[] | []>([]);

  useEffect(() => {
    async function initializeLocations() {
      const initialLocations = await fetchLocations();
      setLocations(initialLocations);  
    }
    initializeLocations();
  }, []);


  const centerLocation = getCenterLocation(locations);

  return (
    <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
      <h1>Visitor Location Map</h1>
      <div style={{ height: "100%", width: "100%" }}>
        <Map center={centerLocation} zoom={2}>
          {locations.map(location => <Marker position={location} />)}
        </Map>    
      </div>
  </APIProvider>
  );
};

export default App
