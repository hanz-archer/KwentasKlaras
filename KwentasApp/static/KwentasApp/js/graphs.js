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
// ---------- CHARTS ----------



// ---------- NEW CHARTS ----------

// COMPARISON BAR CHART (Comparison Section)
const comparisonBarChartOptions = {
  series: [
    {
      name: 'Current Year',
      data: [44, 55, 41, 64, 22],
    },
    {
      name: 'Previous Year',
      data: [53, 32, 33, 52, 13],
    },
  ],
  chart: {
    type: 'bar',
    background: 'transparent',
    height: 350,
    stacked: false,
    toolbar: {
      show: false,
    },
  },
  colors: ['#ff9800', '#3f51b5'],
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '50%',
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent'],
  },
  tooltip: {
    theme: 'dark',
  },
  xaxis: {
    categories: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5'],
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: {
    title: {
      text: 'Revenue',
      style: {
        color: '#f5f7ff',
      },
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
};

const comparisonBarChart = new ApexCharts(
  document.querySelector('#comparison-bar-chart'),
  comparisonBarChartOptions
);
comparisonBarChart.render();

// COMPARISON AREA CHART (Comparison Section)
const comparisonAreaChartOptions = {
  series: [
    {
      name: 'Current Year',
      data: [30, 40, 35, 50, 49, 60, 70],
    },
    {
      name: 'Previous Year',
      data: [20, 29, 37, 36, 44, 45, 50],
    },
  ],
  chart: {
    type: 'area',
    background: 'transparent',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#00bcd4', '#8bc34a'],
  dataLabels: {
    enabled: false,
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.7,
      opacityTo: 0.2,
      stops: [0, 90, 100],
    },
  },
  stroke: {
    curve: 'smooth',
    width: 2,
  },
  grid: {
    borderColor: '#55596e',
    xaxis: {
      lines: {
        show: true,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  xaxis: {
    type: 'datetime',
    categories: ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01', '2024-07-01'],
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: {
    title: {
      text: 'Orders',
      style: {
        color: '#f5f7ff',
      },
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  tooltip: {
    theme: 'dark',
    x: {
      format: 'dd MMM yyyy',
    },
  },
};

const comparisonAreaChart = new ApexCharts(
  document.querySelector('#comparison-area-chart'),
  comparisonAreaChartOptions
);
comparisonAreaChart.render();





// DEPARTMENT CHART (Department Section)
const departmentChartOptions = {
  series: [
    {
      name: 'Employees',
      data: [40, 55, 30, 70, 60, 80],
    },
  ],
  chart: {
    type: 'bar',
    background: 'transparent',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#673ab7'],
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '50%',
      endingShape: 'rounded',
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent'],
  },
  xaxis: {
    categories: ['HR', 'Engineering', 'Sales', 'Marketing', 'Finance', 'Support'],
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: {
    title: {
      text: 'Number of Employees',
      style: {
        color: '#f5f7ff',
      },
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  fill: {
    opacity: 1,
  },
  tooltip: {
    theme: 'dark',
  },
  legend: {
    show: false,
  },
};

const departmentChart = new ApexCharts(
  document.querySelector('#department-chart'),
  departmentChartOptions
);
departmentChart.render();
