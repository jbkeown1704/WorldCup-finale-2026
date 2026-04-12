/**
 * RouteMap — YOUR TASK (Frontend)
 *
 * Display the optimised travel route on an interactive map.
 */

import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { LatLngExpression, DivIcon } from 'leaflet';
import { OptimisedRoute, City, ItineraryStop } from '../types';

// Centre of North America
const MAP_CENTRE: LatLngExpression = [39, -98];

// Creates a multi-numbered marker icon (e.g., "2, 4" for stops within same City)
function createMultiNumberedIcon(numbers: number[]): DivIcon {
  const label = numbers.join(', ');
  const width = Math.max(28, 12 + label.length * 8);
  return new DivIcon({
    className: 'numbered-marker',
    html: `<div class="marker-number marker-multi">${label}</div>`,
    iconSize: [width, 28],
    iconAnchor: [width / 2, 14],
  });
}

// Creates a "Start" marker icon
function createStartIcon(): DivIcon {
  return new DivIcon({
    className: 'numbered-marker',
    html: `<div class="marker-start">Start</div>`,
    iconSize: [40, 28],
    iconAnchor: [20, 14],
  });
}

// Group stops by city
function groupStopsByCity(stops: ItineraryStop[]): Map<string, ItineraryStop[]> {
  const grouped = new Map<string, ItineraryStop[]>();
  stops.forEach((stop) => {
    const cityId = stop.city.id;
    if (!grouped.has(cityId)) {
      grouped.set(cityId, []);
    }
    grouped.get(cityId)!.push(stop);
  });
  return grouped;
}

interface RouteMapProps {
  route: OptimisedRoute | null;
  originCity: City | null;
}

function RouteMap({ route, originCity }: RouteMapProps) {
  if (!route) {
    return (
      <div className="route-map-placeholder">
        <h3>Route Map</h3>
        <p>Validate a route to see it displayed on the map.</p>
      </div>
    );
  }

  // Build positions array including origin city
  const positions: LatLngExpression[] = [];

  if (originCity) {
    positions.push([originCity.latitude, originCity.longitude]);
  }

  route.stops.forEach((stop) => {
    positions.push([stop.city.latitude, stop.city.longitude]);
  });

  return (
    <MapContainer
      center={MAP_CENTRE}
      zoom={3}
      style={{ height: '400px', width: '100%', borderRadius: '8px' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Start marker for origin city */}
      {originCity && (
        <Marker
          position={[originCity.latitude, originCity.longitude]}
          icon={createStartIcon()}
        >
          <Popup>
            <strong>Start: {originCity.name}</strong>
            <br />
            <span style={{ fontSize: '0.85em', color: '#666' }}>{originCity.country}</span>
          </Popup>
        </Marker>
      )}

      {Array.from(groupStopsByCity(route.stops).entries()).map(([cityId, stops]) => {
        const firstStop = stops[0];
        const stopNumbers = stops.map((s) => s.stopNumber);

        return (
          <Marker
            key={cityId}
            position={[firstStop.city.latitude, firstStop.city.longitude]}
            icon={createMultiNumberedIcon(stopNumbers)}
          >
            <Popup>
              <strong>{firstStop.city.name}</strong>
              <br />
              <span style={{ fontSize: '0.85em', color: '#666' }}>{firstStop.city.country}</span>
              <hr style={{ margin: '0.5rem 0', border: 'none', borderTop: '1px solid #ddd' }} />
              
              {/* Render match details for each stop in this city */}
              {stops.map((stop) => (
                <div key={stop.stopNumber} className="popup-match" style={{ marginBottom: '0.75rem' }}>
                  <div className="popup-match-number" style={{ fontWeight: 'bold', color: '#e94560' }}>
                    Stop {stop.stopNumber}
                  </div>
                  <div style={{ margin: '0.25rem 0' }}>
                    {stop.match?.homeTeam?.name || 'TBD'} vs {stop.match?.awayTeam?.name || 'TBD'}
                  </div>
                  <div className="popup-match-date" style={{ fontSize: '0.8em', color: '#666' }}>
                    {stop.match?.kickoff ? new Date(stop.match.kickoff).toLocaleDateString('en-US', {
                      weekday: 'short',
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    }) : 'Date TBD'}
                  </div>
                  {stop.distanceFromPrevious > 0 && (
                    <div style={{ fontSize: '0.7em', color: '#999', marginTop: '0.25rem' }}>
                      ✈️ {Math.round(stop.distanceFromPrevious)} km from previous stop
                    </div>
                  )}
                </div>
              ))}
            </Popup>
          </Marker>
        );
      })}
      <Polyline positions={positions} color="#e94560" weight={3} />
    </MapContainer>
  );
}

export default RouteMap;