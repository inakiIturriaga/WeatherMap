let marker;

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(-34.6037, -58.3816),
        zoom: 10,
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    map.addListener("click", (event) => {
        addMarker(event.latLng);
    });
    fetch('/pmarker')
        .then(response => response.json())
        .then(data => {
            var lat = data.lat;
            var lon = data.lon;
            var latLng = new google.maps.LatLng(lat, lon);
            addMarker(latLng);
            map.setCenter(latLng);
        });
}

function addMarker(location) {

    if (marker) {
        // Move the existing marker
        marker.setPosition(location);
    } else {
        // Create a new marker
        marker = new google.maps.Marker({
            position: location,
            map: map,
        });
    }

    $.ajax({
        url: "/marker",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            lat: location.lat(),
            lng: location.lng()
        })
    }).done(function(response) {
        var temp = response.temp;
        var city = response.city;
        var humidity = response.humidity;
        var deg = response.deg;
        var speed = response.speed;
        document.getElementById('temperature-display').innerHTML = 'Temperature: ' + temp.toFixed(2) + "°C";
        document.getElementById('humidity-display').innerHTML = 'Humidity: ' + humidity + "%";
        document.getElementById('speed-display').innerHTML = 'Wind speed: ' + speed.toFixed(2) + "km/h";
        document.getElementById('wind-arrow').style.transform = 'rotate(' + -(deg) + 'deg)';
        document.getElementById('city-display').innerHTML = 'City: ' + city;

    });
}


