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

export const options = {
  plugins: {
    title: {
      display: true,
      text: "Pace vs Elevation (m) - test plot",
      color: "black",
      font: {
        size: 14,
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
        text: "Pace (min/km)",
        color: "black"
      },
      reverse: true,
      border: {
        color: "black"},
      grid: {
        tickColor: "black"},
      ticks: {
        color: "black"}
    },
    x: {
      title: {
        display: true,
        text: "Elevation (m)",
        color: "black"
      },
      border: {
        color: "black"},
      grid: {
        tickColor: "black"},
      ticks: {
        color: "black"}
    }
  }
};

export const data = {
  datasets: [
    {
      label: "Pace vs Elevation (test plot)",
      data: [{x: 100, y: 7.2}, {x: 70, y: 6.6}, {x: 50, y: 6.5}, {x: 30, y: 5.8}, {x: 43, y: 6.45}, {x: 90, y: 7.4}],
      backgroundColor: "rgb(43, 125, 17)"
    }
  ]
};

export function PaceVsElevation() {
  return <Scatter options={options} data={data} />;
}