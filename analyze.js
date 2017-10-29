function spreadsheetAnalytics() {
    // Get the channel ID
    var myChannels = YouTube.Channels.list('id', {mine: true});
    var channel = myChannels.items[0];
    var channelId = channel.id;
    // Set the dates for our report
    var today = new Date();
    var oneMonthAgo = new Date();
    oneMonthAgo.setMonth(today.getMonth() - 1);
    var todayFormatted = Utilities.formatDate(today, 'UTC', 'yyyy-MM-dd')
    var oneMonthAgoFormatted = Utilities.formatDate(oneMonthAgo, 'UTC', 'yyyy-MM-dd');

    // The YouTubeAnalytics.Reports.query() function has four required parameters and one optional
    // parameter. The first parameter identifies the channel or content owner for which you are
    // retrieving data. The second and third parameters specify the start and end dates for the
    // report, respectively. The fourth parameter identifies the metrics that you are retrieving.
    // The fifth parameter is an object that contains any additional optional parameters
    // (dimensions, filters, sort, etc.) that you want to set.
    var analyticsResponse = YouTubeAnalytics.Reports.query(
        'channel==' + channelId,
        oneMonthAgoFormatted,
        todayFormatted,
        'views,likes,dislikes,shares',
        {
            dimensions: 'day',
            sort: '-day'
        });

    // Create a new Spreadsheet with rows and columns corresponding to our dates
    var ssName = 'YouTube channel report ' + oneMonthAgoFormatted + ' - ' + todayFormatted;
    var numRows = analyticsResponse.rows.length;
    var numCols = analyticsResponse.columnHeaders.length;

    // Add an extra row for column headers
    var ssNew = SpreadsheetApp.create(ssName, numRows + 1, numCols);

    // Get the first sheet
    var sheet = ssNew.getSheets()[0];

    // Get the range for the title columns
    // Remember, spreadsheets are 1-indexed, whereas arrays are 0-indexed
    var headersRange = sheet.getRange(1, 1, 1, numCols);
    var headers = [];

    // These column headers will correspond with the metrics requested
    // in the initial call: views, likes, dislikes, shares
    for (var i in analyticsResponse.columnHeaders) {
        var columnHeader = analyticsResponse.columnHeaders[i];
        var columnName = columnHeader.name;
        headers[i] = columnName;
    }
    // This takes a 2 dimensional array
    headersRange.setValues([headers]);

    // Bold and freeze the column names
    headersRange.setFontWeight('bold');
    sheet.setFrozenRows(1);

    // Get the data range and set the values
    var dataRange = sheet.getRange(2, 1, numRows, numCols);
    dataRange.setValues(analyticsResponse.rows);

    // Bold and freeze the dates
    var dateHeaders = sheet.getRange(1, 1, numRows, 1);
    dateHeaders.setFontWeight('bold');
    sheet.setFrozenColumns(1);

    // Include the headers in our range. The headers are used
    // to label the axes
    var range = sheet.getRange(1, 1, numRows, numCols);
    var chart = sheet.newChart()
        .asColumnChart()
        .setStacked()
        .addRange(range)
        .setPosition(4, 2, 10, 10)
        .build();
    sheet.insertChart(chart);

}