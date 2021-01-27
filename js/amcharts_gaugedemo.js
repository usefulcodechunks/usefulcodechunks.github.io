am4core.useTheme(am4themes_material); 		// Theme Selection

function color_value(percent){

		if(percent <= 15){
			color = am4core.color("#DB4437");
		}
		else if(percent <= 45){
			color = am4core.color("#F4B400");
		}
		else if(percent > 45){
			color = am4core.color("#0F9D58");
		}
		return color
}









// Assinging Chart to Div
var chart = am4core.create("amcharts_demo", am4charts.RadarChart);

var colorSet = new am4core.ColorSet();
console.log(colorSet.color)

// Add data
chart.data = [
	{
	  "category": "Mentorship Users",
	  "value": 15,
		"delta":10,
	  "full": 67
	},
	{
	  "category": "Active Users",
	  "value": 67,
		"delta":10,
	  "full": 100
	},
	{
	  "category": "Total Users",
	  "value": 100,
		"delta":0,
	  "full": 100
	}];

// Make chart not full circle
chart.startAngle = -90;
chart.endAngle = 180;
chart.innerRadius = am4core.percent(50);

// Set number format
chart.numberFormatter.numberFormat = "#.#'%'";

// Category Label Code
var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "category";
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.renderer.grid.template.strokeOpacity = 0;
categoryAxis.renderer.labels.template.horizontalCenter = "right";
categoryAxis.renderer.labels.template.fontWeight = 500;
categoryAxis.renderer.labels.template.adapter.add("fill", function(fill, target) {
	return (target.dataItem.index >= 0) ? am4core.color("#1c1c1c") : fill;});
categoryAxis.renderer.minGridDistance = 10;



// Value Axis Code
var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
valueAxis.renderer.grid.template.strokeOpacity = 0;
valueAxis.min = 1;
valueAxis.max = 100;
valueAxis.strictMinMax = true;
valueAxis.logarithmic = false;


// Radar Chart Full Gauge
var series1 = chart.series.push(new am4charts.RadarColumnSeries());
series1.dataFields.valueX = "full";
series1.dataFields.categoryY = "category";
series1.clustered = false;
series1.columns.template.fill = new am4core.InterfaceColorSet().getFor("alternativeBackground");
series1.columns.template.fillOpacity = 0.08;
series1.columns.template.cornerRadiusTopLeft = 20;
series1.columns.template.strokeWidth = 0;
series1.columns.template.radarColumn.cornerRadius = 20;

// Radar Chart Full Gauge
// var series3 = chart.series.push(new am4charts.RadarColumnSeries());
// series3.dataFields.valueX = "delta";
// series3.dataFields.categoryY = "category";
// series3.clustered = false;
// series3.columns.template.fill = am4core.color("#1c1c1c");
// series3.columns.template.fillOpacity = 0.5;
// series3.columns.template.cornerRadiusTopLeft = 20;
// series3.columns.template.strokeWidth = 0;
// series3.columns.template.radarColumn.cornerRadius = 20;

// Radar Chart Highlighted Gauge
var series2 = chart.series.push(new am4charts.RadarColumnSeries());
series2.dataFields.valueX = "value";
series2.dataFields.categoryY = "category";
series2.clustered = false;
series2.columns.template.strokeWidth = 0;
series2.columns.template.tooltipText = "{category}: [bold]{value}[/]";
series2.columns.template.radarColumn.cornerRadius = 20;
series2.columns.template.adapter.add("fill", function(fill, target) {
	return color_value(target.dataItem.valueX)});

// Add cursor
chart.cursor = new am4charts.RadarCursor();
