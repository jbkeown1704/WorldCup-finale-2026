// Mock CSS imports before importing the component
jest.mock('leaflet/dist/leaflet.css', () => ({}), { virtual: true });

import { render, screen } from '@testing-library/react';
import RouteMap from '../src/components/RouteMap';
import { OptimisedRoute, City } from '../src/types';

// Mock leaflet components
jest.mock('react-leaflet', () => ({
  MapContainer: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="map-container">{children}</div>
  ),
  TileLayer: () => <div data-testid="tile-layer"></div>,
  Marker: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="marker">{children}</div>
  ),
  Popup: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="popup">{children}</div>
  ),
  Polyline: () => <div data-testid="polyline"></div>,
}));

// Mock leaflet
jest.mock('leaflet', () => ({
  Icon: jest.fn(),
  DivIcon: jest.fn().mockImplementation(() => ({})),
  icon: jest.fn(),
  latLng: jest.fn(),
  map: jest.fn(),
  IconDefault: jest.fn(),
}));

describe('RouteMap', () => {
  const mockOriginCity: City = {
    id: 'city-new-york',
    name: 'New York',
    country: 'USA',
    latitude: 40.7128,
    longitude: -74.0060,
    stadium: 'MetLife Stadium',
    accommodationPerNight: 300,
  };

  const mockRoute: OptimisedRoute = {
    stops: [
      {
        stopNumber: 1,
        city: {
          id: 'city-boston',
          name: 'Boston',
          country: 'USA',
          latitude: 42.3601,
          longitude: -71.0589,
          stadium: 'Gillette Stadium',
          accommodationPerNight: 220,
        },
        match: {
          id: 'match-1',
          homeTeam: { id: 'team-usa', name: 'USA', code: 'USA', group: 'A' },
          awayTeam: { id: 'team-mexico', name: 'Mexico', code: 'MEX', group: 'A' },
          city: {
            id: 'city-boston',
            name: 'Boston',
            country: 'USA',
            latitude: 42.3601,
            longitude: -71.0589,
            stadium: 'Gillette Stadium',
            accommodationPerNight: 220,
          },
          kickoff: '2026-06-11T17:00:00Z',
          group: 'A',
          matchDay: 1,
          ticketPrice: 120,
        },
        distanceFromPrevious: 0,
      },
      {
        stopNumber: 2,
        city: {
          id: 'city-philadelphia',
          name: 'Philadelphia',
          country: 'USA',
          latitude: 39.9526,
          longitude: -75.1652,
          stadium: 'Lincoln Financial Field',
          accommodationPerNight: 190,
        },
        match: {
          id: 'match-2',
          homeTeam: { id: 'team-brazil', name: 'Brazil', code: 'BRA', group: 'C' },
          awayTeam: { id: 'team-argentina', name: 'Argentina', code: 'ARG', group: 'J' },
          city: {
            id: 'city-philadelphia',
            name: 'Philadelphia',
            country: 'USA',
            latitude: 39.9526,
            longitude: -75.1652,
            stadium: 'Lincoln Financial Field',
            accommodationPerNight: 190,
          },
          kickoff: '2026-06-12T19:00:00Z',
          group: 'C',
          matchDay: 1,
          ticketPrice: 150,
        },
        distanceFromPrevious: 350,
      },
    ],
    totalDistance: 350,
    strategy: 'nearest-neighbour',
    feasible: true,
    warnings: [],
    countriesVisited: ['USA'],
    missingCountries: ['Mexico', 'Canada'],
  };

  it('should render placeholder message when route is null', () => {
    render(<RouteMap route={null} originCity={mockOriginCity} />);
    expect(screen.getByText(/Validate a route to see it displayed on the map/i)).toBeTruthy();
  });

  it('should render a map container when route is provided', () => {
    render(<RouteMap route={mockRoute} originCity={mockOriginCity} />);
    expect(screen.getByTestId('map-container')).toBeTruthy();
  });

  it('should render a marker for each stop in the route', () => {
    render(<RouteMap route={mockRoute} originCity={mockOriginCity} />);
    const markers = screen.getAllByTestId('marker');
    expect(markers.length).toBe(3);
  });

  it('should handle route with empty stops array', () => {
    const emptyRoute: OptimisedRoute = {
      ...mockRoute,
      stops: [],
      totalDistance: 0,
    };
    render(<RouteMap route={emptyRoute} originCity={mockOriginCity} />);
    expect(screen.getByTestId('map-container')).toBeTruthy();
    const markers = screen.getAllByTestId('marker');
    expect(markers.length).toBe(1);
  });
});