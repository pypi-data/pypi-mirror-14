jQuery.fn.toCSV = function(name) {
	var data = $(this).first(); //Only one table
	var csvData = [];
	var tmpArr = [];
	var tmpStr = '';
	data.find("tr").each(function() {
		if($(this).find("th").length) {
			$(this).find("th").each(function() {
				tmpStr = $(this).text().replace(/"/g, '""').replace(/(?:\r\n|\r|\n)/g, ' ');;
				tmpArr.push('"' + tmpStr.trim() + '"');
			});
			csvData.push(tmpArr);
		} else {
			tmpArr = [];
			$(this).find("td").each(function() {
				if($(this).text().match(/^-{0,1}\d*\.{0,1}\d+$/)) {
					tmpArr.push(parseFloat($(this).text()));
				} else {
					tmpStr = $(this).text().replace(/"/g, '""').replace(/(?:\r\n|\r|\n)/g, ' ');;
					tmpArr.push('"' + tmpStr.trim() + '"');
				}
			});
			csvData.push(tmpArr.join(','));
		}
	});
	var output = csvData.join('\n');
	var uri = 'data:application/csv;charset=UTF-8,' + encodeURIComponent(output);
	var link = document.createElement('a');
	link.download = name;
	link.href = uri;
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
}
