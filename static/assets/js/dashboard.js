/* globals Chart:false, feather:false */

;window.setTimeout(function () {
  //values
  var values = document.getElementById("values");

  var monday = values.getAttribute("data-monday");
  var tuesday = values.getAttribute("data-tuesday");
  var wednessday = values.getAttribute("data-wednessday");
  var thursday = values.getAttribute("data-thursday");
  var friday = values.getAttribute("data-friday");
  var saturday = values.getAttribute("data-saturday");
  var sunday = values.getAttribute("data-sunday");

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          sunday,
          monday,
          tuesday,
          wednessday,
          thursday,
          friday,
          saturday
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  });
},1000);
