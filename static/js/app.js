fetch('/api/potholes')
  .then(res => res.json())
  .then(data => {
    initMap(data);
    drawChart(data);
  });

function initMap(potholes) {
  const container = document.getElementById('map');
  const options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 6
  };
  const map = new kakao.maps.Map(container, options);

  potholes.forEach(p => {
    const marker = new kakao.maps.Marker({
      map: map,
      position: new kakao.maps.LatLng(p.latitude, p.longitude)
    });

    const content = `
      <div style="padding:10px;">
        <b>ID:</b> ${p.id}<br>
        <b>심각도:</b> ${p.severity}<br>
        <b>상태:</b> ${p.status}<br>
        <img src="${p.image_url}" width="100" style="margin-top:5px;">
      </div>`;
    const infowindow = new kakao.maps.InfoWindow({ content });
    kakao.maps.event.addListener(marker, 'click', () => infowindow.open(map, marker));
  });
}

function drawChart(potholes) {
  const ctx = document.getElementById('chart').getContext('2d');
  const resolved = potholes.filter(p => p.status === "Resolved").length;
  const unresolved = potholes.filter(p => p.status === "Unresolved").length;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['처리 완료', '미처리'],
      datasets: [{
        data: [resolved, unresolved],
        backgroundColor: ['#4CAF50', '#F44336']
      }]
    },
    options: {
      plugins: {
        title: { display: true, text: '포트홀 처리 현황' }
      }
    }
  });
}
