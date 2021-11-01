$(function () {
  'use strict'

  var ticksStyle = {
    fontColor: '#1c718d',
    fontStyle: 'bold'
  }

  var mode = 'index'
  var intersect = true

  // eslint-disable-next-line no-unused-vars
  var $estudiantesSemanaChart = $('#estudiantes-semana-chart')
  const lista_cantidad_estudiantes_dias_actual = JSON.parse(document.getElementById('lista_cantidad_estudiantes_dias_actual').textContent);
  const lista_cantidad_estudiantes_dias_pasado = JSON.parse(document.getElementById('lista_cantidad_estudiantes_dias_pasado').textContent);
  const maximo = JSON.parse(document.getElementById('maximo').textContent);
  // eslint-disable-next-line no-unused-vars
 
var estudiantesSemana = new Chart($estudiantesSemanaChart, {
      type: 'line',
      data: {
        labels: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
        datasets: [
          {
            label: 'Semana Actual',
            data: lista_cantidad_estudiantes_dias_actual,
            borderColor: '#0b5ad4',
            backgroundColor:'#007bff',
          },
          {
            label: 'Semana Anterior',
            data:lista_cantidad_estudiantes_dias_pasado ,
            borderColor: '#6c757d',
            backgroundColor: '#ced4da',
          },
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
          },
        },
        scales: {
        y: {
            max: maximo+1,
            min: -0.2,
            ticks: {
                stepSize: 1
            }
        }
    }
        
      },
  })
var $estudiantesMatriSemanaChart = $('#estudiantes-matriculados-semana-chart')
  // eslint-disable-next-line no-unused-vars
var estudiantesMatriSemana = new Chart($estudiantesMatriSemanaChart, {
    type: 'bar',
    data: {
       labels: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
      datasets: [
        {
          backgroundColor: '#007bff',
          borderColor: '#007bff',
          data: [30, 20, 10, 25, 60, 13,23]
        },
        {
          backgroundColor: '#ced4da',
          borderColor: '#ced4da',
          data: [20, 10, 15, 30, 45, 14,20]
        }
      ]
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        mode: mode,
        intersect: intersect
      },
      hover: {
        mode: mode,
        intersect: intersect
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          // display: false,
          gridLines: {
            display: true,
            lineWidth: '4px',
            color: 'rgba(0, 0, 0, .2)',
            zeroLineColor: 'transparent'
          },
          ticks:  ticksStyle
        }],
        xAxes: [{
          display: true,
          gridLines: {
            display: false
          },
          ticks: ticksStyle
        }]
      }
    }
})
  /*gradica de los no matriculados*/
  var $estudiantesNoMatriculadosChart = $('#estudiantes-NoMatriculados-chart')
  var barColors = [,,"red",,"red","red"];
  // eslint-disable-next-line no-unused-vars
var $estudiantesNoMatriculados = new Chart($estudiantesNoMatriculadosChart, {
    type: 'bar',
    data: {
       labels: ['Regla', 'Playa', 'Guanabacoa', '10 Octubre', 'San Miguel', 'Cotorro'],
      datasets: [
        {
          backgroundColor: barColors,
          borderColor: '#007bff',
          data: [10, 20, 50, 12, 100, 32,24]
        }
      ]
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        mode: mode,
        intersect: intersect
      },
      hover: {
        mode: mode,
        intersect: intersect
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          // display: false,
          gridLines: {
            display: true,
            lineWidth: '10px',
            color: '#ced4da',
            zeroLineColor: 'transparent'
          },
          ticks:  ticksStyle
        }],
        xAxes: [{
          display: true,
          gridLines: {
            display: false
          },
          ticks: ticksStyle
        }]
      }
    }
})
  
  var xyValues = [
  {x:50, y:7},
  {x:60, y:8},
  {x:70, y:8},
  {x:80, y:9},
  {x:90, y:9},
  {x:100, y:9},
  {x:110, y:10},
  {x:120, y:11},
  {x:130, y:14},
  {x:140, y:14},
  {x:150, y:15}
];

new Chart("myChart", {
  type: "scatter",
  data: {
    datasets: [{
      pointRadius: 4,
      pointBackgroundColor: "red",
      data: xyValues
    }]
  },
  options: {
    legend: {display: false},
    scales: {
      xAxes: [{ticks: {min: 40, max:160}}],
      yAxes: [{ticks: {min: 6, max:16}}],
    }
  }
});

//-------------
    //- DONUT CHART -
    //-------------
    // Get context with jQuery - using jQuery's .get() method.
    var municipiosCursosCanvas = $('#municipios-cursos-chart').get(0).getContext('2d')
    var donutData        = {
      labels: [
          'San Miguel del Padrón',
          'Regla',
          'Diez de Octubre',
          'Palya',
          'Cotorro'
      ],
      datasets: [
        {
          data: [60,50,45,30,24],
          backgroundColor : ['#624b20', '#0f1ab9', '#f39c12', '#00c0ef', '#3c8dbc'],
        }
      ]
    }
    var donutOptions     = {
      maintainAspectRatio : false,
      responsive : true,
    }
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    new Chart(municipiosCursosCanvas, {
      type: 'doughnut',
      data: donutData,
      options: donutOptions
    })
  
})
