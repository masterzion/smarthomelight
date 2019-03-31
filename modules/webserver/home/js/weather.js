// -----------  get data result  -----------
function roundToTwo(num) {
    return +(Math.round(num + "e+2")  + "e-2");
}

function getLastTempResult() {
  $.getJSON('/getmodules/thermometer/external_thermometer', function( data ) {
    if (typeof data != 'undefined') {
        data=roundToTwo(data);
        ar=data.toString().split(".");
        $("#currenttemp").html(  ar[0]  );
        $("#currenttemp_decimal").html(  ar[1]  );
    }
  });

  $.getJSON('/getmodules/thermometer/internal_thermometer_temperature', function( data ) {
        data=roundToTwo(data);
        ar=data.toString().split(".");
        $("#currenttemp_int").html(  ar[0]  );
        $("#currenttemp_int_decimal").html(  ar[1]  );
  });


  $.getJSON('/getmodules/thermometer/internal_thermometer_humidity', function( data ) {
        data=roundToTwo(data);
        ar=data.toString().split(".");
        $("#humidity_int").html(  ar[0]  );
        $("#humidity_int_decimal").html(  ar[1]  );
  });

}

// ----------- charts  -----------
function drawCurveTypes() {
  $.getJSON('/js/day.json', function( jsondata ) {
    if (typeof jsondata != 'undefined') {
      json_labels=[];
      json_internal=[];
      json_external=[];
      jsondata.forEach(function(entry) {
        json_labels.push(entry[0]);
        json_external.push(entry[1]);
        json_internal.push(entry[2]);
      });
      var config = {
        type: 'line',
        data: {
          labels: json_labels,
          datasets: [{
            label: 'Internal',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: json_internal,
            fill: false,
          }, {
            label: 'External',
            fill: false,
            backgroundColor: 'rgb(54, 162, 235)',
            borderColor: 'rgb(54, 162, 235)',
            data:  json_external,
          }]
        },
        options: {
          responsive: true,
          title: {
            display: true,
            text: 'Today'
          },
          tooltips: {
            mode: 'index',
            intersect: false,
          },
          hover: {
            mode: 'nearest',
            intersect: true
          },
          scales: {
            xAxes: [{
              display: true,
              scaleLabel: {
                display: true,
                labelString: 'Time'
              }
            }],
            yAxes: [{
              display: true,
              scaleLabel: {
                display: true,
                labelString: 'Value'
              }
            }]
          }
        }
      };
      ctx = document.getElementById('canvas').getContext('2d');
      window.myLine = new Chart(ctx, config);
    }
  });
}

// ----------- auto refresh  -----------
ChartCounterDelay=0;
setInterval(function() {
    getLastTempResult();
    ChartCounterDelay++;
    if ( ChartCounterDelay == 100  ) {
       ChartCounterDelay=0;
       drawCurveTypes();
    }
}, 3 * 1000); // 60 * 1000 milsec

$( window ).load(function() {
  getLastTempResult();
  drawCurveTypes();
});
