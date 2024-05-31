// SIDEBAR TOGGLE

let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebarOpen = false;
  }
}

 // PIE CHART
 const pieChartOptions = {
  series: [60, 40], // Utilized and Remaining
  chart: {
      width: 380,
      type: 'pie',
  },
  labels: ['Utilized', 'Remaining'],
  colors: ['#4f35a1', '#246dec'],
  responsive: [{
      breakpoint: 480,
      options: {
          chart: {
              width: 200
          },
          legend: {
              position: 'bottom'
          }
      }
  }]
};

const pieChart = new ApexCharts(
  document.querySelector('#pie-chart'),
  pieChartOptions
);
pieChart.render();





// BAR CHART
const barChartOptions = {
    series: [{
        name: 'Project Count',
        data: [15, 20, 10, 25], // Sample project counts for each department
    }],
    chart: {
        height: 350,
        type: 'bar',
        toolbar: {
            show: false,
        },
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded'
        },
    },
    colors: ['#4f35a1'],
    dataLabels: {
        enabled: false,
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    xaxis: {
        categories: ['Department A', 'Department B', 'Department C', 'Department D'], // Sample department names
    },
    yaxis: {
        title: {
            text: 'Project Count',
        },
    },
    fill: {
        opacity: 1
    },
    tooltip: {
        enabled: true,
        y: {
            formatter: function (val) {
                return val + " projects";
            }
        }
    }
  };
  
  const barChart = new ApexCharts(
    document.querySelector('#area-chart'),
    barChartOptions
  );
  barChart.render();
  



// Distribution of LDF - Pie Chart
const pieChartOption = {
    series: [30, 20, 25, 15, 10], // Sample data for LDF distribution
    chart: {
      width: 380,
      type: 'pie',
      toolbar: {
        show: false
      }
    },
    labels: ['Department A', 'Department B', 'Department C', 'Department D', 'Department E'], // Sample departments
    colors: ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0', '#FF5722'], // Updated colors for each department
    responsive: [{
      breakpoint: 480,
      options: {
        chart: {
          width: 200
        },
        legend: {
          position: 'bottom'
        }
      }
    }],
    legend: {
      position: 'right',
      offsetY: 0,
      height: 230,
    },
    dataLabels: {
      enabled: false
    }
  };
  
  const pieCharts = new ApexCharts(
    document.querySelector('#pie-charts'),
    pieChartOption
  );
  pieCharts.render();
  
  // Utilization Rate of Each Category - Bar Chart
const utilizationChartOptions = {
    series: [{
      name: 'Utilization Rate',
      data: [70, 80, 60, 85], // Sample data for utilization rates (out of 100) for obligations, disbursements, procurements, and projects
    }],
    chart: {
      height: 350,
      type: 'bar',
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        endingShape: 'rounded',
      },
    },
    colors: ['#4f35a1'],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['transparent'],
    },
    xaxis: {
      categories: ['Obligations', 'Disbursements', 'Procurements', 'Projects'], // Categories representing obligations, disbursements, procurements, and projects
    },
    yaxis: {
      title: {
        text: 'Utilization Rate (%)',
      },
    },
  };
  
  const utilizationChart = new ApexCharts(
    document.querySelector('#utilization-chart'),
    utilizationChartOptions
  );
  utilizationChart.render();


  
  