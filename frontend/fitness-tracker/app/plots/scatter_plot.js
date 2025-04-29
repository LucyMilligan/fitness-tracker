import React from 'react';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';

ChartJS.register(Title, LinearScale, PointElement, LineElement, Tooltip, Legend)

export function ScatterPlot({chartTitle, yAxisTitle, xAxisTitle, chartData}) {
  //reverse y axis for pace (smaller number = faster), but not for speed
  let reversed = false
  if (yAxisTitle == "Pace (min/km)") {
    reversed = true
  }

  const options = {
    plugins: {
      title: {
        display: true,
        text: chartTitle,
        color: "black",
        font: {
          size: 16,
          weight: "bold"
        },
        padding: {
          bottom: 10
        }
      },
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        title: {
          display: true,
          text: yAxisTitle,
          color: "black",
          font: {
            size: 14
          }
        },
        reverse: reversed,
        border: {
          color: "black"},
        grid: {
          tickColor: "black"},
        ticks: {
          color: "black",
          font: {
            size: 14
          }
        }
      },
      x: {
        title: {
          display: true,
          text: xAxisTitle,
          color: "black",
          font: {
            size: 14
          }
        },
        border: {
          color: "black"},
        grid: {
          tickColor: "black"},
        ticks: {
          color: "black",
          font: {
            size: 14
          }
        }
      }
    }
  }
  const data = {
    datasets: [
      {
        label: chartTitle,
        data: chartData,
        backgroundColor: "rgb(43, 125, 17)"
      }
    ]
  }
  return <Scatter options={options} data={data} />
}