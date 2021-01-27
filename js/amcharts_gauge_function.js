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

function format_user_data(group_percent,total_user_count,active_user_per,group_title){
  output = [{
  "category": group_title,
  "active_users": active_user_per*100,
  "delta": (active_user_per-group_percent)*100,
  "value": group_percent*100,
  "full": 100}];
  return output}





function drawGuageChart(data,div_id){
  // Assinging Chart to Div
  var chart = am4core.create(div_id, am4charts.RadarChart);
  var colorSet = new am4core.ColorSet();

  chart.data = data

  // Make chart not full circle
  chart.startAngle = -90;
  chart.endAngle = 180;
  chart.innerRadius = am4core.percent(70);

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

  var series3 = chart.series.push(new am4charts.RadarColumnSeries());
  series3.dataFields.valueX = "active_users";
  series3.dataFields.categoryY = "category";
  series3.clustered = false;
  series3.columns.template.adapter.add("fill",function(fill, target) {
  	return color_value(parseInt("{delta}")).lighten(.6)});
  series3.columns.template.fillOpacity = 1;
  series3.columns.template.cornerRadiusTopLeft = 20;
  series3.columns.template.strokeWidth = 0;
  series3.columns.template.tooltipText = "Active Users not using \n this functionality: [bold]{delta}[/]";
  series3.columns.template.tooltipPosition = "pointer"
  series3.columns.template.radarColumn.cornerRadius = 20;

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
}

drawGuageChart(format_user_data(.45,300,.67,"Lit Users"),"amcharts_demo2")
