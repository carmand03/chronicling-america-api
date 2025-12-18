import pandas as pd
import json
import numpy as np

csv_path = "city_statistics_with_coords.csv"
df = pd.read_csv(csv_path)

df["count_num"] = (
    df["count"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)

max_count = int(df["count_num"].max())

records = []
for _, r in df.iterrows():
    records.append({
        "city": str(r["city"]),
        "state": str(r["state"]),
        "count": int(r["count_num"]),
        "lat": float(r["latitude"]),
        "lng": float(r["longitude"]),
    })

# Legend breakpoints (percentiles): 25%, 50%, 75%, 100%
qs = [0.25, 0.50, 0.75, 1.00]
legend_counts = sorted(set(int(np.quantile(df["count_num"], q)) for q in qs))
if len(legend_counts) < 3:
    legend_counts = sorted(set([int(df["count_num"].min())] + legend_counts + [max_count]))

html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>US City Counts (Leaflet)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    html, body { height: 100%; margin: 0; }
    #map { height: 100%; width: 100%; }

    .legend {
      background: rgba(255,255,255,0.95);
      padding: 10px 12px;
      border-radius: 10px;
      box-shadow: 0 1px 6px rgba(0,0,0,0.25);
      font: 13px/1.35 system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color: #111;
    }
    .legend h4 {
      margin: 0 0 8px 0;
      font-size: 14px;
      font-weight: 700;
    }
    .legend .item {
      display: flex;
      align-items: center;
      gap: 10px;
      margin: 6px 0;
      white-space: nowrap;
    }
    .legend .note {
      margin-top: 6px;
      opacity: 0.75;
      font-size: 12px;
    }
  </style>
</head>
<body>
<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const data = [{"city": "Washington", "state": "District of Columbia", "count": 1427, "lat": 38.8950368, "lng": -77.0365427}, {"city": "New York", "state": "New York", "count": 789, "lat": 40.7127281, "lng": -74.0060152}, {"city": "Honolulu", "state": "Hawaii", "count": 601, "lat": 21.304547, "lng": -157.855676}, {"city": "Chicago", "state": "Illinois", "count": 286, "lat": 41.8755616, "lng": -87.6244212}, {"city": "Springfield", "state": "Illinois", "count": 284, "lat": 39.7990175, "lng": -89.6439575}, {"city": "Richmond", "state": "Virginia", "count": 281, "lat": 37.5385087, "lng": -77.43428}, {"city": "Columbia", "state": "nan", "count": 234, "lat": 4.099917, "lng": -72.9088133}, {"city": "San Francisco", "state": "California", "count": 201, "lat": 37.7879363, "lng": -122.4075201}, {"city": "Augusta", "state": "Bayern", "count": 198, "lat": 48.3690341, "lng": 10.8979522}, {"city": "Omaha", "state": "Nebraska", "count": 184, "lat": 41.2587459, "lng": -95.9383758}, {"city": "New Haven", "state": "Connecticut", "count": 182, "lat": 41.3082138, "lng": -72.9250518}, {"city": "Milwaukee", "state": "Wisconsin", "count": 148, "lat": 43.0386475, "lng": -87.9090751}, {"city": "Salt Lake City", "state": "Utah", "count": 144, "lat": 40.7596198, "lng": -111.886797}, {"city": "Wilmington", "state": "Delaware", "count": 129, "lat": 39.7459468, "lng": -75.546589}, {"city": "Birmingham", "state": "England", "count": 124, "lat": 52.4796992, "lng": -1.9026911}, {"city": "Indianapolis", "state": "Indiana", "count": 120, "lat": 39.7683331, "lng": -86.1583502}, {"city": "Topeka", "state": "Kansas", "count": 119, "lat": 39.049011, "lng": -95.677556}, {"city": "Montgomery", "state": "Alabama", "count": 114, "lat": 32.3777111, "lng": -86.3090775}, {"city": "Atlanta", "state": "Georgia", "count": 113, "lat": 33.7544657, "lng": -84.3898151}, {"city": "New Britain", "state": "Islands Region", "count": 113, "lat": -5.2245897, "lng": 151.5569677}, {"city": "Seattle", "state": "Washington", "count": 112, "lat": 47.6038321, "lng": -122.330062}, {"city": "South Bend", "state": "Indiana", "count": 111, "lat": 41.6833813, "lng": -86.2500066}, {"city": "Waterbury", "state": "Connecticut", "count": 104, "lat": 41.5538091, "lng": -73.0438362}, {"city": "Brownsville", "state": "Texas", "count": 98, "lat": 25.9024289, "lng": -97.4981698}, {"city": "Detroit", "state": "Michigan", "count": 90, "lat": 42.3315509, "lng": -83.0466403}, {"city": "Bridgeport", "state": "Connecticut", "count": 85, "lat": 41.1792695, "lng": -73.1887863}, {"city": "Ogden", "state": "Utah", "count": 83, "lat": 41.2230048, "lng": -111.9738429}, {"city": "Saint Paul", "state": "Minnesota", "count": 83, "lat": 44.9497487, "lng": -93.0931028}, {"city": "Los Angeles", "state": "California", "count": 76, "lat": 34.0536909, "lng": -118.242766}, {"city": "Minneapolis", "state": "Minnesota", "count": 72, "lat": 44.9772995, "lng": -93.2654692}, {"city": "Norwich", "state": "England", "count": 69, "lat": 52.6285576, "lng": 1.2923954}, {"city": "Bismarck", "state": "North Dakota", "count": 68, "lat": 46.808327, "lng": -100.783739}, {"city": "San Antonio", "state": "Texas", "count": 67, "lat": 29.4246002, "lng": -98.4951405}, {"city": "Phoenix", "state": "Arizona", "count": 66, "lat": 33.4484367, "lng": -112.074141}, {"city": "Grand Forks", "state": "North Dakota", "count": 64, "lat": 47.9252104, "lng": -97.0306325}, {"city": "Providence", "state": "Rhode Island", "count": 61, "lat": 41.8239891, "lng": -71.4128343}, {"city": "Manchester", "state": "England", "count": 59, "lat": 53.4794892, "lng": -2.2451148}, {"city": "Fargo", "state": "North Dakota", "count": 57, "lat": 46.877229, "lng": -96.789821}, {"city": "Greenville", "state": "South Carolina", "count": 57, "lat": 34.851354, "lng": -82.3984882}, {"city": "Juneau", "state": "Alaska", "count": 57, "lat": 58.3019613, "lng": -134.4196751}, {"city": "Laramie", "state": "Wyoming", "count": 57, "lat": 41.3116442, "lng": -105.5917876}, {"city": "Newark", "state": "New Jersey", "count": 54, "lat": 40.735657, "lng": -74.1723667}, {"city": "Marshalltown", "state": "Iowa", "count": 50, "lat": 42.048881, "lng": -92.9122672}, {"city": "Savannah", "state": "Georgia", "count": 50, "lat": 32.0790074, "lng": -81.0921335}, {"city": "Philadelphia", "state": "Pennsylvania", "count": 49, "lat": 39.9527237, "lng": -75.1635262}, {"city": "Mandan", "state": "North Dakota", "count": 46, "lat": 46.826415, "lng": -100.889704}, {"city": "Albuquerque", "state": "New Mexico", "count": 45, "lat": 35.0841034, "lng": -106.650985}, {"city": "Anderson", "state": "Texas", "count": 43, "lat": 31.7819242, "lng": -95.6258199}, {"city": "El Centro", "state": "California", "count": 41, "lat": 32.792, "lng": -115.563051}, {"city": "Macon", "state": "Georgia", "count": 41, "lat": 32.8406946, "lng": -83.6324022}, {"city": "Pendleton", "state": "Kentucky", "count": 41, "lat": 38.6914606, "lng": -84.3689142}, {"city": "Charleston", "state": "South Carolina", "count": 40, "lat": 32.7884363, "lng": -79.9399309}, {"city": "Orangeburg", "state": "South Carolina", "count": 40, "lat": 33.4918203, "lng": -80.8556476}, {"city": "Perth Amboy", "state": "New Jersey", "count": 39, "lat": 40.5133218, "lng": -74.2724241}, {"city": "Key West", "state": "Florida", "count": 37, "lat": 24.5548262, "lng": -81.8020722}, {"city": "Laredo", "state": "Texas", "count": 36, "lat": 27.5075005, "lng": -99.5069922}, {"city": "Nome", "state": "Alaska", "count": 36, "lat": 64.4975098, "lng": -165.4061701}, {"city": "Rock Island", "state": "Illinois", "count": 36, "lat": 41.4411786, "lng": -90.5766144}, {"city": "Bisbee", "state": "Arizona", "count": 35, "lat": 31.4417165, "lng": -109.9159946}, {"city": "El Paso", "state": "Texas", "count": 35, "lat": 31.7601164, "lng": -106.4870404}, {"city": "Putnam", "state": "Illinois", "count": 35, "lat": 41.2025915, "lng": -89.2676414}, {"city": "Barre", "state": "Occitanie", "count": 34, "lat": 43.7513, "lng": 2.82702}, {"city": "Spartanburg", "state": "South Carolina", "count": 34, "lat": 34.9498007, "lng": -81.9320157}, {"city": "Lancaster", "state": "Pennsylvania", "count": 33, "lat": 40.0379958, "lng": -76.3056707}, {"city": "O'Neill", "state": "Nebraska", "count": 33, "lat": 42.4577934, "lng": -98.6477823}, {"city": "O'Neill City", "state": "София-град", "count": 33, "lat": 42.6889666, "lng": 23.3175375}];
const MAX_COUNT = 1427;

// Circle sizing on map (meters)
const MIN_RADIUS_M = 8000;
const SCALE_RADIUS_M = 60000;
function radiusMetersForCount(count) {
  return MIN_RADIUS_M + SCALE_RADIUS_M * Math.sqrt(count / MAX_COUNT);
}

// Legend sizing (pixels, relative)
const MIN_R_PX = 6;
const SCALE_R_PX = 24;
function radiusPxForCount(count) {
  return MIN_R_PX + SCALE_R_PX * Math.sqrt(count / MAX_COUNT);
}

const map = L.map('map').setView([39.5, -98.35], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const bounds = L.latLngBounds();

data.forEach(d => {
  const latlng = [d.lat, d.lng];
  bounds.extend(latlng);

  L.circle(latlng, {
    radius: radiusMetersForCount(d.count),
    color: '#1f78b4',
    weight: 1,
    fillColor: '#1f78b4',
    fillOpacity: 0.55
  })
  .bindPopup(`<b>${d.city}, ${d.state}</b><br>Count: <b>${d.count.toLocaleString()}</b>`)
  .addTo(map);
});

if (data.length) {
  map.fitBounds(bounds.pad(0.15));
}

// Legend keyed to actual counts
const legendCounts = [41, 66, 117, 1427];

const legend = L.control({ position: 'bottomright' });
legend.onAdd = function() {
  const div = L.DomUtil.create('div', 'legend');
  div.innerHTML = `<h4>Count legend</h4>`;

  const sorted = [...legendCounts].sort((a,b) => b-a);
  sorted.forEach(c => {
    const r = radiusPxForCount(c);
    const size = Math.ceil((r * 2) + 2);
    const svg = `
      <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
        <circle cx="${size/2}" cy="${size/2}" r="${r}"
          fill="rgba(31,120,180,0.55)" stroke="rgba(31,120,180,1)" stroke-width="1" />
      </svg>
    `;
    const item = document.createElement('div');
    item.className = 'item';
    item.innerHTML = `${svg} <span>${c.toLocaleString()}</span>`;
    div.appendChild(item);
  });

  const note = document.createElement('div');
  note.className = 'note';
  note.textContent = 'Legend bubbles show relative size for these count values.';
  div.appendChild(note);

  return div;
};
legend.addTo(map);
</script>
</body>
</html>
"""

output_path = "us_city_counts_leaflet_map_with_count_legend.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Map written to: {output_path}")
