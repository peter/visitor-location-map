/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect } from 'react';
import {APIProvider, Map, Marker} from '@vis.gl/react-google-maps';
import './App.css'
import _ from 'lodash';

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

type Location = {
  lat: number;
  lng: number;
  country: string;
  created_at: string;
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
  const [country, setCountry] = useState('');
  const [locations, setLocations] = useState<Location[] | []>([]);

  useEffect(() => {
    async function initializeLocations() {
      const initialLocations = await fetchLocations();
      setLocations(initialLocations);  
    }
    initializeLocations();
  }, []);

  const countries: string[] = _.uniq((locations || []).map(location => location.country));
  const countryOptions = [
    { value: '', label: 'All Countries' },
    ...countries.map(country => ({ value: country, label: country }))
  ];
  const handleCountryChange = (event: any) => {
    setCountry(event.target.value);
  }

  const filteredLocations = country ? locations.filter(location => location.country === country) : locations;
  const centerLocation = getCenterLocation(filteredLocations);

  return (
    <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
      <h1>Visitor Location Map</h1>

      <div className="country-select">
        {countryOptions.length > 2 && <select value={country} onChange={handleCountryChange}>
         {countryOptions.map((option) => (
           <option value={option.value}>{option.label}</option>
         ))}
        </select>}
      </div>

      <div style={{ height: "100%", width: "100%" }}>
        <Map center={centerLocation} zoom={2}>
          {filteredLocations.map(location => <Marker position={location} />)}
        </Map>    
      </div>
  </APIProvider>
  );
};

export default App
