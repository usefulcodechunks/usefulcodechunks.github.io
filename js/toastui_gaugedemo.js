
var chart = tui.chart; /* namespace */

var container = document.getElementById('toastui_demo');
var data = {
    categories: ['User Breakdown'],
    seriesAlias: {
        pie1: 'pie',
        pie2: 'pie',
        pie3: 'pie',

    },
    series: {
        pie1: [
            {
                name: 'Mentorship Users',
                data: 46
            },
            {
                name: 'Non Mentorship Users',
                data: 23
            }
        ],
        pie2: [

            {
                name: 'Active Users',
                data: 67
            },
            {
                name: 'Non-Active Users',
                data: 33
            }
        ],
        pie3: [

            {
                name: 'efef 1',
                data: 5
            },
            {
                name: 'sff 1',
                data: 7.25
            }
        ]
    }
};
var options = {
    chart: {
        width: 400,
        height: 400,
        title: 'User Breakdown'
    },
    series: {
        pie1: {
            radiusRange: ['75%','78%'],
            showLabel: false,
            showLegend: false,
            startAngle: 0,
            endAngle: 270
        },
        pie2: {
            radiusRange: ['80%', '100%'],
            showLabel: false,
            showLegend: false,
            startAngle: 0,
            endAngle: 270
        },
        pie3: {
            radiusRange: ['63%', '74%'],
            showLabel: false,
            showLegend: false,
            startAngle: 0,
            endAngle: 270
        }
    },
    legend: {
        visible: false
    },
    tooltip: {
        suffix: '%'
    },
    theme: 'newTheme'
};

tui.chart.registerTheme('newTheme', {
    series: {
        pie1: {
            colors: ['#00a9ff', '#ffb840', '#ff5a46', '#00bd9f', '#785fff', '#f28b8c', '#989486', '#516f7d', '#29dbe3', '#dddddd'],
            label: {
                color: '#fff',
                fontFamily: 'sans-serif'
            }
        },
        pie2: {
            colors: [
                '#33baff', '#66ccff',
                '#ffc666', '#ffd48c', '#FFDB9F',
                '#ff7b6b', '#ff9c90',
                '#33cab2',
                '#937fff', '#f5a2a3'],
            label: {
                color: '#fff',
                fontFamily: 'sans-serif'
            }
        },
        pie3: {
            colors: [
                '#33baff', '#66ccff',
                '#ffc666', '#ffd48c', '#FFDB9F',
                '#ff7b6b', '#ff9c90',
                '#33cab2',
                '#937fff', '#f5a2a3'],
            label: {
                color: '#fff',
                fontFamily: 'sans-serif'
            }
        }
    }
});

tui.chart.comboChart(container, data, options);
