import React from "react";
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title,
  TimeScale,
} from "chart.js";
import { Scatter, Bar } from "react-chartjs-2";
import "chartjs-adapter-date-fns";

ChartJS.register(
  Title,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  TimeScale
);

function isReversed(yAxisTitle) {
  //reverse y axis for pace (smaller number = faster), but not for speed
  let reversed = false;
  if (yAxisTitle == "Pace (min/km)") {
    reversed = true;
  }
  return reversed;
}

// could combine the plots and add logic to see if xaxis is time based, then
// insert the type: "time" into scales>x
function scatterPlot(chartTitle, yAxisTitle, xAxisTitle, chartData) {
  const options = {
    plugins: {
      responsive: "true",
      maintainAspectRatio: "false",
      title: {
        display: true,
        text: chartTitle,
        color: "black",
        font: {
          size: 16,
          weight: "bold",
        },
        padding: {
          bottom: 10,
        },
      },
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        title: {
          display: true,
          text: yAxisTitle,
          color: "black",
          font: {
            size: 14,
          },
        },
        reverse: isReversed(yAxisTitle),
        border: {
          color: "black",
        },
        grid: {
          tickColor: "black",
        },
        ticks: {
          color: "black",
          font: {
            size: 14,
          },
        },
      },
      x: {
        title: {
          display: true,
          text: xAxisTitle,
          color: "black",
          font: {
            size: 14,
          },
        },
        border: {
          color: "black",
        },
        grid: {
          tickColor: "black",
        },
        ticks: {
          color: "black",
          font: {
            size: 14,
          },
        },
      },
    },
  };
  const data = {
    datasets: [
      {
        label: chartTitle,
        data: chartData,
        backgroundColor: "rgb(43, 125, 17)",
      },
    ],
  };
  return <Scatter options={options} data={data} />;
}

function scatterPlotDate(chartTitle, yAxisTitle, xAxisTitle, chartData) {
  const options = {
    plugins: {
      title: {
        display: true,
        text: chartTitle,
        color: "black",
        font: {
          size: 16,
          weight: "bold",
        },
        padding: {
          bottom: 10,
        },
      },
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        title: {
          display: true,
          text: yAxisTitle,
          color: "black",
          font: {
            size: 14,
          },
        },
        reverse: isReversed(yAxisTitle),
        border: {
          color: "black",
        },
        grid: {
          tickColor: "black",
        },
        ticks: {
          color: "black",
          font: {
            size: 14,
          },
        },
      },
      x: {
        type: "time",
        title: {
          display: true,
          text: xAxisTitle,
          color: "black",
          font: {
            size: 14,
          },
        },
        border: {
          color: "black",
        },
        grid: {
          tickColor: "black",
        },
        ticks: {
          color: "black",
          font: {
            size: 14,
          },
        },
      },
    },
  };
  const data = {
    datasets: [
      {
        label: chartTitle,
        data: chartData,
        backgroundColor: "rgb(43, 125, 17)",
      },
    ],
  };
  return <Scatter options={options} data={data} />;
}

// function BarChart(chartTitle, yAxisTitle, xAxisTitle, chartData) {
//   return <Bar options={options} data={data} />
// }

export function Plot({ chartTitle, yAxisTitle, xAxisTitle, chartData }) {
  let plot = null;

  switch (xAxisTitle) {
    case "Distance (km)":
    case "Elevation (m)":
    case "Perceived Effort (1 [very easy] - 10 [maximum effort])":
      plot = scatterPlot(chartTitle, yAxisTitle, xAxisTitle, chartData);
      break;
    case "Date":
      plot = scatterPlotDate(chartTitle, yAxisTitle, xAxisTitle, chartData);
      break;
  }
  return plot;
}
