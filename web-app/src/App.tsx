import {APIProvider, Map, Marker} from '@vis.gl/react-google-maps';
import './App.css'

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string;

const App = () => {
  const position = {lat: 59.3688, lng: 18.118};

  return (
    <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
      <h1>Visitor Location Map</h1>
      <div style={{ height: "100%", width: "100%" }}>
        <Map center={position} zoom={10}>
          <Marker position={position} />
        </Map>    
      </div>
  </APIProvider>
  );
};

export default App
