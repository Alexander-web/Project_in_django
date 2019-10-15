var ctx = document.getElementById('myChart').getContext('2d');
// Global Options
Chart.defaults.global.defaultFontFamily = 'Lato';
Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.defaultFontColor = '#777';
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'Характеристики',
            backgroundColor: 'rgb(54, 162, 235, 0.5)',
            borderColor: 'dark',
            data: [45, 10, 5, 2, 20, 30, 0]
        }]
    },
    // Configuration options go here
    options: {}
});