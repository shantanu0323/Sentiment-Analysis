import json
from textblob import TextBlob
from pathlib import Path

f = open("./commentData.json")
s = f.read()

root = json.loads(s)

items = root['items']

total = 0
count = 0
datas = []
for item in items:
    snippet = item['snippet']
    topLevelComment = snippet['topLevelComment']
    innerSnippet = topLevelComment['snippet']
    textDisplay = innerSnippet['textDisplay']
    data = {}
    data['textDisplay'] = textDisplay
    blob = TextBlob(textDisplay)

    # print(textDisplay)
    tot = 0
    c = 0
    for sentence in blob.sentences:
        tot += sentence.sentiment.polarity
        c += 1

    score = tot / c * 100
    score = float("{0:.2f}".format(score))
    data['score'] = score
    datas.append(data)
    # print(score)
    # print('**********************')
    count += 1
    total += score
overallScore = total / count;
overallScore = float("{0:.2f}".format(overallScore))
# print(overallScore)

htmlSource = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Analysis</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>

    <script src="https://code.highcharts.com/modules/solid-gauge.js"></script>


    <script>

        var gaugeOptions = {

            chart: {
                type: 'solidgauge'
            },

            title: null,

            pane: {
                center: ['50%', '85%'],
                size: '140%',
                startAngle: -90,
                endAngle: 90,
                background: {
                    backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                    innerRadius: '60%',
                    outerRadius: '100%',
                    shape: 'arc'
                }
            },

            tooltip: {
                enabled: false
            },

            // the value axis
            yAxis: {
                stops: [
                    [0.1, '#DF5353'], // green
                    [0.5, '#EEEE00'], // yellow
                    [0.9, '#55BF3B'] // red
                ],
                lineWidth: 0,
                minorTickInterval: null,
                tickAmount: 2,
                title: {
                    y: -70
                },
                labels: {
                    y: 16
                }
            },

            plotOptions: {
                solidgauge: {
                    dataLabels: {
                        y: 5,
                        borderWidth: 0,
                        useHTML: true
                    }
                }
            }
        };

    </script>

    <style>
        * {
            margin: 0;
            padding: 0;
            font-family: helvetica;
        }

        table {
            display: block;
            width: 80%;
            border: 2px solid black;
            position: absolute;
            left: 50%;
            transform: translate(-50%, 0);
        }

        tr {
            border-bottom: 1px solid black;                    
        }

        td.text {
            width: 90%;
            padding: 5px;
            font-size: 20px;
        }

        td.graph {
            width: 30%;
        }
    </style>
</head>
<body>

<table>
    <tr>
        <td colspan="2" class="graph">
            <div id="container-overall" style="width: 600px; height: 360px"></div>
            <script>
                // The polarity gauge
                var value = ''' + str(overallScore) + ''';
                var result = (value == 0 ? 'Neutral' : (value > 0 ? 'Positive' : 'Negative'));
                var formatData = '<div style="text-align:center; padding:0"><span style="font-size:40px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}%</span><br/>' +
                    '<span style="font-size:20px;color:#aaa">' + result + '</span></div>';
                var chartPolarity = Highcharts.chart('container-overall', Highcharts.merge(gaugeOptions, {
                    yAxis: {
                        min: -100,
                        max: 100,
                        title: {
                            text: 'Polarity'
                        }
                    },

                    credits: {
                        enabled: false
                    },

                    series: [{
                        name: 'Polarity',
                        data: [value],
                        dataLabels: {
                            format: formatData
                        },
                        tooltip: {
                            valueSuffix: '%pos'
                        }
                    }]

                }));

            </script>

        </td>
    </tr>'''

i = 0
for data in datas:
    i += 1
    htmlSource = htmlSource + '''
        <tr>
        <td class="text">''' + data['textDisplay'] + '''</td>
        <td class="graph">
            <div id="container-polarity-'''+ str(i) + '''" style="width: 200px; height: 120px"></div>
            <script>
                // The polarity gauge
                var value = ''' + str(data['score']) + ''';
                var result = (value == 0 ? 'Neutral' : (value > 0 ? 'Positive' : 'Negative'));
                var formatData = '<div style="text-align:center; padding:0"><span style="font-size:14px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}%</span><br/>' +
                    '<span style="font-size:12px;color:#aaa">' + result + '</span></div>';
                var chartPolarity = Highcharts.chart("container-polarity-'''+ str(i) + '''", Highcharts.merge(gaugeOptions, {
                    yAxis: {
                        min: -100,
                        max: 100,
                        title: {
                            text: 'Polarity'
                        }
                    },

                    credits: {
                        enabled: false
                    },

                    series: [{
                        name: 'Polarity',
                        data: [value],
                        dataLabels: {
                            format: formatData
                        },
                        tooltip: {
                            valueSuffix: '%pos'
                        }
                    }]

                }));

            </script>

        </td>
    </tr>
    '''

htmlSource = htmlSource + '''
    </table>
    </body>
    </html>'''

try:
    f = open('./commentsAnalysis.html', 'w', encoding='utf8')
    f.write(htmlSource)
    f.close()
except FileNotFoundError as error:
    print("There was an error in creating the webpage" + error)
else:
    link = Path("commentsAnalysis.html").resolve()
    print("You can now visit the link '" + str(link) + "'")
