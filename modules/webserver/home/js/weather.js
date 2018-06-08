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
google.load('visualization', '1', {packages: ['corechart', 'line']});
google.setOnLoadCallback(drawCurveTypes);

function drawCurveTypes() {
  $.getJSON('/js/day.json', function( jsondata ) {
    if (typeof jsondata != 'undefined') {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Hour');
        data.addColumn('number', 'External');
        data.addColumn('number', 'Internal');

        data.addRows( jsondata );

        var options = {
          backgroundColor: { fill:'transparent' },
          colors: ['#55f', '#5f5'],

          curveType: 'function',
          hAxis: {
            title: 'Hour',
          },
          vAxis: {
            title: 'Temperature',
            format:'##',
          },
        };

        var chart = new google.visualization.LineChart(document.getElementById('chartdiv'));
        chart.draw(data, options);
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
});
