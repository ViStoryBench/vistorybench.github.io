import Chart from 'chart.js/auto';

declare global {
  interface Window {
    Chart: typeof Chart;
  }
}

if (typeof window !== 'undefined') {
  window.Chart = Chart;
}
