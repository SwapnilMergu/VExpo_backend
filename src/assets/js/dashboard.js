
var no_of_visitors = [];
var no_of_bookings = [];
var categories=[]

// var no_of_visitors_filter = [];
// var no_of_bookings_filter = [];
// var categories_filter=[]
// var todaysDate = new Date();

// function filterDates(selectedDate) {
//   const categories_filter = categories.filter(categoryDate => {
//     return categoryDate === selectedDate;
//   });
//   for (let index = 0; index < categories_filter.length; index++) {
    
//     no_of_bookings_filter.push(no_of_bookings[categories.indexOf(categories_filter[index])]);
//     no_of_visitors_filter.push(no_of_visitors[categories.indexOf(categories_filter[index])]);
    
//   }

// }


$(function () {


  // =====================================
  // Profit
  // =====================================
  console.log("inside ", user_role)

    if(user_role=='vendor'){
      console.log("inside vendor")
      fetch('/api/dashboard')
    .then(response => response.json())
    .then(data => {
      no_of_bookings=data.data.bookings;
      no_of_visitors=data.data.values;
      categories= data.data.labels;
      // console.log(no_of_bookings,"\n",no_of_visitors,"\n",categories)
      var chart = {
        series: [
          { name: "No. of Visitors", data: no_of_visitors },
          { name: "No. of Bookings", data: no_of_bookings },
        ],
    
        chart: {
          type: "bar",
          height: 400,
          offsetX: -15,
          toolbar: { show: true },
          foreColor: "#adb0bb",
          fontFamily: 'inherit',
          sparkline: { enabled: false },
        },
    
    
        colors: ["#f76b07", "#333333"],
    
    
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "35%",
            borderRadius: [6],
            borderRadiusApplication: 'end',
            borderRadiusWhenStacked: 'all'
          },
        },
        markers: { size: 0 },
    
        dataLabels: {
          enabled: false,
        },
    
    
        legend: {
          show: false,
        },
    
    
        grid: {
          borderColor: "rgba(0,0,0,0.1)",
          strokeDashArray: 3,
          xaxis: {
            lines: {
              show: false,
            },
          },
        },
    
        xaxis: {
          type: "category",
          categories: data.data.labels,
          labels: {
            style: { cssClass: "grey--text lighten-2--text fill-color" },
          },
        },
    
    
        yaxis: {
          show: true,
          min: 0,
          max: data.data.max_val,
          tickAmount: 5 ,
          labels: {
            style: {
              cssClass: "grey--text lighten-2--text fill-color",
            },
          },
        },
        stroke: {
          show: true,
          width: 3,
          lineCap: "butt",
          colors: ["transparent"],
        },
    
    
        tooltip: { theme: "light" },
    
        responsive: [
          {
            breakpoint: 600,
            options: {
              plotOptions: {
                bar: {
                  borderRadius: 3,
                }
              },
            }
          }
        ]
    
    
      };
    
      var chart = new ApexCharts(document.querySelector("#chart"), chart);
      chart.render();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
    }
    if(user_role=='admin'){
      console.log("inside admin")
      console.log("/api/dashboard/admin/categories")
      fetch('/api/dashboard/admin/categories')
    .then(response => response.json())
    .then(data => {
      no_of_visitors=data.data.values;
      var labels= data.data.labels;
      console.log("\n",no_of_visitors,"\n",categories)
      
      var chart = {
        series: [
          { name: "No. of Visitors", data: no_of_visitors },
        ],
    
        chart: {
          type: "bar",
          height: 400,
          offsetX: -15,
          toolbar: { show: true },
          foreColor: "#adb0bb",
          fontFamily: 'inherit',
          sparkline: { enabled: false },
        },
    
    
        colors: ["#f76b07", "#333333"],
    
    
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "35%",
            borderRadius: [6],
            borderRadiusApplication: 'end',
            borderRadiusWhenStacked: 'all'
          },
        },
        markers: { size: 0 },
    
        dataLabels: {
          enabled: false,
        },
    
    
        legend: {
          show: false,
        },
    
    
        grid: {
          borderColor: "rgba(0,0,0,0.1)",
          strokeDashArray: 3,
          xaxis: {
            lines: {
              show: false,
            },
          },
        },
    
        xaxis: {
          type: "category",
          categories: labels,
          labels: {
            style: { cssClass: "grey--text lighten-2--text fill-color" },
          },
        },
    
    
        yaxis: {
          show: true,
          min: 0,
          max: data.data.max_val,
          tickAmount: 5 ,
          labels: {
            style: {
              cssClass: "grey--text lighten-2--text fill-color",
            },
          },
        },
        stroke: {
          show: true,
          width: 3,
          lineCap: "butt",
          colors: ["transparent"],
        },
    
    
        tooltip: { theme: "light" },
    
        responsive: [
          {
            breakpoint: 600,
            options: {
              plotOptions: {
                bar: {
                  borderRadius: 3,
                }
              },
            }
          }
        ]
    
    
      };
    
      var chart = new ApexCharts(document.querySelector("#chart"), chart);
      chart.render();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

    }

    if(user_role=='super'){
      console.log("inside superuser")
      fetch('/api/dashboard/superuser')
    .then(response => response.json())
    .then(data => {
        console.log("monthcount",data.data.month_counts)
        console.log("data: ",data.data)
     
        no_of_visitors=data.data.values;
        categories=data.data.labels
      var chart = {
        series: [
          { name: "No. of Registrations", data: no_of_visitors },
        ],
    
        chart: {
          type: "bar",
          height: 400,
          offsetX: -15,
          toolbar: { show: true },
          foreColor: "#adb0bb",
          fontFamily: 'inherit',
          sparkline: { enabled: false },
        },
    
    
        colors: ["#f76b07", "#333333"],
    
    
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "35%",
            borderRadius: [6],
            borderRadiusApplication: 'end',
            borderRadiusWhenStacked: 'all'
          },
        },
        markers: { size: 0 },
    
        dataLabels: {
          enabled: false,
        },
    
    
        legend: {
          show: false,
        },
    
    
        grid: {
          borderColor: "rgba(0,0,0,0.1)",
          strokeDashArray: 3,
          xaxis: {
            lines: {
              show: false,
            },
          },
        },
    
        xaxis: {
          type: "category",
          categories: categories,
          labels: {
            style: { cssClass: "grey--text lighten-2--text fill-color" },
          },
        },
    
    
        yaxis: {
          show: true,
          min: 0,
          max: data.data.max_val,
          tickAmount: 5 ,
          labels: {
            style: {
              cssClass: "grey--text lighten-2--text fill-color",
            },
          },
        },
        stroke: {
          show: true,
          width: 3,
          lineCap: "butt",
          colors: ["transparent"],
        },
    
    
        tooltip: { theme: "light" },
    
        responsive: [
          {
            breakpoint: 600,
            options: {
              plotOptions: {
                bar: {
                  borderRadius: 3,
                }
              },
            }
          }
        ]
    
    
      };
    
      var chart = new ApexCharts(document.querySelector("#chart"), chart);
      chart.render();
      
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

    }

    // =====================================
  // Breakup
  // =====================================
  // var breakup = {
  //   color: "#adb5bd",
  //   series: [38, 40, 25],
  //   labels: ["2022", "2021", "2020"],
  //   chart: {
  //     width: 180,
  //     type: "donut",
  //     fontFamily: "Plus Jakarta Sans', sans-serif",
  //     foreColor: "#adb0bb",
  //   },
  //   plotOptions: {
  //     pie: {
  //       startAngle: 0,
  //       endAngle: 360,
  //       donut: {
  //         size: '75%',
  //       },
  //     },
  //   },
  //   stroke: {
  //     show: false,
  //   },

  //   dataLabels: {
  //     enabled: false,
  //   },

  //   legend: {
  //     show: false,
  //   },
  //   colors: ["#f76b07", "#ecf2ff", "#F9F9FD"],

  //   responsive: [
  //     {
  //       breakpoint: 991,
  //       options: {
  //         chart: {
  //           width: 150,
  //         },
  //       },
  //     },
  //   ],
  //   tooltip: {
  //     theme: "dark",
  //     fillSeriesColor: false,
  //   },
  // };

  // var chart = new ApexCharts(document.querySelector("#breakup"), breakup);
  // chart.render();



  // =====================================
  // Earning
  // =====================================
  var earning = {
    chart: {
      id: "sparkline3",
      type: "area",
      height: 60,
      sparkline: {
        enabled: true,
      },
      group: "sparklines",
      fontFamily: "Plus Jakarta Sans', sans-serif",
      foreColor: "#adb0bb",
    },
    series: [
      {
        name: "Earnings",
        color: "#49BEFF",
        data: [25, 66, 20, 40, 12, 58, 20],
      },
    ],
    stroke: {
      curve: "smooth",
      width: 2,
    },
    fill: {
      colors: ["#f3feff"],
      type: "solid",
      opacity: 0.05,
    },

    markers: {
      size: 0,
    },
    tooltip: {
      theme: "dark",
      fixed: {
        enabled: true,
        position: "right",
      },
      x: {
        show: false,
      },
    },
  };
  new ApexCharts(document.querySelector("#earning"), earning).render();
})



// function formatDate(dateString) {
//   const parts = dateString.split('-');
//   const year = parts[0];
//   const month = parts[1].padStart(2, '0');
//   const day = parts[2].padStart(2, '0');

//   return `${day}/${month}/${year}`;
// }

// $(document).ready(function() {
// $('#filterDate').change(function() {
//   const selectedDate = $(this).val();
//   // Your logic to filter data based on selectedDate goes here
//   const date= formatDate(selectedDate);
//   console.log("Selected date:", date);  // Example placeholder
//   document.getElementById("date-container").innerHTML = date+" - Bookings" ;
//   console.log(no_of_bookings)
// });
// });